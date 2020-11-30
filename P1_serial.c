#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/resource.h>

/* Global Variables:
-------------------*/
long NUM_ITER;
double sum = 0.0;
double x   = 0.0;
double elapsedTime;

/* Function: 
-------------------*/
void divide( )
{
	int i;

	double st  = 1.0 / ( (double) NUM_ITER);

	for (i = 0; i < NUM_ITER; i++)
	{
		x = (i + 0.25)*st;
		sum += 4.0/(x*x+1);
	}
}

/* Main: 
-------------------*/

int main(int argc, char *argv[]) {
	struct timeval t1, t2;
  	struct rusage ru;

	NUM_ITER = 100000000; // Default Value
	if (argc >= 2){
		NUM_ITER = atol(argv[1]);  // Updated Value taken from terminal argumentes
	}

	gettimeofday(&t1, NULL);
	divide();
	gettimeofday(&t2, NULL);	

	elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0; //sec to ms
	elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0; // us to ms

    getrusage(RUSAGE_SELF, &ru);
    long MEMORY_USAGE = ru.ru_maxrss;   // Memory usage in Kb

	printf("DATA, %lf, %ld, %lf, %ld \n", sum, NUM_ITER, elapsedTime, MEMORY_USAGE);

	return 0;
}


