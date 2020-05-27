while true;do filename="`date +%Y_%m_%d_%H_%M_%S`.log"; vcgencmd measure_temp > $filename;sleep 5;done
