echo "Starting build..."

pyinstaller --onefile ./test.py

cp ./dist/test.exe ../console-tester.exe
rm -r ./dist
rm ./test.spec

echo "Build complete"