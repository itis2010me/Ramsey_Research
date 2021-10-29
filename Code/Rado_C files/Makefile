all: RadoCG Rado_sub

CC = g++
CFLAGS = -std=c++11 -Wall -Werror

RadoCG: RadoCG.cpp 
	$(CC) -o $@ $(CFLAGS) $^

Rado_sub: Rado_sub.cpp
	$(CC) -o $@ $(CFLAGS) $^

clean:
	rm -f *.o
	rm -f RadoCG
	rm -f Rado_sub