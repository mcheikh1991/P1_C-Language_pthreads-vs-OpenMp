import matplotlib.pyplot as plt
import numpy as np
import re
import os
from os import listdir, remove
from os.path import isfile, join
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['figure.figsize'] = 7.5, 7
rcParams['font.size'] =  12
rcParams['font.family'] = 'serif'


Loc = os.getcwd() 

def sort(main,other):
	main , other = zip(*sorted(zip(main,other)))
	main = np.array(main)
	other = np.array(other)
	return main, other

#---------------------------------------------------------
# Ploting the Data  
#---------------------------------------------------------

Col = ['k','b','g','m','r','c','y','#92C6FF','#E24A33', '#001C7F', '.15', '0.40']
Mar = [".","s","o","d","P","v","^","<",">","1","2","3","4","8","+","p","P","*"]
Lin = ['-','.-',':']

i = 0
j = 0
g = 0
FilesKilled = []
FilesWorking = []
RunNumber = []

Ser_Num_Iter   		=  []
Ser_Sum				=  np.array([])
Ser_ElapsedTime 	=  np.array([])
Ser_MemoryUsage 	=  np.array([])
Ser_Average_Ratio 	=  np.array([])

Pth_Num_Thread 	    =  []
Pth_Sum				=  []
Pth_Num_Iter   		=  []
Pth_ElapsedTime 	=  []
Pth_MemoryUsage 	=  []
Pth_Average_Ratio 	=  []

OMp_Num_Thread 	    =  []
OMp_Num_Iter   		=  []
OMp_Sum				=  []
OMp_ElapsedTime 	=  []
OMp_MemoryUsage 	=  []
OMp_Average_Ratio 	=  []

Data_Loc = Loc +'/Data/'

# Gets all Files
AllFiles = [f for f in listdir(Data_Loc) if isfile(join(Data_Loc, f))]

for z in ['sh.e','sh.po','sh.pe']:
	ErrorFiles = [File for File in AllFiles if re.findall(z,File) != []]
	for File in ErrorFiles: 
		print 'Error File for deletion:',File
		remove(Data_Loc+File)

