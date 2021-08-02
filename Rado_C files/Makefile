all: RadoCG

CC = g++
CFLAGS = -std=c++11 -Wall -Werror

RadoCG: main.cpp 
	$(CC) -o $@ $(CFLAGS) $^

clean:
	rm -f *.o
	rm -f RadoCG