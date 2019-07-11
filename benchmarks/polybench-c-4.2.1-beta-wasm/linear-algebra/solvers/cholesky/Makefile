include ../../../config.mk

EXTRA_FLAGS=-lm

cholesky: cholesky.c cholesky.h
	${VERBOSE} ${CC} -o cholesky.html cholesky.c ${CFLAGS} -I. -I../../../utilities ../../../utilities/polybench.c ${EXTRA_FLAGS}

clean:
	@ rm -f cholesky.html cholesky.js cholesky.wasm

