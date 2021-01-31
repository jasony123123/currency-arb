all: neg_cycles
	./neg_cycles
neg_cycles: neg_cycles.cpp
	g++ -std=c++11 -Wall -Wextra neg_cycles.cpp -o neg_cycles
