if [ "$#" -ne 2 ]; then
    echo "Ожидаемый ввод: $0 num1 num2"
    exit 1
fi

sum=$(( $1 + $2 ))
echo "Сумма: $sum"