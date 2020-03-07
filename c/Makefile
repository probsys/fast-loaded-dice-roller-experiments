all: main.out main.out.opt preprocess.out preprocess.out.opt test
SRC_C = flip.c main.c macros.c readio.c sample.c utils.c
SRC_CPP = main.cpp macros.c readio.c readio.cpp sample.cpp
LIBS = -lgsl -lgslcblas -lm

main.out: $(SRC_C)
	gcc -pg -o main.out $^ $(LIBS)

main.out.opt: $(SRC_C)
	gcc -O3 -Wno-unused-result -o main.out.opt $^ $(LIBS)

main.out.profile.out: $(SRC_C)
	gcc -pg -o main.out.profile.out $^ $(LIBS)

preprocess.out: readio.c preprocess.c
	gcc -o preprocess.out $^ $(LIBS)

preprocess.out.opt: readio.c preprocess.c
	gcc -O3 -Wno-unused-result  -o preprocess.out.opt $^ $(LIBS)

SAMPLERS =alias.exact interval ky.enc rej.binary rej.enc rej.matc rej.table rej.uniform
test: main.out.opt
	for sampler in $(SAMPLERS); do \
		./main.out.opt 1 1000000 $${sampler} d/d.00050.$${sampler}; \
	done

.PHONY:clean
clean:
	rm -rf *.out
