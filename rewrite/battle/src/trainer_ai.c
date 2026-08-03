#include "pokered/battle/trainer_ai.h"

#include <stddef.h>
#include <string.h>

enum {
    EFFECT_01 = 0x01,
    ATTACK_UP1_EFFECT = 0x0a,
    BIDE_EFFECT = 0x1a,
    SLEEP_EFFECT = 0x20,
    SUPER_FANG_EFFECT = 0x28,
    SPECIAL_DAMAGE_EFFECT = 0x29,
    FLY_EFFECT = 0x2b,
    ATTACK_UP2_EFFECT = 0x32,
    POISON_EFFECT = 0x42,
    PARALYZE_EFFECT = 0x43
};

typedef struct {
    uint8_t layers;
    TrainerAiPolicy policy;
    uint8_t maximum_uses;
} TrainerClassPolicy;

#define LAYER_1 (1U << 0U)
#define LAYER_2 (1U << 1U)
#define LAYER_3 (1U << 2U)

#include "gen1_trainer_tables.generated.h"

static bool is_status_ailment_effect(uint8_t effect) {
    return effect == EFFECT_01 || effect == SLEEP_EFFECT ||
           effect == POISON_EFFECT || effect == PARALYZE_EFFECT;
}

static bool layer_two_prefers(uint8_t effect) {
    return (effect >= ATTACK_UP1_EFFECT && effect < BIDE_EFFECT) ||
           (effect >= ATTACK_UP2_EFFECT && effect < POISON_EFFECT);
}

static bool has_better_move(const TrainerAiMoveObservation *observation,
                            const TrainerAiMove *ineffective) {
    size_t index;

    for (index = 0; index < TRAINER_AI_MOVE_SLOTS; ++index) {
        const TrainerAiMove *move = &observation->moves[index];
        if (move->id == 0U) {
            break;
        }
        if (move->effect == SUPER_FANG_EFFECT ||
            move->effect == SPECIAL_DAMAGE_EFFECT || move->effect == FLY_EFFECT) {
            return true;
        }
        if (move->type != ineffective->type && move->power != 0U) {
            return true;
        }
    }
    return false;
}

BattleStatus trainer_ai_score_moves(const TrainerAiMoveObservation *observation,
                                    TrainerAiMoveScores *result) {
    const TrainerClassPolicy *trainer_class;
    uint8_t minimum = UINT8_MAX;
    size_t index;

    if (observation == NULL || result == NULL || observation->trainer_class < 1U ||
        observation->trainer_class > GEN1_TRAINER_CLASS_COUNT ||
        observation->disabled_move_slot > TRAINER_AI_MOVE_SLOTS) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }

    trainer_class = &TRAINER_CLASSES[observation->trainer_class - 1U];
    for (index = 0; index < TRAINER_AI_MOVE_SLOTS; ++index) {
        result->scores[index] = 10U;
        result->candidates[index] = 0U;
    }
    if (observation->disabled_move_slot != 0U) {
        result->scores[observation->disabled_move_slot - 1U] = 0x50U;
    }

    for (index = 0; index < TRAINER_AI_MOVE_SLOTS; ++index) {
        const TrainerAiMove *move = &observation->moves[index];
        uint8_t effectiveness;
        if (move->id == 0U) {
            break;
        }
        if ((trainer_class->layers & LAYER_1) != 0U &&
            observation->defender_status != 0U && move->power == 0U &&
            is_status_ailment_effect(move->effect)) {
            result->scores[index] = (uint8_t)(result->scores[index] + 5U);
        }
        if ((trainer_class->layers & LAYER_2) != 0U &&
            observation->layer2_encouragement == 1U &&
            layer_two_prefers(move->effect)) {
            result->scores[index] = (uint8_t)(result->scores[index] - 1U);
        }
        if ((trainer_class->layers & LAYER_3) == 0U) {
            continue;
        }
        effectiveness =
            combat_math_ai_type_effectiveness(move->type,
                                              observation->defender_types);
        if (effectiveness > 0x10U) {
            result->scores[index] = (uint8_t)(result->scores[index] - 1U);
        } else if (effectiveness < 0x10U &&
                   has_better_move(observation, move)) {
            result->scores[index] = (uint8_t)(result->scores[index] + 1U);
        }
    }

    for (index = 0; index < TRAINER_AI_MOVE_SLOTS; ++index) {
        if (observation->moves[index].id != 0U &&
            result->scores[index] < minimum) {
            minimum = result->scores[index];
        }
    }
    for (index = 0; index < TRAINER_AI_MOVE_SLOTS; ++index) {
        if (observation->moves[index].id != 0U &&
            result->scores[index] == minimum) {
            result->candidates[index] = observation->moves[index].id;
        }
    }
    return BATTLE_STATUS_OK;
}

