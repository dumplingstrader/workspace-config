@echo off
echo Installing GU Forge Assistant dependencies...
pip install -r requirements.txt
echo.
echo Installing Playwright browsers...
playwright install chromium
echo.
echo Done! Run with: python main.py
pause
