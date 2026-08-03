#include "pokered/battle/combat_math.h"

#include <stddef.h>

typedef struct {
    uint8_t numerator;
    uint8_t denominator;
} StatRatio;

typedef struct {
    uint8_t attacker;
    uint8_t defender;
    uint8_t multiplier;
} TypeEffect;

#include "gen1_combat_tables.generated.h"

static uint8_t rotate_left_three(uint8_t value) {
    return (uint8_t)((uint8_t)(value << 3U) | (uint8_t)(value >> 5U));
}

static uint8_t rotate_right_one(uint8_t value) {
    return (uint8_t)((uint8_t)(value >> 1U) | (uint8_t)(value << 7U));
}

static uint8_t saturating_double(uint8_t value) {
    return value > 127U ? UINT8_MAX : (uint8_t)(value * 2U);
}

uint8_t combat_math_scale_accuracy(uint8_t accuracy, uint8_t accuracy_stage,
                                   uint8_t evasion_stage) {
    uint32_t value = accuracy;
    uint8_t reflected_evasion;
    const StatRatio *ratio;

    if (accuracy_stage < 1U || accuracy_stage > 13U || evasion_stage < 1U ||
        evasion_stage > 13U) {
        return 0;
    }

    reflected_evasion = (uint8_t)(14U - evasion_stage);
    ratio = &STAT_RATIOS[accuracy_stage - 1U];
    value = (value * ratio->numerator) / ratio->denominator;
    if (value == 0U) {
        value = 1U;
    }

    ratio = &STAT_RATIOS[reflected_evasion - 1U];
    value = (value * ratio->numerator) / ratio->denominator;
    if (value == 0U) {
        value = 1U;
    }

    return value > UINT8_MAX ? UINT8_MAX : (uint8_t)value;
}

BattleStatus combat_math_roll_hit(uint8_t accuracy, uint8_t accuracy_stage,
                                  uint8_t evasion_stage, bool bypass_accuracy,
                                  BattleRandomSource *random, bool *hit,
                                  uint8_t *scaled_accuracy) {
    uint8_t roll;
    BattleStatus status;

    if (hit == NULL || scaled_accuracy == NULL || accuracy_stage < 1U ||
        accuracy_stage > 13U || evasion_stage < 1U || evasion_stage > 13U) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }

    if (bypass_accuracy) {
        *scaled_accuracy = accuracy;
        *hit = true;
        return BATTLE_STATUS_OK;
    }

    *scaled_accuracy =
        combat_math_scale_accuracy(accuracy, accuracy_stage, evasion_stage);
    status = battle_random_next(random, &roll);
    if (status != BATTLE_STATUS_OK) {
        return status;
    }
    *hit = roll < *scaled_accuracy;
    return BATTLE_STATUS_OK;
}

uint8_t combat_math_critical_threshold(uint8_t base_speed, bool high_critical,
                                       bool focus_energy) {
    uint8_t threshold = (uint8_t)(base_speed >> 1U);

    threshold = focus_energy ? (uint8_t)(threshold >> 1U)
                             : saturating_double(threshold);
    if (high_critical) {
        threshold = saturating_double(threshold);
        threshold = saturating_double(threshold);
    } else {
        threshold = (uint8_t)(threshold >> 1U);
    }
    return threshold;
}

BattleStatus combat_math_roll_critical(uint8_t base_speed, uint8_t move_power,
                                       bool high_critical, bool focus_energy,
                                       BattleRandomSource *random,
                                       bool *critical) {
    uint8_t roll;
    BattleStatus status;

    if (critical == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }
    if (move_power == 0U) {
        *critical = false;
        return BATTLE_STATUS_OK;
    }
    status = battle_random_next(random, &roll);
    if (status != BATTLE_STATUS_OK) {
        return status;
    }
    *critical = rotate_left_three(roll) <
                combat_math_critical_threshold(base_speed, high_critical,
                                               focus_energy);
    return BATTLE_STATUS_OK;
}

bool combat_math_is_high_critical_move(uint8_t move_id) {
    size_t index;
    for (index = 0;
         index < sizeof(HIGH_CRITICAL_MOVES) / sizeof(HIGH_CRITICAL_MOVES[0]);
         ++index) {
        if (HIGH_CRITICAL_MOVES[index] == move_id) {
            return true;
        }
    }
    return false;
}

