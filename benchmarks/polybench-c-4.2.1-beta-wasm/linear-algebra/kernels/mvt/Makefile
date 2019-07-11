include ../../../config.mk

EXTRA_FLAGS=

mvt: mvt.c mvt.h
	${VERBOSE} ${CC} -o mvt.html mvt.c ${CFLAGS} -I. -I../../../utilities ../../../utilities/polybench.c ${EXTRA_FLAGS}

clean:
	@ rm -f mvt.html mvt.js mvt.wasm

