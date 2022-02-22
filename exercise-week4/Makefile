CXX = gcc
CXX-FLAGS = -g

all: caching vertical horizontal

.PHONY=bw caching

caching: caching.c
	$(CXX) $(CXX-FLAGS) -O0 -o caching-0 caching.c
	$(CXX) $(CXX-FLAGS) -O3 -o caching-3 caching.c

vertical: vertical.c
	$(CXX) $(CXX-FLAGS) -O0 -o vertical-0 vertical.c
	$(CXX) $(CXX-FLAGS) -O3 -o vertical-3 vertical.c

horizontal: horizontal.c
	$(CXX) $(CXX-FLAGS) -O0 -o horizontal-0 horizontal.c
	$(CXX) $(CXX-FLAGS) -O3 -o horizontal-3 horizontal.c