# Keeps only the output files ".o"
AllFiles = [File for File in AllFiles if re.findall('sh.o',File) != []]
for File in AllFiles:
	Data_File = open(Data_Loc+File,'r')
	Data_File = Data_File.read()

	try:
		AllData = re.findall(r'DATA, [^\n]*',Data_File)
		for Data in AllData:
			Data = Data.replace(' ','')
			Data = Data.split(',')
			Sum = float (Data[1])		 # Final Answer 
			IT  = long  (Data[2]) 		 # Number of Iterations
			ET  = float (Data[3]) / 1000   # Elapsed Time (s)
			MU  = long  (Data[4]) / 1024.0 # Memory Usafe (Mb)

			# Serial:
			#--------------
			if len(Data) == 5: 
				if Ser_Num_Iter.count(IT) == 0:

					Ser_Num_Iter.append(IT)
					Ser_ElapsedTime = np.append(Ser_ElapsedTime,ET) 				
					Ser_MemoryUsage = np.append(Ser_MemoryUsage,MU) 	# Mb 
					Ser_Average_Ratio = np.append(Ser_Average_Ratio,1)
					Ser_Sum = np.append(Ser_Sum,Sum) 
				else:
					Index = Ser_Num_Iter.index(IT)
					Ser_ElapsedTime[Index] += ET 				
					Ser_MemoryUsage[Index] += MU 
					Ser_Average_Ratio[Index] += 1
					Ser_Sum[Index] += Sum

			# Pthread:
			#----------------
			elif len(Data) == 6: 
				TR = long (Data[5])  # Number of Threads
				if Pth_Num_Thread.count(TR) == 0: 
					Pth_Num_Thread.append(TR)
					Pth_Num_Iter.append([])
					Pth_ElapsedTime.append(np.array([]))
					Pth_MemoryUsage.append(np.array([]))
					Pth_Average_Ratio.append(np.array([]))
					Pth_Sum.append(np.array([]))
				
				Index_T = Pth_Num_Thread.index(TR)
				Pth_Num_Iter_Local = Pth_Num_Iter[Index_T]
				Pth_ElapsedTime_Local = Pth_ElapsedTime[Index_T]
				Pth_MemoryUsage_Local = Pth_MemoryUsage[Index_T]
				Pth_Average_Ratio_Local = Pth_Average_Ratio[Index_T]
				Pth_Sum_Local			= Pth_Sum[Index_T]

				if Pth_Num_Iter_Local.count(IT) == 0:
					Pth_Num_Iter_Local.append(IT)	
					Pth_ElapsedTime_Local = np.append(Pth_ElapsedTime_Local,ET)
					Pth_MemoryUsage_Local = np.append(Pth_MemoryUsage_Local,MU) 	
					Pth_Average_Ratio_Local = np.append(Pth_Average_Ratio_Local,1)
					Pth_Sum_Local = np.append(Pth_Sum_Local,Sum)
				else:
					Index_I = Pth_Num_Iter_Local.index(IT)
					Pth_ElapsedTime_Local[Index_I]   += ET 				
					Pth_MemoryUsage_Local[Index_I]   += MU 
					Pth_Average_Ratio_Local[Index_I] += 1
					Pth_Sum_Local[Index_I] += Sum

				Pth_Num_Iter[Index_T]     = Pth_Num_Iter_Local
				Pth_ElapsedTime[Index_T]  = Pth_ElapsedTime_Local
				Pth_MemoryUsage[Index_T]  = Pth_MemoryUsage_Local
				Pth_Average_Ratio[Index_T]= Pth_Average_Ratio_Local
				Pth_Sum[Index_T]	      = Pth_Sum_Local

			# OpenMp:
			#----------------
			elif len(Data) == 7 and Data[6]=='OpenMp': 
				TR = long (Data[5])  # Number of Threads
				if OMp_Num_Thread.count(TR) == 0: 
					OMp_Num_Thread.append(TR)
					OMp_Num_Iter.append([])
					OMp_ElapsedTime.append(np.array([]))
					OMp_MemoryUsage.append(np.array([]))
					OMp_Average_Ratio.append(np.array([]))
					OMp_Sum.append(np.array([]))
				
				Index_T = OMp_Num_Thread.index(TR)
				OMp_Num_Iter_Local = OMp_Num_Iter[Index_T]
				OMp_ElapsedTime_Local = OMp_ElapsedTime[Index_T]
				OMp_MemoryUsage_Local = OMp_MemoryUsage[Index_T]
				OMp_Average_Ratio_Local = OMp_Average_Ratio[Index_T]
				OMp_Sum_Local			= OMp_Sum[Index_T]

				if OMp_Num_Iter_Local.count(IT) == 0:
					OMp_Num_Iter_Local.append(IT)	
					OMp_ElapsedTime_Local = np.append(OMp_ElapsedTime_Local,ET)
					OMp_MemoryUsage_Local = np.append(OMp_MemoryUsage_Local,MU) 	
					OMp_Average_Ratio_Local = np.append(OMp_Average_Ratio_Local,1)
					OMp_Sum_Local = np.append(OMp_Sum_Local,Sum)
				else:
					Index_I = OMp_Num_Iter_Local.index(IT)
					OMp_ElapsedTime_Local[Index_I]   += ET 				
					OMp_MemoryUsage_Local[Index_I]   += MU 
					OMp_Average_Ratio_Local[Index_I] += 1
					OMp_Sum_Local[Index_I] += Sum

				OMp_Num_Iter[Index_T]     = OMp_Num_Iter_Local
				OMp_ElapsedTime[Index_T]  = OMp_ElapsedTime_Local
				OMp_MemoryUsage[Index_T]  = OMp_MemoryUsage_Local
				OMp_Average_Ratio[Index_T]= OMp_Average_Ratio_Local
				OMp_Sum[Index_T]	      = OMp_Sum_Local

			else:
				print "Error in reading Data:",Data

		FilesWorking.append(File)
	except:
		FilesKilled.append(File)
		print 'Killed File:',File
		#remove(Data_Loc+File)

# Averaging The Data
#--------------------
Ser_ElapsedTime = Ser_ElapsedTime/Ser_Average_Ratio
Ser_MemoryUsage = Ser_MemoryUsage/Ser_Average_Ratio
Ser_Sum = Ser_Sum/ Ser_Average_Ratio

for i in range(len(Pth_Num_Thread)):
	Pth_ElapsedTime[i] = Pth_ElapsedTime[i]/Pth_Average_Ratio[i]
	Pth_MemoryUsage[i] = Pth_MemoryUsage[i]/Pth_Average_Ratio[i]
	Pth_Sum[i] = Pth_Sum[i]/Pth_Average_Ratio[i]

for i in range(len(OMp_Num_Thread)):
	OMp_ElapsedTime[i] = OMp_ElapsedTime[i]/OMp_Average_Ratio[i]
	OMp_MemoryUsage[i] = OMp_MemoryUsage[i]/OMp_Average_Ratio[i]
	OMp_Sum[i] = OMp_Sum[i]/OMp_Average_Ratio[i]

# Printing The Results:
#----------------------
print '\n%2s %5s %9s %7s %11s %9s %9s %9s' % ('n', 'Ratio', 'Num_Iter', 'Sum', 'Time [s]', 'Memory [Mb]', 'Threads', 'Type')

