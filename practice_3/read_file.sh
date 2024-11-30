if [ "$#" -ne 1 ]; then
    echo "Ожидаемый ввод: $0 filename"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Файл $1 не существует."
    exit 1
fi

while IFS= read -r line; do
    echo "$line"
done < "$1"