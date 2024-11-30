if [ "$#" -ne 3 ]; then
    echo "Ожидаемый ввод: $0 filename old_word new_word"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Файл $1 не существует."
    exit 1
fi

sed -i '' "s/$2/$3/g" "$1"
echo "Текст '$2' заменён на '$3' в файле $1."