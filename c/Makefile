CFLAGS	:= -Wall

.PHONY: nanotime

nanotime: nanotime.out

nanotime.out: nanotime.c
	@$(CC) $(CFLAGS) $< -o nanotime.out -lm
	@echo Built nanotime.out
