read -p "Введите путь к директории, которую нужно архивировать: " dirpath

if [[ ! -d "$dirpath" ]]; then
    echo "Ошибка: Директория $dirpath не найдена!"
    exit 1
fi

current_date=$(date +%Y-%m-%d)

archive_name="$(basename "$dirpath")_$current_date.tar.gz"

tar -czf "$archive_name" -C "$(dirname "$dirpath")" "$(basename "$dirpath")"

if [[ $? -eq 0 ]]; then
    echo "Архив успешно создан: $archive_name"
else
    echo "Ошибка при создании архива."
fi