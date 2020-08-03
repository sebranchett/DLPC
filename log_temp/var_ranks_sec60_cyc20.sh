for ranks in {1..32}
do
    cd logs
    rm *
    bash ../create_logs.sh &
    cd ..
    mpiexec -hostfile myhostfile -np "$ranks" python3 blog/log_temp/process_logs.py 60 20 > pi8proc"$ranks"sec60cyc20.out
    mv output.csv pi8proc"$ranks"sec60cyc20.csv
    sleep 1
done
