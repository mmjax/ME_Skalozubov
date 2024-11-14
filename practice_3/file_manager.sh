mkdir temp_dir
cd temp_dir || exit 1

touch file1.txt file2.txt file3.txt
echo "Files created."
sleep 10
rm file1.txt file2.txt file3.txt
echo "Files deleted."

cd ..
rmdir temp_dir
echo "Directory removed."