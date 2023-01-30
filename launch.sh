git pull
conda activate tgen
[ -d "~/bank" ] && ./mount.sh
accelerate --multi_gpu --debug src/scripts/run.py $1