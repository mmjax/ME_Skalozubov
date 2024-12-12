read -p "Введите путь к директории: " dirpath

if [[ ! -d "$dirpath" ]]; then
    echo "Ошибка: Директория $dirpath не найдена!"
    exit 1
fi

find "$dirpath" -type f -mtime +7 -exec rm -v {} \;

echo "Удаление завершено"