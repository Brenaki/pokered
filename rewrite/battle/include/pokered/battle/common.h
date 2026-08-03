#ifndef POKERED_BATTLE_COMMON_H
#define POKERED_BATTLE_COMMON_H

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    GEN1_FIDELITY = 0,
    ENHANCED = 1
} BehaviorMode;

typedef enum {
    BATTLE_STATUS_OK = 0,
    BATTLE_STATUS_INVALID_ARGUMENT,
    BATTLE_STATUS_RNG_EXHAUSTED,
    BATTLE_STATUS_UNSUPPORTED_MODE
} BattleStatus;

typedef bool (*BattleRandomNext)(void *context, uint8_t *value);

typedef struct {
    BattleRandomNext next_u8;
    void *context;
} BattleRandomSource;

BattleStatus battle_random_next(BattleRandomSource *source, uint8_t *value);

#endif
