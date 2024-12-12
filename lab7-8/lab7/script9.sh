echo "Введите команду для запуска в фоне:"
read command

$command &

pid=$!

echo "Команда '$command' запущена в фоне с PID: $pid"