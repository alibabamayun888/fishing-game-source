dependdir := $(shell ls .depend >/dev/null 2>&1)
ifneq ($(dependdir), .depend)
    dependdir := $(shell touch .depend)
endif

CC=g++
GCC=gcc
#COMP_PARA=-g -Wall -c -D__MULITI_THREAD__ -D__DEBUG__ -DNDEBUG -D_LINUX -D_mt  -DMONGO_HAVE_STDINT \
              -DMONGO_HAVE_UNISTD -DMONGO_USE__INT64 -DMONGO_USE_LONG_LONG_INT -DMONGO_BIG_ENDIAN
COMP_PARA=-g -Wall -c -D__MULITI_THREAD__ -D__DEBUG__ -DNDEBUG -D_LINUX -D_mt #-D_CQ_DEBUG_

BASE_PATH=/home/share/debug
LINK_PARA=-mt -pg

INCS=-I/usr/local/include/hiredis/ -I../../public  -I/usr/local/include -I/usr/include/  -I../  -I$(BASE_PATH)/interface/ 

LIBS= -L/usr/local/lib/  -L$(BASE_PATH)/libs  -lbsoncpp  -lboost_thread -lboost_filesystem -lboost_program_options  -lboost_system  -lnskernel -lnc -lbase -lpthread -lz -lcrypto -lhiredis
CSRCS   = $(wildcard *.c) 
CPPSRCS = $(wildcard *.cpp) 

COBJS   = $(patsubst %.c, %.o, $(CSRCS))
CPPOBJS = $(patsubst %.cpp, $(OBJ_DIR)%.o, $(CPPSRCS))
OBJS = $(CPPOBJS)
 

TARGET=../bin/redistools

all : $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LINK_PARA) -o $@ $^ $(LIBS)

testmongo: testmongo.cpp
	$(CC)  -o $@ $^ $(LIBS) $(INCS)

test: $(TESTOBJS)
	$(CC) $(LINK_PARA) -o test  $^ $(LIBS)
	cp -f $@ ../bin


$(COBJS) : %.o:%.c
	${GCC} ${COMP_PARA} -o $@ $< ${INCS}
	@echo

$(CPPOBJS) : %.o:%.cpp
	${CC} ${COMP_PARA} -o $@ $< $(INCS)
	@echo

#.cpp.o :
#	${CC} ${COMP_PARA} $< ${INCS}

#.c.o :
#	${GCC} ${COMP_PARA} $< ${INCS}

clean :
	@-rm -f $(CPPOBJS) $(COBJS) $(TARGET)

depend:
	gcc -E -c $(CFLAGS) $(INCS) -MM *.c >.depend
	g++ -E -c $(CPPFLAGS) $(INCS) -MM *.cpp >>.depend

include .depend
