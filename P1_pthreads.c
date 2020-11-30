#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/resource.h>

/* Global Variables:
-------------------*/
long NUM_ITER;
double sum = 0.0;
double elapsedTime;
double st;
pthread_mutex_t mutexsum; // A mutex variable acts like a "lock" protecting access to a shared data resource

int NUM_THREADS;  // Will be updated by the enviromental variables of Beocat

/* Function: 
-------------------*/
void *divide(void *myID)
{
	int i;
	int startPos = ((int) myID) * (NUM_ITER / NUM_THREADS);
	int endPos = startPos + (NUM_ITER / NUM_THREADS);

	printf("myID = %d startPos = %d endPos = %d \n", (int) myID, startPos, endPos);
	
	double local_x 	 = 0.0;
	double local_sum = 0.0; 

	// Add up our section of the local sum
	for (i = startPos; i < endPos; i++)
	{
		local_x = (i + 0.25)*st;
		local_sum += 4.0/(local_x*local_x+1);
	}

	// sum up the partial sum into the global sum
	pthread_mutex_lock (&mutexsum);
	sum += local_sum;
	pthread_mutex_unlock (&mutexsum);
	pthread_exit(NULL);
}

/* Main: 
-------------------*/

int main(int argc, char *argv[]) {
	int i,rc;	
	void *status;
	struct timeval t1, t2;
  	struct rusage ru;

	//NUM_THREADS = getenv("NSLOTS");
	NUM_THREADS = 4;
	NUM_ITER = 100000000; // Default Value
	if (argc >= 2){
		NUM_ITER = atol(argv[1]);  // Updated Value taken from terminal argumentes
	}

	st  = 1.0 / ( (double) NUM_ITER);
	/* Create, initialize and set thread detached attribute */
	pthread_t threads[NUM_THREADS]; // creates an array of pthread_t
	pthread_attr_t attr;
	pthread_attr_init(&attr); /* initializes the thread attributes object
	pointed to by attr with default attribute values */
	pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE); /*sets the detach state attribute of the thread attributes object to joinable*/
	/* joinable means, we can wait for its completion.  A thread may have already terminated before we join it. As a result, the Pthreads system must retain some information when a thread is joinable: namely, at least the thread ID and the returned value[1]. Indeed this information is needed for joining the thread. and all other threads using the function pthread_join() */

	// Starting the Division:
	gettimeofday(&t1, NULL);
	printf("DEBUG: starting loop on %s\n", getenv("HOST"));
	for (i = 0; i < NUM_THREADS; i++ ) {
		// starts a new thread in the calling proces
	    rc = pthread_create(&threads[i], &attr, divide, (void *)i); 
		/*
		The pthread_create() funchwtion starts a new thread in the calling
       	process. The new thread starts execution by invoking 
       	start_routine(); arg is passed as the sole argument of
       	start_routine()
		*/
	    if (rc) {
	    	printf("ERROR; return code from pthread_create() is %d\n", rc);
			exit(-1);
	    }
	}
	/* Free attribute and wait for the other threads */
	pthread_attr_destroy(&attr); // destroy a thread attributes object. 
	for(i=0; i<NUM_THREADS; i++) {
	     rc = pthread_join(threads[i], &status);
	     if (rc) {
		   printf("ERROR; return code from pthread_join() is %d\n", rc);
		   exit(-1);
	     }
	}
	gettimeofday(&t2, NULL);	

	elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0; //sec to ms
	elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0; // us to ms

    getrusage(RUSAGE_SELF, &ru);
    long MEMORY_USAGE = ru.ru_maxrss;   // Memory usage in Kb

	pthread_mutex_destroy(&mutexsum);
	printf("Main: program completed. Exiting.\n");
	printf("DATA, %lf, %ld, %lf, %ld \n", sum, NUM_ITER, elapsedTime, MEMORY_USAGE);
	pthread_exit(NULL);

	return 0;
}


