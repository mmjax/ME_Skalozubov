read -p "Введите путь к директории: " dir

if [ ! -d "$dir" ]; then
  echo "Указанная директория не существует."
  exit 1
fi

for file in "$dir"/*; do
  if [ -f "$file" ]; then
    new_name=$(echo "$file" | tr '[:upper:]' '[:lower:]')

    mv "$file" "$new_name"
    echo "Переименован файл: $file -> $new_name"
  fi
done

echo "Все файлы в директории переименованы в строчные буквы."