for I in range(len(Ser_Average_Ratio)):
	print '%2i %3.0f %11i %12.2f %5.3f %3.4f %5s %9s'%(I,Ser_Average_Ratio[I],Ser_Num_Iter[I],Ser_Sum[I],Ser_ElapsedTime[I],Ser_MemoryUsage[I],'----','Serial')

print "-----------------------------"
print '\n%2s %5s %9s %7s %11s %9s %9s %9s' % ('n', 'Ratio', 'Num_Iter', 'Sum', 'Time [s]', 'Memory [Mb]', 'Threads', 'Type')
for J in range(len(Pth_Num_Thread)):
	for I in range(len(Pth_Average_Ratio[J])):
		print '%2i %3.0f %11i %12.2f %5.3f %3.4f %5i %9s'%(I,Pth_Average_Ratio[J][I],Pth_Num_Iter[J][I],Pth_Sum[J][I],Pth_ElapsedTime[J][I],Pth_MemoryUsage[J][I],Pth_Num_Thread[J],'Pthread')
	print "-----------------------------"

print '\n%2s %5s %9s %7s %11s %9s %9s %9s' % ('n', 'Ratio', 'Num_Iter', 'Sum', 'Time [s]', 'Memory [Mb]', 'Threads', 'Type')
for J in range(len(OMp_Num_Thread)):
	for I in range(len(OMp_Average_Ratio[J])):
		print '%2i %3.0f %11i %12.2f %5.3f %3.4f %5i %9s'%(I,OMp_Average_Ratio[J][I],OMp_Num_Iter[J][I],OMp_Sum[J][I],OMp_ElapsedTime[J][I],OMp_MemoryUsage[J][I],OMp_Num_Thread[J],'OpenMp')
	print "-----------------------------"


# Plotting Data:
#---------------
i = 0
plt.figure(1)
plt.plot(Ser_Num_Iter,Ser_ElapsedTime,color=Col[i],marker=Mar[i],label='Serial')
for J in range(len(Pth_Num_Thread)):
	plt.plot(Pth_Num_Iter[J],Pth_ElapsedTime[J],color=Col[i+1+J], marker=Mar[i+1+J] ,label='pthread %i'%(Pth_Num_Thread[J]) )

for K in range(len(OMp_Num_Thread)):
	plt.plot(OMp_Num_Iter[K],OMp_ElapsedTime[K],color=Col[i+2+J+K],marker=Mar[i+2+J+K],label='OpenMp %i'%(OMp_Num_Thread[K]) )

i = 0
plt.figure(2)
plt.plot(Ser_Num_Iter,Ser_MemoryUsage,color=Col[i],marker=Mar[i],label='Serial')
for J in range(len(Pth_Num_Thread)):
	plt.plot(Pth_Num_Iter[J],Pth_MemoryUsage[J],color=Col[i+1+J],marker=Mar[i+1+J],label='pthread %i'%(Pth_Num_Thread[J]) )

for K in range(len(OMp_Num_Thread)):
	plt.plot(OMp_Num_Iter[K],OMp_MemoryUsage[K],color=Col[i+2+J+K],marker=Mar[i+2+J+K] ,label='OpenMp %i'%(OMp_Num_Thread[K]) )

i = 0
plt.figure(3)
plt.plot(Ser_Num_Iter,Ser_Sum,color=Col[i],marker=Mar[i],label='Serial')

for J in range(len(Pth_Num_Thread)):
	plt.plot(Pth_Num_Iter[J],Pth_Sum[J],color=Col[i+1+J],marker=Mar[i+1+J],label='pthread %i'%(Pth_Num_Thread[J]) )

for K in range(len(OMp_Num_Thread)):
	plt.plot(OMp_Num_Iter[K],OMp_Sum[K],color=Col[i+2+J+K],marker=Mar[i+2+J+K],label='OpenMp %i'%(OMp_Num_Thread[K]) )


plt.figure(1)
plt.xlabel('Number of Iteraions')
plt.ylabel('Time ($s$)')
plt.xlim([0,2.1e9])
#plt.plot([0,5e9],[25000,25000],'g--')
#plt.ylim([0,np.max(ElapsedTime)])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17),
          ncol=3, fancybox=True, shadow=False)
plt.savefig('Num_Iteration_Vs_Time.png')
plt.close()

plt.figure(2)
plt.xlabel('Number of Iteraions')
plt.ylabel('Memory Usage ($Mb$)')
plt.xlim([0,2.1e9])
plt.ylim([0,1.7])
#plt.plot([0,5e9],[25000,25000],'g--')
#plt.ylim([0,np.max(ElapsedTime)])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17),
          ncol=3, fancybox=True, shadow=False)
plt.savefig('Memory_Vs_Num_Iteratione.png')
plt.close()