BattleStatus combat_math_select_damage_stats(const DamageStatsInput *input,
                                             DamageStats *result) {
    uint16_t attack;
    uint16_t defense;
    bool special;

    if (input == NULL || result == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }

    special = input->move_type >= GEN1_SPECIAL_TYPE;
    if (input->critical) {
        attack = special ? input->base_special : input->base_attack;
        defense = special ? input->base_defender_special : input->base_defense;
    } else {
        attack = special ? input->current_special : input->current_attack;
        defense = special ? input->current_defender_special
                          : input->current_defense;
        if ((special && input->light_screen) || (!special && input->reflect)) {
            defense = (uint16_t)(defense * 2U);
        }
    }

    if (attack > UINT8_MAX || defense > UINT8_MAX) {
        attack >>= 2U;
        defense >>= 2U;
    }
    if (attack == 0U) {
        attack = 1U;
    }

    result->attack = (uint8_t)attack;
    result->defense = (uint8_t)defense;
    result->power = input->move_power;
    result->level = (uint8_t)(input->critical
                                  ? (uint8_t)(input->level << 1U)
                                  : input->level);
    return BATTLE_STATUS_OK;
}

BattleStatus combat_math_calculate_base_damage(const BaseDamageInput *input,
                                               uint16_t *damage) {
    uint32_t calculated;
    uint8_t defense;

    if (input == NULL || damage == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }
    if (input->power == 0U) {
        *damage = input->accumulated_damage;
        return BATTLE_STATUS_OK;
    }

    defense = input->defense;
    if (input->move_effect == GEN1_EXPLODE_EFFECT) {
        defense = (uint8_t)(defense >> 1U);
        if (defense == 0U) {
            defense = 1U;
        }
    }
    if (defense == 0U) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }

    calculated = ((uint32_t)input->level * 2U) / 5U;
    calculated += 2U;
    calculated *= input->power;
    calculated *= input->attack;
    calculated /= defense;
    calculated /= 50U;
    calculated += input->accumulated_damage;
    if (calculated > 997U) {
        calculated = 997U;
    }
    *damage = (uint16_t)(calculated + 2U);
    return BATTLE_STATUS_OK;
}

BattleStatus combat_math_apply_type_modifiers(uint16_t damage,
                                              PokemonTypes attacker,
                                              PokemonTypes defender,
                                              uint8_t move_type,
                                              TypeDamageResult *result) {
    size_t index;

    if (result == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }

    result->damage = damage;
    result->stab = move_type == attacker.first || move_type == attacker.second;
    result->damage_multipliers = result->stab ? 0x80U : 0U;
    result->immune_or_rounded_to_zero = false;
    if (result->stab) {
        result->damage = (uint16_t)(damage + (damage >> 1U));
    }

    for (index = 0; index < sizeof(TYPE_EFFECTS) / sizeof(TYPE_EFFECTS[0]);
         ++index) {
        const TypeEffect *effect = &TYPE_EFFECTS[index];
        if (effect->attacker != move_type ||
            (effect->defender != defender.first &&
             effect->defender != defender.second)) {
            continue;
        }
        result->damage =
            (uint16_t)(((uint32_t)result->damage * effect->multiplier) / 10U);
        result->damage_multipliers =
            (uint8_t)(effect->multiplier | (result->stab ? 0x80U : 0U));
        if (result->damage == 0U) {
            result->immune_or_rounded_to_zero = true;
        }
    }
    return BATTLE_STATUS_OK;
}

uint8_t combat_math_ai_type_effectiveness(uint8_t move_type,
                                          PokemonTypes defender) {
    size_t index;

    for (index = 0; index < sizeof(TYPE_EFFECTS) / sizeof(TYPE_EFFECTS[0]);
         ++index) {
        const TypeEffect *effect = &TYPE_EFFECTS[index];
        if (effect->attacker == move_type &&
            (effect->defender == defender.first ||
             effect->defender == defender.second)) {
            return effect->multiplier;
        }
    }
    return 0x10U;
}

BattleStatus combat_math_randomize_damage(uint16_t damage,
                                          BattleRandomSource *random,
                                          uint16_t *result) {
    uint8_t roll;
    uint8_t factor;
    BattleStatus status;

    if (result == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }
    if (damage < 2U) {
        *result = damage;
        return BATTLE_STATUS_OK;
    }

    do {
        status = battle_random_next(random, &roll);
        if (status != BATTLE_STATUS_OK) {
            return status;
        }
        factor = rotate_right_one(roll);
    } while (factor < 217U);

    *result = (uint16_t)(((uint32_t)damage * factor) / UINT8_MAX);
    return BATTLE_STATUS_OK;
}
