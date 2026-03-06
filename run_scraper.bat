@echo off
cd /d "C:\Users\David\Desktop\MyWebsiteLocal\Test"
python scraper_greenhouse.py
git add .
git commit -m "Auto-update jobs"
git push
pause