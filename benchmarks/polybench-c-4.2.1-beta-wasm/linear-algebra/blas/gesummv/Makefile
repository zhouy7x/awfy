include ../../../config.mk

EXTRA_FLAGS=

gesummv: gesummv.c gesummv.h
	${VERBOSE} ${CC} -o gesummv.html gesummv.c ${CFLAGS} -I. -I../../../utilities ../../../utilities/polybench.c ${EXTRA_FLAGS}

clean:
	@ rm -f gesummv.html gesummv.js gesummv.wasm