BattleStatus trainer_ai_choose_move(const TrainerAiMoveScores *scores,
                                    uint8_t disabled_move_slot,
                                    BattleRandomSource *random,
                                    TrainerAiDecision *decision) {
    uint8_t roll;
    uint8_t slot;
    BattleStatus status;

    if (scores == NULL || decision == NULL ||
        disabled_move_slot > TRAINER_AI_MOVE_SLOTS) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }

    for (;;) {
        status = battle_random_next(random, &roll);
        if (status != BATTLE_STATUS_OK) {
            return status;
        }
        if (roll < 63U) {
            slot = 0U;
        } else if (roll < 127U) {
            slot = 1U;
        } else if (roll < 190U) {
            slot = 2U;
        } else {
            slot = 3U;
        }
        if (scores->candidates[slot] == 0U ||
            disabled_move_slot == (uint8_t)(slot + 1U)) {
            continue;
        }
        decision->action = TRAINER_AI_ACTION_MOVE;
        decision->move_slot = slot;
        decision->move_id = scores->candidates[slot];
        decision->consumes_action_count = false;
        decision->remaining_action_count = 0U;
        return BATTLE_STATUS_OK;
    }
}

static bool hp_below_fraction(uint16_t hp, uint16_t max_hp, uint8_t fraction) {
    return hp < (uint16_t)(max_hp / fraction);
}

static TrainerAiAction switch_if_possible(uint8_t living_party_members) {
    return living_party_members >= 2U ? TRAINER_AI_ACTION_SWITCH
                                     : TRAINER_AI_ACTION_NONE;
}

BattleStatus trainer_ai_choose_special_action(
    const TrainerAiSpecialObservation *observation,
    TrainerAiDecision *decision) {
    TrainerAiAction action = TRAINER_AI_ACTION_NONE;
    uint8_t roll;

    if (observation == NULL || decision == NULL || observation->max_hp == 0U ||
        observation->current_hp > observation->max_hp) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }
    if (observation->mode != GEN1_FIDELITY) {
        return BATTLE_STATUS_UNSUPPORTED_MODE;
    }
    roll = observation->random_roll;

    switch (observation->policy) {
    case TRAINER_AI_POLICY_GENERIC:
        break;
    case TRAINER_AI_POLICY_JUGGLER:
        if (roll < 64U) {
            action = switch_if_possible(observation->living_party_members);
        }
        break;
    case TRAINER_AI_POLICY_BLACKBELT:
        if (roll < 32U) {
            action = TRAINER_AI_ACTION_USE_X_ATTACK;
        }
        break;
    case TRAINER_AI_POLICY_GIOVANNI:
        if (roll < 64U) {
            action = TRAINER_AI_ACTION_USE_GUARD_SPEC;
        }
        break;
    case TRAINER_AI_POLICY_COOLTRAINER_M:
    case TRAINER_AI_POLICY_KOGA:
        if (roll < 64U) {
            action = TRAINER_AI_ACTION_USE_X_ATTACK;
        }
        break;
    case TRAINER_AI_POLICY_COOLTRAINER_F:
        if (hp_below_fraction(observation->current_hp, observation->max_hp,
                              10U)) {
            action = TRAINER_AI_ACTION_USE_HYPER_POTION;
        } else if (hp_below_fraction(observation->current_hp,
                                     observation->max_hp, 5U)) {
            action = switch_if_possible(observation->living_party_members);
        }
        break;
    case TRAINER_AI_POLICY_BROCK:
        if (observation->status != 0U) {
            action = TRAINER_AI_ACTION_USE_FULL_HEAL;
        }
        break;
    case TRAINER_AI_POLICY_MISTY:
    case TRAINER_AI_POLICY_BRUNO:
        if (roll < 64U) {
            action = TRAINER_AI_ACTION_USE_X_DEFEND;
        }
        break;
    case TRAINER_AI_POLICY_LT_SURGE:
        if (roll < 64U) {
            action = TRAINER_AI_ACTION_USE_X_SPEED;
        }
        break;
    case TRAINER_AI_POLICY_ERIKA:
        if (roll < 128U &&
            hp_below_fraction(observation->current_hp, observation->max_hp,
                              10U)) {
            action = TRAINER_AI_ACTION_USE_SUPER_POTION;
        }
        break;
    case TRAINER_AI_POLICY_BLAINE:
        if (roll < 64U) {
            action = TRAINER_AI_ACTION_USE_SUPER_POTION;
        }
        break;
    case TRAINER_AI_POLICY_SABRINA:
        if (roll < 64U &&
            hp_below_fraction(observation->current_hp, observation->max_hp,
                              10U)) {
            action = TRAINER_AI_ACTION_USE_HYPER_POTION;
        }
        break;
    case TRAINER_AI_POLICY_RIVAL2:
        if (roll < 32U &&
            hp_below_fraction(observation->current_hp, observation->max_hp,
                              5U)) {
            action = TRAINER_AI_ACTION_USE_POTION;
        }
        break;
    case TRAINER_AI_POLICY_RIVAL3:
        if (roll < 32U &&
            hp_below_fraction(observation->current_hp, observation->max_hp,
                              5U)) {
            action = TRAINER_AI_ACTION_USE_FULL_RESTORE;
        }
        break;
    case TRAINER_AI_POLICY_LORELEI:
        if (roll < 128U &&
            hp_below_fraction(observation->current_hp, observation->max_hp,
                              5U)) {
            action = TRAINER_AI_ACTION_USE_SUPER_POTION;
        }
        break;
    case TRAINER_AI_POLICY_AGATHA:
        if (roll < 20U) {
            action = switch_if_possible(observation->living_party_members);
        } else if (roll < 128U &&
                   hp_below_fraction(observation->current_hp,
                                     observation->max_hp, 4U)) {
            action = TRAINER_AI_ACTION_USE_SUPER_POTION;
        }
        break;
    case TRAINER_AI_POLICY_LANCE:
        if (roll < 128U &&
            hp_below_fraction(observation->current_hp, observation->max_hp,
                              5U)) {
            action = TRAINER_AI_ACTION_USE_HYPER_POTION;
        }
        break;
    default:
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }

    decision->action = action;
    decision->move_slot = 0U;
    decision->move_id = 0U;
    decision->consumes_action_count = action != TRAINER_AI_ACTION_NONE;
    decision->remaining_action_count = 0U;
    return BATTLE_STATUS_OK;
}

