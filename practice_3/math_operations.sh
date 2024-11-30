add() {
    echo "Сумма: $(( $1 + $2 ))"
}

subtract() {
    echo "Разность: $(( $1 - $2 ))"
}

multiply() {
    echo "Произведение: $(( $1 * $2 ))"
}

divide() {
    if [ "$2" -eq 0 ]; then
        echo "Ошибка: Деление на ноль"
    else
        echo "Частное: $(( $1 / $2 ))"
    fi
}

echo "Введите первое число:"
read -r num1
echo "Введите второе число:"
read -r num2
echo "Выберите операцию (add, subtract, multiply, divide):"
read -r operation

case $operation in
    add) add "$num1" "$num2" ;;
    subtract) subtract "$num1" "$num2" ;;
    multiply) multiply "$num1" "$num2" ;;
    divide) divide "$num1" "$num2" ;;
    *) echo "Недопустимая операция" ;;
esac