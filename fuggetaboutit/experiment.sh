#!/bin/bash

TIME=3600
# assuming average 14 hops per link so arrivalRates is for each hop up to middle of the network
# which are assumed to be core routers
arrivalRates=( 28.45 142.25 711.25 3556.25 17781.25 88906.25 444531.25 )
deletionRates=( 10 20 30 40 50 )
bfsizes=( 128 192 256 )
bfhashes=( 3 4 5 6 7 8 )
RANDOMSIZE=100

for ar in "${arrivalRates[@]}"
do
    for dr in "${deletionRates[@]}"
    do
        for bfsize in "${bfsizes[@]}"
        do
            for bfhash in "${bfhashes[@]}"
            do
                echo python decayer.py $TIME $bfsize $bfhash 1 $ar $dr $RANDOMSIZE
                python decayer.py $TIME $bfsize $bfhash 1 $ar $dr $RANDOMSIZE > out_$TIME_$bfsize_$bfhash_1_$ar_$dr_$RANDOMSIZE.out
            done    
        done
    done
done

