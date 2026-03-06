@echo off
cd /d "C:\Users\David\Desktop\MyWebsiteLocal\Test"
python scraper_greenhouse.py
git add .
git commit -m "Auto-update jobs"
git push
echo %date% %time% > scrape_time.txt
git add scrape_time.txt
git commit -m "Update scrape timestamp"
git push
pause