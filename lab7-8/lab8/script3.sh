read -p "Введите длину пароля:" length

alph="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
pass=""

for ((i=0; i<length; i++)); do
    pass+="${alph:RANDOM%${#alph}:1}"
done

echo "Сгенерированный пароль: $pass"