#include "pokered/battle/common.h"

#include <stddef.h>

BattleStatus battle_random_next(BattleRandomSource *source, uint8_t *value) {
    if (source == NULL || value == NULL || source->next_u8 == NULL) {
        return BATTLE_STATUS_INVALID_ARGUMENT;
    }
    if (!source->next_u8(source->context, value)) {
        return BATTLE_STATUS_RNG_EXHAUSTED;
    }
    return BATTLE_STATUS_OK;
}