BattleStatus trainer_ai_policy_for_class(uint8_t trainer_class,
                                         TrainerAiPolicy *policy,
                                         uint8_t *maximum_uses) {
    const TrainerClassPolicy *entry;
    if (trainer_class < 1U || trainer_class > GEN1_TRAINER_CLASS_COUNT ||
        policy == NULL || maximum_uses == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }
    entry = &TRAINER_CLASSES[trainer_class - 1U];
    *policy = entry->policy;
    *maximum_uses = entry->maximum_uses;
    return BATTLE_STATUS_OK;
}

uint8_t trainer_ai_decrement_action_count(uint8_t action_count) {
    return (uint8_t)(action_count - 1U);
}

BattleStatus trainer_ai_decide(const TrainerAiObservation *observation,
                               BattleRandomSource *random,
                               TrainerAiDecision *decision) {
    TrainerAiPolicy policy;
    TrainerAiSpecialObservation special;
    TrainerAiMoveScores scores;
    TrainerAiDecision special_decision;
    uint8_t maximum_uses;
    uint8_t action_count;
    uint8_t roll;
    BattleStatus status;

    if (observation == NULL || decision == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }
    if (observation->mode != GEN1_FIDELITY) {
        return BATTLE_STATUS_UNSUPPORTED_MODE;
    }
    status = trainer_ai_policy_for_class(
        observation->move_observation.trainer_class, &policy, &maximum_uses);
    if (status != BATTLE_STATUS_OK) {
        return status;
    }

    action_count = observation->action_count == UINT8_MAX
                       ? maximum_uses
                       : observation->action_count;
    if (action_count != 0U) {
        status = battle_random_next(random, &roll);
        if (status != BATTLE_STATUS_OK) {
            return status;
        }
        special = (TrainerAiSpecialObservation){
            observation->mode,
            policy,
            roll,
            observation->current_hp,
            observation->max_hp,
            observation->own_status,
            observation->living_party_members,
        };
        status = trainer_ai_choose_special_action(&special, &special_decision);
        if (status != BATTLE_STATUS_OK) {
            return status;
        }
        if (special_decision.action != TRAINER_AI_ACTION_NONE) {
            *decision = special_decision;
            decision->remaining_action_count =
                trainer_ai_decrement_action_count(action_count);
            return BATTLE_STATUS_OK;
        }
    }

    status = trainer_ai_score_moves(&observation->move_observation, &scores);
    if (status != BATTLE_STATUS_OK) {
        return status;
    }
    status = trainer_ai_choose_move(
        &scores, observation->move_observation.disabled_move_slot, random,
        decision);
    if (status == BATTLE_STATUS_OK) {
        decision->remaining_action_count = action_count;
    }
    return status;
}
