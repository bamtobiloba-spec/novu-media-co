@echo off
cd /d "C:\Users\PC\Desktop\Projects\Consultation\Media Expert\agent"
echo Installing required packages...
pip install requests python-dotenv --quiet
echo.
echo Running TikTok credential test...
python post_tiktok.py --info
pause
