read -p "Введите токен от телеграм бота:" TOKEN
read -p "Введите id пользователя, у которого есть активный чат с ботом:" CHAT_ID

MESSAGE="Привет, это тестовое сообщение!"

URL="https://api.telegram.org/bot$TOKEN/sendMessage"

curl -s -X POST $URL -d "chat_id=$CHAT_ID" -d "text=$MESSAGE"

echo "Сообщение отправлено!"