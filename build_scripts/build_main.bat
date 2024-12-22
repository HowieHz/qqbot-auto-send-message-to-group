del .\dist\qqbot-auto-send-message-to-group.exe
pyinstaller .\src\main.py --onefile
ren .\dist\main.exe qqbot-auto-send-message-to-group.exe
