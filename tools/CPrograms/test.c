#include <stdio.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(int argc, char *argv[])
{
	int fd;
	char *f = malloc(10);
	f=malloc(100);

	fd = open(argv[0], O_RDONLY);
	return 0;
}
