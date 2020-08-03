for ranks in {1..32}
do
    mpiexec -hostfile myhostfile -np $ranks python3 blog/calc_pi/calculate_pi.py 1000000 > r"$ranks"p1000000.out
    mv pi_estimate_10*_points.csv r"$ranks"p1000000.csv
    mv pi_estimate_10*_points.png r"$ranks"p1000000.png
    tail -n 3 r"$ranks"p1000000.out
    sleep 2
done
