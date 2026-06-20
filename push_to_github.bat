@echo off
cd /d "C:\Users\PC\Desktop\Projects\Consultation\Media Expert"

echo Setting up git...
git config user.name "Oluwatobi Bamigboye"
git config user.email "bamtobiloba@gmail.com"

git init
git remote remove origin 2>nul
git remote add origin https://github.com/bamtobiloba-spec/novu-media-co.git

git add .
git commit -m "Initial commit: Novu Media Co. website, automation scripts, and content plan"
git branch -M main
git push -u origin main

echo.
echo Done! Check https://github.com/bamtobiloba-spec/novu-media-co
pause
