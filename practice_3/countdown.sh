if [ -z "$1" ]; then
    echo "Please provide a number as an argument."
    exit 1
fi

count=$1
while [ $count -ge 0 ]; do
    echo $count
    ((count--))
done