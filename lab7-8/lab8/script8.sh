read -p "Введите дирректорию:" DIRECTORY

if [ ! -d "$DIRECTORY" ]; then
  echo "Указанная директория не существует."
  exit 1
fi

find "$DIRECTORY" -type f -name "*.log" -exec ls -lt {} + | tail -n 5