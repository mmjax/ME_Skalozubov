read -p "Введите путь к файлу для отслеживания изменений:" file_path

if [ ! -f "$file_path" ]; then
  echo "Указанный файл не существует."
  exit 1
fi

prev_checksum=$(md5sum "$file_path" | awk '{print $1}')

while true; do
  current_checksum=$(md5sum "$file_path" | awk '{print $1}')

  if [ "$prev_checksum" != "$current_checksum" ]; then
    echo "Файл $file_path был изменен!"
    prev_checksum=$current_checksum
  fi
  sleep 1
done