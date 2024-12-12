read -p "Введите путь к директории: " dirpath

if [[ ! -d "$dirpath" ]]; then
    echo "Ошибка: Директория $dirpath не найдена!"
    exit 1
fi

for file in "$dirpath"/*; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file")
        mv "$file" "$dirpath/backup_$filename"
        echo "Файл $filename переименован в backup_$filename"
    fi
done

echo "Переименование завершено."