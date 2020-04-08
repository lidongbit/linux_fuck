/*
NAME
       opendir, fdopendir - open a directory

SYNOPSIS
       #include <sys/types.h>
       #include <dirent.h>

       DIR *opendir(const char *name);
       DIR *fdopendir(int fd);

DESCRIPTION
       The opendir() function opens a directory stream corresponding to the directory name, and returns
       a pointer to the directory stream.  The stream is positioned at the first entry  in  the  direc‐
       tory.

       The  fdopendir() is like opendir(), but returns a directory stream for the directory referred to
       by the open file descriptor fd.  After a successful call to fdopendir(), fd is  used  internally
       by the implementation, and should not otherwise be used by the application.

RETURN VALUE
       The  opendir()  and  fdopendir()  functions return a pointer to the directory stream.  On error,
       NULL is returned, and errno is set appropriately.
*/

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
int main(int argc, char *argv[])
{
    DIR *dp;
    struct dirent *dirp;
    if(argc!=2)
        printf("usage: myls directory_name!\n");
    if((dp=opendir(argv[1]))==NULL)
        printf("can't open %s!\n", argv[1]);
    while((dirp=readdir(dp))!=NULL)
        printf("%s\n", dirp->d_name);
    closedir(dp);
    exit(0);
}