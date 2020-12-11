# Project 1: C-Language pthreads-vs-OpenMp
The current repository will analyze the performance of two parallel execution models which are pthreads and OpenMp.
The two models are implemented to solve a simple equation shown below,
                x = (i + 0.25)* (1/Max_Num_ITE)                
where i represents the loop iteration starting from 0 and going to the maximum number of iterations (Known as Max_Num_ITE), and then sums up all the values of x.

Performance analysis of the two parallel execution models, was carried out with a range of values for Max_Num_ITE starting with of 100 million and stopping at 2.1 billion. As for the number of cores each parallelization model implemented are 2, 4, 8, and 16 cores.

The results are shown in the report.
