#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {
	char cmd[256];
	char options[256];
	options[0] = '\0';
	
	for (int i = 1; i < argc; i++) {
		strcat(options, argv[i]);
	}

	sprintf(cmd, "python C:\\Anaconda\\Lib\\site-packages\\PyQt4\\uic\\pyuic.py %s", options);
	system(cmd);
	return 0;
}