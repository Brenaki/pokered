#ifndef POKERED_BATTLE_COMBAT_MATH_H
#define POKERED_BATTLE_COMBAT_MATH_H

#include "pokered/battle/common.h"

enum {
    GEN1_SPECIAL_TYPE = 20,
    GEN1_SWIFT_EFFECT = 0x11,
    GEN1_EXPLODE_EFFECT = 0x07
};

typedef struct {
    uint8_t first;
    uint8_t second;
} PokemonTypes;

typedef struct {
    uint16_t current_attack;
    uint16_t current_special;
    uint16_t base_attack;
    uint16_t base_special;
    uint16_t current_defense;
    uint16_t current_defender_special;
    uint16_t base_defense;
    uint16_t base_defender_special;
    uint8_t move_power;
    uint8_t move_type;
    uint8_t level;
    bool critical;
    bool reflect;
    bool light_screen;
} DamageStatsInput;

typedef struct {
    uint8_t attack;
    uint8_t defense;
    uint8_t power;
    uint8_t level;
} DamageStats;

typedef struct {
    uint8_t attack;
    uint8_t defense;
    uint8_t power;
    uint8_t level;
    uint8_t move_effect;
    uint16_t accumulated_damage;
} BaseDamageInput;

typedef struct {
    uint16_t damage;
    uint8_t damage_multipliers;
    bool stab;
    bool immune_or_rounded_to_zero;
} TypeDamageResult;

uint8_t combat_math_scale_accuracy(uint8_t accuracy, uint8_t accuracy_stage,
                                   uint8_t evasion_stage);

BattleStatus combat_math_roll_hit(uint8_t accuracy, uint8_t accuracy_stage,
                                  uint8_t evasion_stage, bool bypass_accuracy,
                                  BattleRandomSource *random, bool *hit,
                                  uint8_t *scaled_accuracy);

uint8_t combat_math_critical_threshold(uint8_t base_speed, bool high_critical,
                                       bool focus_energy);

BattleStatus combat_math_roll_critical(uint8_t base_speed, uint8_t move_power,
                                       bool high_critical, bool focus_energy,
                                       BattleRandomSource *random,
                                       bool *critical);

bool combat_math_is_high_critical_move(uint8_t move_id);

BattleStatus combat_math_select_damage_stats(const DamageStatsInput *input,
                                             DamageStats *result);

BattleStatus combat_math_calculate_base_damage(const BaseDamageInput *input,
                                               uint16_t *damage);

BattleStatus combat_math_apply_type_modifiers(uint16_t damage,
                                              PokemonTypes attacker,
                                              PokemonTypes defender,
                                              uint8_t move_type,
                                              TypeDamageResult *result);

uint8_t combat_math_ai_type_effectiveness(uint8_t move_type,
                                          PokemonTypes defender);

BattleStatus combat_math_randomize_damage(uint16_t damage,
                                          BattleRandomSource *random,
                                          uint16_t *result);

#endif
