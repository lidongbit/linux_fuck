#include<stdio.h>
#include<string.h>
#include<errno.h>
#include<sys/types.h>
int main(int argc, char* argv[])
{
    fprintf(stderr, "EACCES: %s\n", strerror(EACCES));
    errno = ENOENT;
    perror(argv[0]);
    exit(0);
}