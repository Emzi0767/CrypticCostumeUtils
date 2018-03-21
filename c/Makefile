CC=clang-3.9
LD=ld

CFLAGS=-std=c99 -Wall -O2
LDFLAGS=

INCLUDE_PATH=.
LIBRARIES=
DEPENDENCIES = ver.h

OBJ_PATH=obj
OUT_PATH=.
BIN_NAME=ccu

_OBJS = program.o ver.o costume.o pack.o extract.o
OBJS = $(patsubst %,$(OBJ_PATH)/%,$(_OBJS))

$(OBJ_PATH)/%.o: %.c $(DEPENDENCIES)
	@[ -d $(OBJ_PATH) ] || mkdir $(OBJ_PATH)
	@echo " [CC] " $@
	@$(CC) -c -o $@ $< -I$(INCLUDE_PATH) $(CFLAGS)

$(OUT_PATH)/$(BIN_NAME): $(OBJS)
	@[ -d $(OUT_PATH) ] || mkdir $(OUT_PATH)
	@echo " [LD] " $@
	@$(CC) -fuse-ld=$(LD) -o $@ $^ $(LIBRARIES) $(LDFLAGS)

.PHONY: clean

clean: $(OBJS) $(OUT_PATH)/$(BIN_NAME)
	@echo Cleaning up $(OBJ_PATH)
	@rm -rf $(OBJ_PATH)
	@echo Cleaning up $(OUT_PATH)/$(BIN_NAME)
	@rm -rf $(OUT_PATH)/$(BIN_NAME)