plt.figure(3)
plt.xlabel('Number of Iteraions')
plt.ylabel('Final Sum')
plt.xlim([0,2.1e9])
plt.ylim([0,8e9])
#plt.plot([0,5e9],[25000,25000],'g--')
#plt.ylim([0,np.max(ElapsedTime)])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.17),
          ncol=3, fancybox=True, shadow=False)
plt.savefig('Sum_Vs_Num_Iteration.png')
plt.close()


#------------------------------------------------------
# Performance Comparison:
#------------------------------------------------------


Ser_Num_Iter[:20]
Ser_ElapsedTime[:20]

Pth_Performance = []
OMp_Performance = []
for J in range(len(Pth_Num_Thread)):
	Pth_Performance.append(np.average(Ser_ElapsedTime[:20]/Pth_ElapsedTime[J][:20]*100))
	OMp_Performance.append(np.average(Ser_ElapsedTime[:20]/OMp_ElapsedTime[J][:20]*100))

xxx = OMp_Performance[3]
OMp_Performance[3] = OMp_Performance[2]
OMp_Performance[2] = xxx



plt.figure(4)

fig, ax = plt.subplots()
opacity = 0.7
error_config = {'ecolor': '0.3'}
width = 0.35

rects1 = ax.bar([0.35], [100], width, color='r', alpha=opacity,
                 error_kw=error_config)
rects2 = ax.bar(np.arange(1,5), Pth_Performance, width, color='b', alpha=opacity,
                 error_kw=error_config)
rects3 = ax.bar(np.arange(1,5)+width, OMp_Performance, width, color='g', alpha=opacity,
                 error_kw=error_config)



# add some text for labels, title and axes ticks
ax.set_ylabel('Performance Speed Up (%)')
ax.set_title('Performance Analysis')
ax.set_xticks([0.35, 1.175, 2.175, 3.175,4.175])
ax.set_xticklabels(('Serial', '2 Cores', '4 Cores', '8 Cores', '16 Cores'))

'''
PLT = ax.plot([0.825,1.525],[200,200],'m:')
PLT = ax.plot([1.825,2.525],[400,400],'m:')
PLT = ax.plot([2.825,3.525],[800,800],'m:')
PLT = ax.plot([3.825,4.525],[1600,1600],'m:')
'''

ax.legend((rects2[0], rects3[0]), ('pthreads', 'OpenMp'))

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height+30,
                '%d%s' % (int(height),'%'),ha='center', va='bottom',size='smaller',color='k')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.ylim([0,1300])
ax.legend(loc='upper left')


plt.savefig('Performance.png')
plt.close()



plt.figure(5)

rcParams['font.size'] =  10
Pth_Performance_Array = []
OMp_Performance_Array = []
for J in range(len(Pth_Num_Thread)):
	Pth_Performance_Array.append((Ser_ElapsedTime[:20]/Pth_ElapsedTime[J][:20]*100))
	OMp_Performance_Array.append((Ser_ElapsedTime[:20]/OMp_ElapsedTime[J][:20]*100))

xxx = OMp_Performance_Array[3]
OMp_Performance_Array[3] = OMp_Performance_Array[2]
OMp_Performance_Array[2] = xxx


i = 0
J = 0
K = 0
for J in range(len(Pth_Num_Thread)):
	plt.subplot(2,2,J+1)
	plt.plot(Pth_Num_Iter[J][:20],Pth_Performance_Array[J],'b-o' ,label='pthread',alpha=opacity,)


for K in range(len(OMp_Num_Thread)):
	plt.subplot(2,2,K+1)
	plt.plot(OMp_Num_Iter[K][:20],OMp_Performance_Array[K],'g-s',label='OpenMp',alpha=opacity,)
	plt.xlabel('Number of Iteraions')
	plt.plot([0.1e9,2.1e9],[Pth_Num_Thread[K]*100,Pth_Num_Thread[K]*100],'k:',label = "Amdahl's Law")

	if K == 2 or K == 0:
		plt.ylabel('Performance Speed Up (%)')

	if K==0:
		plt.text(1.8e9, 119, '2 Cores',ha='center', va='bottom',size='larger',color='r')
	elif K==1:
		plt.text(1.8e9, 133, '4 Cores',ha='center', va='bottom',size='larger',color='r')
	elif K==2:
		plt.text(1.8e9, 346.5, '8 Cores',ha='center', va='bottom',size='larger',color='r')
	elif K==3:
		plt.text(1.75e9, 340, '16 Cores',ha='center', va='bottom',size='larger',color='r')
	

plt.xlim([0,2.1e9])
plt.legend(loc='upper center', bbox_to_anchor=(0, 2.4),
          ncol=3, fancybox=True, shadow=False)
plt.savefig('Num_Iteration_Vs_Performance.png')
plt.close()



















