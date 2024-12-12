echo "Введите имя файла:"
read filename

echo "Введите слово для поиска:"
read word

if [[ ! -f "$filename" ]]; then
    echo "Файл не найден."
    exit 1
fi

count=$(grep -o -i "$word" "$filename" | wc -l)

echo "Слово '$word' встречается в файле '$filename' $count раз."