while true; do
    read -p "Введите цифпу (1-Дата, 2-Время, 3-Файлы, 4-Система, 5-Калькулятор, 6-Запуск, 0-Выход):" command

    case $command in
        "1")
            echo "Текущая дата: $(date)"
            ;;
        "2")
            echo "Текущее время: $(date +%T)"
            ;;
        "3")
            echo "Список файлов в текущей директории:"
            ls -l
            ;;
        "4")
            echo "Информация о системе:"
            echo "Доступная память:"
            sysctl -a | grep mem
            echo "Загрузка процессора:"
            top -l 1 -s 0 | grep "CPU usage"
            ;;
        "5")
            read -p "Введите математическое выражение (например, 2 + 2):" expression
            result=$(echo "$expression" | bc -l)
            echo "Результат: $result"
            ;;
        "6")
            read -p "Введите команду для запуска:" user_command
            echo "Запуск команды: $user_command"
            $user_command
            ;;
        "0")
            echo "До свидания!"
            break
            ;;
        *)
            echo "Неизвестная команда: $command"
            ;;
    esac
done