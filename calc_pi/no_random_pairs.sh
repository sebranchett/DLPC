for pairs in 10 100 1000 10000 100000 1000000
do
    mpiexec -hostfile myhostfile$ranks -np 1 python3 blog/calc_pi/calculate_pi.py $pairs > r1p"$pairs".out
    mv pi_estimate_10*_points.csv r1p"$pairs".csv
    mv pi_estimate_10*_points.png r1p"$pairs".png
    tail -n 3 r1p"$pairs".out
    sleep 2
done
