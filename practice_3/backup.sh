if [ "$#" -ne 2 ]; then
    echo "Ожидаемый ввод: $0 source_dir target_dir"
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "Директория $1 не существует."
    exit 1
fi

mkdir -p "$2"

for file in "$1"/*; do
    base_name=$(basename "$file")
    cp "$file" "$2/${base_name}_$(date +%Y-%m-%d)"
done

echo "Файлы успешно скопированы в $2 с добавлением даты."