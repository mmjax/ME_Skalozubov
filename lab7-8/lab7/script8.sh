disk_usage=$(df / | grep / | awk '{ print $5 }' | sed 's/%//')

if (( disk_usage > 80 )); then
    echo "Внимание: использование диска превышает 80% (текущее: $disk_usage%)!"
else
    echo "Использование диска в пределах нормы: $disk_usage%."
fi