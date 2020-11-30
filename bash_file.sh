# ! / bin / bash
# $ -l mem = 1 G
# $ -l h_rt = 12:00:00
# $ -l killable
# $ - cwd
# $ -q \* @@elves
# $ - pe single 16
# $ -t 1:10:1
for i in {100000000 . . 2100000000 . . 100000000}
do
P1_serial.out $i
P1_pthreads.out $i 2
P1_openmp.out $i 2
P1_pthreads . out $i 4
P1_openmp.out $i 4
P1_pthreads.out $i 8
P1_openmp.out $i 8
P1_pthreads.out $i 16
P1_openmp.out $i 16
done
