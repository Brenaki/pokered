#include "pokered/battle/combat_math.h"
#include "pokered/battle/trainer_ai.h"

#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const uint8_t *values;
    size_t length;
    size_t position;
} RandomSequence;

static unsigned int failures;

#define CHECK(condition)                                                        \
    do {                                                                        \
        if (!(condition)) {                                                      \
            fprintf(stderr, "%s:%d: check failed: %s\n", __FILE__, __LINE__,  \
                    #condition);                                                 \
            ++failures;                                                          \
        }                                                                        \
    } while (0)

static bool next_random(void *context, uint8_t *value) {
    RandomSequence *sequence = context;
    if (sequence->position >= sequence->length) {
        return false;
    }
    *value = sequence->values[sequence->position++];
    return true;
}

static BattleRandomSource random_source(RandomSequence *sequence) {
    BattleRandomSource source = {next_random, sequence};
    return source;
}

static void test_accuracy(void) {
    const uint8_t miss_values[] = {255};
    const uint8_t hit_values[] = {254};
    RandomSequence miss_sequence = {miss_values, 1, 0};
    RandomSequence hit_sequence = {hit_values, 1, 0};
    BattleRandomSource miss_random = random_source(&miss_sequence);
    BattleRandomSource hit_random = random_source(&hit_sequence);
    bool hit = false;
    uint8_t scaled = 0;

    CHECK(combat_math_scale_accuracy(255, 7, 7) == 255);
    CHECK(combat_math_roll_hit(255, 7, 7, false, &miss_random, &hit,
                               &scaled) == BATTLE_STATUS_OK);
    CHECK(!hit);
    CHECK(scaled == 255);
    CHECK(combat_math_roll_hit(255, 7, 7, false, &hit_random, &hit, &scaled) ==
          BATTLE_STATUS_OK);
    CHECK(hit);
    CHECK(combat_math_roll_hit(1, 1, 13, true, NULL, &hit, &scaled) ==
          BATTLE_STATUS_OK);
    CHECK(hit);
    CHECK(scaled == 1);
}

static void test_critical_hits(void) {
    const uint8_t hit_values[] = {130};
    const uint8_t cap_values[] = {255};
    RandomSequence hit_sequence = {hit_values, 1, 0};
    RandomSequence cap_sequence = {cap_values, 1, 0};
    BattleRandomSource hit_random = random_source(&hit_sequence);
    BattleRandomSource cap_random = random_source(&cap_sequence);
    bool critical = false;

    CHECK(combat_math_critical_threshold(100, false, false) == 50);
    CHECK(combat_math_critical_threshold(100, false, true) == 12);
    CHECK(combat_math_critical_threshold(100, true, false) == 255);
    CHECK(combat_math_roll_critical(100, 40, false, false, &hit_random,
                                    &critical) ==
          BATTLE_STATUS_OK);
    CHECK(critical);
    CHECK(combat_math_roll_critical(100, 70, true, false, &cap_random,
                                    &critical) ==
          BATTLE_STATUS_OK);
    CHECK(!critical);
    CHECK(combat_math_is_high_critical_move(163));
    CHECK(!combat_math_is_high_critical_move(33));
    CHECK(combat_math_roll_critical(100, 0, false, false, NULL, &critical) ==
          BATTLE_STATUS_OK);
    CHECK(!critical);
}

static void test_damage(void) {
    BaseDamageInput base = {100, 80, 80, 50, 0, 0};
    DamageStatsInput stats = {
        .current_attack = 100,
        .current_special = 200,
        .base_attack = 100,
        .base_special = 200,
        .current_defense = 80,
        .current_defender_special = 160,
        .base_defense = 80,
        .base_defender_special = 160,
        .move_power = 80,
        .move_type = 0,
        .level = 50,
    };
    DamageStats selected = {0};
    TypeDamageResult typed = {0};
    uint16_t damage = 0;

    CHECK(combat_math_calculate_base_damage(&base, &damage) == BATTLE_STATUS_OK);
    CHECK(damage == 46);
    base.defense = 1;
    base.power = 170;
    base.move_effect = GEN1_EXPLODE_EFFECT;
    CHECK(combat_math_calculate_base_damage(&base, &damage) == BATTLE_STATUS_OK);
    CHECK(damage == 999);

    CHECK(combat_math_select_damage_stats(&stats, &selected) == BATTLE_STATUS_OK);
    CHECK(selected.attack == 100 && selected.defense == 80 &&
          selected.power == 80 && selected.level == 50);
    stats.move_type = 20;
    CHECK(combat_math_select_damage_stats(&stats, &selected) == BATTLE_STATUS_OK);
    CHECK(selected.attack == 200 && selected.defense == 160);
    stats.critical = true;
    stats.base_special = 100;
    stats.base_defender_special = 80;
    CHECK(combat_math_select_damage_stats(&stats, &selected) == BATTLE_STATUS_OK);
    CHECK(selected.attack == 100 && selected.defense == 80 &&
          selected.level == 100);

    CHECK(combat_math_apply_type_modifiers(46, (PokemonTypes){20, 20},
                                            (PokemonTypes){22, 22}, 20,
                                            &typed) == BATTLE_STATUS_OK);
    CHECK(typed.damage == 138 && typed.damage_multipliers == 148 && typed.stab);
    CHECK(combat_math_apply_type_modifiers(40, (PokemonTypes){21, 21},
                                            (PokemonTypes){20, 5}, 21,
                                            &typed) == BATTLE_STATUS_OK);
    CHECK(typed.damage == 240);
    CHECK(combat_math_apply_type_modifiers(40, (PokemonTypes){8, 8},
                                            (PokemonTypes){24, 24}, 8,
                                            &typed) == BATTLE_STATUS_OK);
    CHECK(typed.damage == 0 && typed.immune_or_rounded_to_zero);
    CHECK(combat_math_ai_type_effectiveness(20, (PokemonTypes){22, 21}) == 20);
}

static void test_damage_randomization(void) {
    const uint8_t values[] = {0, 179};
    RandomSequence sequence = {values, 2, 0};
    BattleRandomSource random = random_source(&sequence);
    uint16_t damage = 0;

    CHECK(combat_math_randomize_damage(138, &random, &damage) ==
          BATTLE_STATUS_OK);
    CHECK(damage == 117);
    CHECK(sequence.position == 2);
}

static TrainerAiMoveObservation base_move_observation(void) {
    TrainerAiMoveObservation observation = {
        .moves = {{33, 0, 40, 0}, {45, 0x12, 0, 0}, {52, 4, 40, 20},
                  {55, 0, 40, 21}},
        .defender_types = {22, 22},
        .trainer_class = 2,
    };
    return observation;
}

static void test_trainer_move_scoring(void) {
    TrainerAiMoveObservation observation = base_move_observation();
    TrainerAiMoveScores scores = {0};

    CHECK(trainer_ai_score_moves(&observation, &scores) == BATTLE_STATUS_OK);
    CHECK(scores.candidates[0] == 33 && scores.candidates[1] == 45 &&
          scores.candidates[2] == 52 && scores.candidates[3] == 55);

    observation.disabled_move_slot = 1;
    CHECK(trainer_ai_score_moves(&observation, &scores) == BATTLE_STATUS_OK);
    CHECK(scores.candidates[0] == 0 && scores.candidates[1] == 45);

    observation = base_move_observation();
    observation.trainer_class = 4;
    CHECK(trainer_ai_score_moves(&observation, &scores) == BATTLE_STATUS_OK);
    CHECK(scores.candidates[2] == 52);
    CHECK(scores.candidates[0] == 0 && scores.candidates[1] == 0 &&
          scores.candidates[3] == 0);
}

static void test_trainer_move_selection(void) {
    TrainerAiMoveScores scores = {.candidates = {33, 0, 52, 55}};
    const uint8_t values[] = {63, 190};
    RandomSequence sequence = {values, 2, 0};
    BattleRandomSource random = random_source(&sequence);
    TrainerAiDecision decision = {0};

    CHECK(trainer_ai_choose_move(&scores, 0, &random, &decision) ==
          BATTLE_STATUS_OK);
    CHECK(decision.move_slot == 3 && decision.move_id == 55);
    CHECK(sequence.position == 2);
}

static void expect_special(TrainerAiPolicy policy, uint8_t roll, uint16_t hp,
                           uint16_t max_hp, uint8_t status, uint8_t living,
                           TrainerAiAction expected) {
    TrainerAiSpecialObservation observation = {
        GEN1_FIDELITY, policy, roll, hp, max_hp, status, living,
    };
    TrainerAiDecision decision = {0};
    CHECK(trainer_ai_choose_special_action(&observation, &decision) ==
          BATTLE_STATUS_OK);
    CHECK(decision.action == expected);
    CHECK(decision.consumes_action_count ==
          (expected != TRAINER_AI_ACTION_NONE));
}

static void test_special_trainer_policies(void) {
    expect_special(TRAINER_AI_POLICY_JUGGLER, 63, 100, 100, 0, 2,
                   TRAINER_AI_ACTION_SWITCH);
    expect_special(TRAINER_AI_POLICY_BLACKBELT, 31, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_X_ATTACK);
    expect_special(TRAINER_AI_POLICY_GIOVANNI, 63, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_GUARD_SPEC);
    expect_special(TRAINER_AI_POLICY_COOLTRAINER_F, 255, 5, 100, 0, 2,
                   TRAINER_AI_ACTION_USE_HYPER_POTION);
    expect_special(TRAINER_AI_POLICY_COOLTRAINER_F, 255, 15, 100, 0, 2,
                   TRAINER_AI_ACTION_SWITCH);
    expect_special(TRAINER_AI_POLICY_BROCK, 255, 100, 100, 8, 1,
                   TRAINER_AI_ACTION_USE_FULL_HEAL);
    expect_special(TRAINER_AI_POLICY_MISTY, 63, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_X_DEFEND);
    expect_special(TRAINER_AI_POLICY_LT_SURGE, 63, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_X_SPEED);
    expect_special(TRAINER_AI_POLICY_ERIKA, 127, 5, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_SUPER_POTION);
    expect_special(TRAINER_AI_POLICY_KOGA, 63, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_X_ATTACK);
    expect_special(TRAINER_AI_POLICY_BLAINE, 63, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_SUPER_POTION);
    expect_special(TRAINER_AI_POLICY_SABRINA, 63, 5, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_HYPER_POTION);
    expect_special(TRAINER_AI_POLICY_RIVAL2, 31, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_POTION);
    expect_special(TRAINER_AI_POLICY_RIVAL3, 31, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_FULL_RESTORE);
    expect_special(TRAINER_AI_POLICY_LORELEI, 127, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_SUPER_POTION);
    expect_special(TRAINER_AI_POLICY_BRUNO, 63, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_X_DEFEND);
    expect_special(TRAINER_AI_POLICY_AGATHA, 19, 100, 100, 0, 2,
                   TRAINER_AI_ACTION_SWITCH);
    expect_special(TRAINER_AI_POLICY_AGATHA, 20, 20, 100, 0, 2,
                   TRAINER_AI_ACTION_USE_SUPER_POTION);
    expect_special(TRAINER_AI_POLICY_LANCE, 127, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_USE_HYPER_POTION);

    expect_special(TRAINER_AI_POLICY_JUGGLER, 64, 100, 100, 0, 2,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_BLACKBELT, 32, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_GIOVANNI, 64, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_COOLTRAINER_M, 64, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_COOLTRAINER_F, 0, 10, 100, 0, 2,
                   TRAINER_AI_ACTION_SWITCH);
    expect_special(TRAINER_AI_POLICY_COOLTRAINER_F, 0, 20, 100, 0, 2,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_BROCK, 0, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_MISTY, 64, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_LT_SURGE, 64, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_ERIKA, 128, 5, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_KOGA, 64, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_BLAINE, 64, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_SABRINA, 64, 5, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_RIVAL2, 32, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_RIVAL3, 32, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_LORELEI, 128, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_BRUNO, 64, 100, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
    expect_special(TRAINER_AI_POLICY_LANCE, 128, 10, 100, 0, 1,
                   TRAINER_AI_ACTION_NONE);
}

static void test_policy_table_and_mode(void) {
    uint8_t trainer_class;
    for (trainer_class = 1; trainer_class <= GEN1_TRAINER_CLASS_COUNT;
         ++trainer_class) {
        TrainerAiPolicy policy;
        uint8_t maximum_uses;
        CHECK(trainer_ai_policy_for_class(trainer_class, &policy,
                                          &maximum_uses) == BATTLE_STATUS_OK);
        CHECK(maximum_uses >= 1 && maximum_uses <= 5);
    }
    CHECK(trainer_ai_decrement_action_count(3) == 2);

    {
        TrainerAiSpecialObservation observation = {
            ENHANCED, TRAINER_AI_POLICY_BLAINE, 0, 1, 1, 0, 1,
        };
        TrainerAiDecision decision = {0};
        CHECK(trainer_ai_choose_special_action(&observation, &decision) ==
              BATTLE_STATUS_UNSUPPORTED_MODE);
    }
}

static void test_trainer_ai_decision_orchestration(void) {
    TrainerAiObservation observation = {
        .mode = GEN1_FIDELITY,
        .move_observation = {
            .moves = {{33, 0, 40, 0}, {45, 0x12, 0, 0}, {52, 4, 40, 20},
                      {55, 0, 40, 21}},
            .defender_types = {22, 22},
            .trainer_class = 39,
        },
        .current_hp = 100,
        .max_hp = 100,
        .living_party_members = 1,
        .action_count = UINT8_MAX,
    };
    const uint8_t item_values[] = {63};
    RandomSequence item_sequence = {item_values, 1, 0};
    BattleRandomSource item_random = random_source(&item_sequence);
    TrainerAiDecision decision = {0};

    CHECK(trainer_ai_decide(&observation, &item_random, &decision) ==
          BATTLE_STATUS_OK);
    CHECK(decision.action == TRAINER_AI_ACTION_USE_SUPER_POTION);
    CHECK(decision.remaining_action_count == 1);
    CHECK(item_sequence.position == 1);

    observation.move_observation.trainer_class = 1;
    observation.action_count = 3;
    {
        const uint8_t move_values[] = {255, 0};
        RandomSequence move_sequence = {move_values, 2, 0};
        BattleRandomSource move_random = random_source(&move_sequence);
        CHECK(trainer_ai_decide(&observation, &move_random, &decision) ==
              BATTLE_STATUS_OK);
        CHECK(decision.action == TRAINER_AI_ACTION_MOVE);
        CHECK(decision.move_slot == 0 && decision.move_id == 33);
        CHECK(decision.remaining_action_count == 3);
        CHECK(move_sequence.position == 2);
    }

    observation.mode = ENHANCED;
    {
        const uint8_t enhanced_values[] = {0};
        RandomSequence enhanced_sequence = {enhanced_values, 1, 0};
        BattleRandomSource enhanced_random = random_source(&enhanced_sequence);
        CHECK(trainer_ai_decide(&observation, &enhanced_random, &decision) ==
              BATTLE_STATUS_UNSUPPORTED_MODE);
        CHECK(enhanced_sequence.position == 0);
    }
}

static uint8_t rotate_left_three_for_test(uint8_t value) {
    return (uint8_t)((uint8_t)(value << 3U) | (uint8_t)(value >> 5U));
}

static uint8_t rotate_right_one_for_test(uint8_t value) {
    return (uint8_t)((uint8_t)(value >> 1U) | (uint8_t)(value << 7U));
}

static void test_all_random_bytes(void) {
    unsigned int raw;
    for (raw = 0; raw <= UINT8_MAX; ++raw) {
        const uint8_t value = (uint8_t)raw;
        const uint8_t accuracy_values[] = {value};
        RandomSequence accuracy_sequence = {accuracy_values, 1, 0};
        BattleRandomSource accuracy_random = random_source(&accuracy_sequence);
        bool hit = false;
        uint8_t scaled = 0;

        CHECK(combat_math_roll_hit(255, 7, 7, false, &accuracy_random, &hit,
                                   &scaled) == BATTLE_STATUS_OK);
        CHECK(hit == (value < 255U));

        {
            const uint8_t critical_values[] = {value};
            RandomSequence critical_sequence = {critical_values, 1, 0};
            BattleRandomSource critical_random = random_source(&critical_sequence);
            bool critical = false;
            CHECK(combat_math_roll_critical(100, 40, false, false,
                                            &critical_random, &critical) ==
                  BATTLE_STATUS_OK);
            CHECK(critical == (rotate_left_three_for_test(value) < 50U));
        }

        {
            const uint8_t factor = rotate_right_one_for_test(value);
            const uint8_t damage_values[] = {value, 255};
            const size_t expected_consumption = factor < 217U ? 2U : 1U;
            const uint8_t accepted_factor = factor < 217U ? 255U : factor;
            RandomSequence damage_sequence = {damage_values, 2, 0};
            BattleRandomSource damage_random = random_source(&damage_sequence);
            uint16_t damage = 0;
            CHECK(combat_math_randomize_damage(138, &damage_random, &damage) ==
                  BATTLE_STATUS_OK);
            CHECK(damage == (uint16_t)((138U * accepted_factor) / 255U));
            CHECK(damage_sequence.position == expected_consumption);
        }

        {
            TrainerAiMoveScores scores = {.candidates = {33, 45, 52, 55}};
            const uint8_t move_values[] = {value};
            RandomSequence move_sequence = {move_values, 1, 0};
            BattleRandomSource move_random = random_source(&move_sequence);
            TrainerAiDecision decision = {0};
            const uint8_t expected_slot =
                value < 63U ? 0U : value < 127U ? 1U : value < 190U ? 2U : 3U;
            CHECK(trainer_ai_choose_move(&scores, 0, &move_random, &decision) ==
                  BATTLE_STATUS_OK);
            CHECK(decision.move_slot == expected_slot);
        }
    }
}

int main(void) {
    test_accuracy();
    test_critical_hits();
    test_damage();
    test_damage_randomization();
    test_trainer_move_scoring();
    test_trainer_move_selection();
    test_special_trainer_policies();
    test_policy_table_and_mode();
    test_trainer_ai_decision_orchestration();
    test_all_random_bytes();

    if (failures != 0U) {
        fprintf(stderr, "%u C battle checks failed\n", failures);
        return EXIT_FAILURE;
    }
    puts("C battle checks passed");
    return EXIT_SUCCESS;
}
