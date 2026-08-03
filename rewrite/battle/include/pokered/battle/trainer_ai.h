#ifndef POKERED_BATTLE_TRAINER_AI_H
#define POKERED_BATTLE_TRAINER_AI_H

#include <stddef.h>

#include "pokered/battle/combat_math.h"

enum {
    TRAINER_AI_MOVE_SLOTS = 4,
    GEN1_TRAINER_CLASS_COUNT = 47,
    GEN1_PARTY_CAPACITY = 6
};

typedef struct {
    uint8_t id;
    uint8_t effect;
    uint8_t power;
    uint8_t type;
} TrainerAiMove;

typedef struct {
    TrainerAiMove moves[TRAINER_AI_MOVE_SLOTS];
    PokemonTypes defender_types;
    uint8_t defender_status;
    uint8_t disabled_move_slot;
    uint8_t layer2_encouragement;
    uint8_t trainer_class;
} TrainerAiMoveObservation;

typedef struct {
    uint8_t scores[TRAINER_AI_MOVE_SLOTS];
    uint8_t candidates[TRAINER_AI_MOVE_SLOTS];
} TrainerAiMoveScores;

typedef enum {
    TRAINER_AI_POLICY_GENERIC = 0,
    TRAINER_AI_POLICY_JUGGLER,
    TRAINER_AI_POLICY_BLACKBELT,
    TRAINER_AI_POLICY_GIOVANNI,
    TRAINER_AI_POLICY_COOLTRAINER_M,
    TRAINER_AI_POLICY_COOLTRAINER_F,
    TRAINER_AI_POLICY_BROCK,
    TRAINER_AI_POLICY_MISTY,
    TRAINER_AI_POLICY_LT_SURGE,
    TRAINER_AI_POLICY_ERIKA,
    TRAINER_AI_POLICY_KOGA,
    TRAINER_AI_POLICY_BLAINE,
    TRAINER_AI_POLICY_SABRINA,
    TRAINER_AI_POLICY_RIVAL2,
    TRAINER_AI_POLICY_RIVAL3,
    TRAINER_AI_POLICY_LORELEI,
    TRAINER_AI_POLICY_BRUNO,
    TRAINER_AI_POLICY_AGATHA,
    TRAINER_AI_POLICY_LANCE
} TrainerAiPolicy;

typedef enum {
    TRAINER_AI_ACTION_NONE = 0,
    TRAINER_AI_ACTION_MOVE,
    TRAINER_AI_ACTION_SWITCH,
    TRAINER_AI_ACTION_USE_POTION,
    TRAINER_AI_ACTION_USE_SUPER_POTION,
    TRAINER_AI_ACTION_USE_HYPER_POTION,
    TRAINER_AI_ACTION_USE_FULL_RESTORE,
    TRAINER_AI_ACTION_USE_FULL_HEAL,
    TRAINER_AI_ACTION_USE_X_ATTACK,
    TRAINER_AI_ACTION_USE_X_DEFEND,
    TRAINER_AI_ACTION_USE_X_SPEED,
    TRAINER_AI_ACTION_USE_GUARD_SPEC
} TrainerAiAction;

typedef struct {
    BehaviorMode mode;
    TrainerAiPolicy policy;
    uint8_t random_roll;
    uint16_t current_hp;
    uint16_t max_hp;
    uint8_t status;
    uint8_t living_party_members;
} TrainerAiSpecialObservation;

typedef struct {
    TrainerAiAction action;
    uint8_t move_slot;
    uint8_t move_id;
    bool consumes_action_count;
    uint8_t remaining_action_count;
} TrainerAiDecision;

typedef struct {
    BehaviorMode mode;
    TrainerAiMoveObservation move_observation;
    uint16_t current_hp;
    uint16_t max_hp;
    uint8_t own_status;
    uint8_t living_party_members;
    uint8_t action_count;
} TrainerAiObservation;

BattleStatus trainer_ai_score_moves(const TrainerAiMoveObservation *observation,
                                    TrainerAiMoveScores *result);

BattleStatus trainer_ai_choose_move(const TrainerAiMoveScores *scores,
                                    uint8_t disabled_move_slot,
                                    BattleRandomSource *random,
                                    TrainerAiDecision *decision);

BattleStatus trainer_ai_choose_special_action(
    const TrainerAiSpecialObservation *observation,
    TrainerAiDecision *decision);

BattleStatus trainer_ai_policy_for_class(uint8_t trainer_class,
                                         TrainerAiPolicy *policy,
                                         uint8_t *maximum_uses);

BattleStatus trainer_ai_decide(const TrainerAiObservation *observation,
                               BattleRandomSource *random,
                               TrainerAiDecision *decision);

uint8_t trainer_ai_decrement_action_count(uint8_t action_count);

#endif
