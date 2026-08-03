CC ?= cc

CPPFLAGS := -Iinclude
BASE_CFLAGS := -std=c17 -Wall -Wextra -Werror -Wconversion -Wsign-conversion -pedantic
OPT_CFLAGS ?= -O2
BUILD_DIR := build
SOURCES := src/common.c src/combat_math.c src/trainer_ai.c
OBJECTS := $(SOURCES:src/%.c=$(BUILD_DIR)/%.o)
TEST_SOURCES := tests/c/test_main.c

.PHONY: all check clean shared tables-check test

all: $(BUILD_DIR)/libpokered_battle.a

check: tables-check test shared

tables-check:
	python3 -m battle_characterization.generate_c_tables --check

shared: $(BUILD_DIR)/libpokered_battle.so

test: $(BUILD_DIR)/battle_c_tests
	ASAN_OPTIONS=detect_leaks=0 $(BUILD_DIR)/battle_c_tests

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/%.o: src/%.c | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(BASE_CFLAGS) $(OPT_CFLAGS) -fPIC -c $< -o $@

$(BUILD_DIR)/libpokered_battle.a: $(OBJECTS)
	$(AR) rcs $@ $^

$(BUILD_DIR)/libpokered_battle.so: $(OBJECTS)
	$(CC) -shared -o $@ $^

$(BUILD_DIR)/battle_c_tests: $(SOURCES) $(TEST_SOURCES) | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(BASE_CFLAGS) -O1 -g \
		-fsanitize=address,undefined -fno-omit-frame-pointer \
		$(SOURCES) $(TEST_SOURCES) -o $@

clean:
	$(RM) -r $(BUILD_DIR)
