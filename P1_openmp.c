#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/resource.h>

/* Global Variables:
-------------------*/
double sum = 0.0;
double elapsedTime;
double st;
pthread_mutex_t mutexsum; // A mutex variable acts like a "lock" protecting access to a shared data resource


long NUM_ITER;    // Will be updated by the terminal
int NUM_THREADS;  // Will be updated by the terminal


/* Function: 
-------------------*/
void *divide(void *myID)
{
	int i;
	int startPos, endPos;
    double local_x, local_sum;
    
    #pragma omp private(myID,theChar,charLoc,local_char_count,startPos,endPos,i,j)
    {
        startPos = ((int) myID) * (NUM_ITER / NUM_THREADS);
        endPos = startPos + (NUM_ITER / NUM_THREADS);
        
        printf("myID = %d startPos = %d endPos = %d \n", (int) myID, startPos, endPos);
	
        // Initailize Local Array
        local_x  = 0.0;
        local_sum = 0.0;

        // Add up our section of the local sum
        for (i = startPos; i < endPos; i++)
        {
		local_x = (i + 0.25)*st;
		local_sum += 4.0/(local_x*local_x+1);
        }

	// sum up the partial sum into the global sum
	#pragma omp critical
	sum += local_sum;
    }
}

/* Main: 
-------------------*/

int main(int argc, char *argv[]) 
{
	int i;
	struct timeval t1, t2;
  	struct rusage ru;
    
    // Default Values
	NUM_THREADS = 1;
	NUM_ITER = 100000000;
    
	if (argc >= 2){
        // Updated Value taken from terminal argumentes
		NUM_ITER = atol(argv[1]);
        NUM_THREADS = atol(argv[2]);
	}

	st  = 1.0 / ( (double) NUM_ITER);
	/* Set the number of threads for the Openmp Enviroment */
    omp_set_num_threads(NUM_THREADS);
    
    // Starting the Division:
	gettimeofday(&t1, NULL);
	printf("DEBUG: starting loop on %s\n", getenv("HOST"));
    
    #pragma omp parallel
    {
        divide(omp_get_thread_num());
    }
	gettimeofday(&t2, NULL);	

	elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0; //sec to ms
	elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0; // us to ms

    getrusage(RUSAGE_SELF, &ru);
    long MEMORY_USAGE = ru.ru_maxrss;   // Memory usage in Kb

	pthread_mutex_destroy(&mutexsum);
	printf("Main: program completed. Exiting.\n");
	printf("DATA, %lf, %ld, %lf, %ld, %ld, OpenMp \n", sum, NUM_ITER, elapsedTime, MEMORY_USAGE, NUM_THREADS);
	pthread_exit(NULL);

	return 0;
}


