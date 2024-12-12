echo "Запуск команд"
echo "1 команда"
sleep 5 &
echo "2 команда"
sleep 10 &
echo "3 команда"
sleep 15 &
wait

echo "Все команды завершены."