CC = gcc
CFLAGS = -Wall -pthread
LIBS = -lpigpio -lrt

all: adx

adx: adx.o
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

adx.o: adx.c
	$(CC) $(CFLAGS) -c $^ $(LIBS)

clean:
	touch *.o
	rm -rf *.o
clobber:
	touch *.o adx
	rm -rf *.o adx
