include ../../../config.mk

EXTRA_FLAGS=

atax: atax.c atax.h
	${VERBOSE} ${CC} -o atax.html atax.c ${CFLAGS} -I. -I../../../utilities ../../../utilities/polybench.c ${EXTRA_FLAGS}

clean:
	@ rm -f atax.html atax.js atax.wasm

