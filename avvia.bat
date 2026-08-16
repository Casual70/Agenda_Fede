@echo off
echo Avvio server Agenda Turni...
start "" python "%~dp0server.py"
timeout /t 2 /nobreak >nul
start "" http://localhost:8080
echo Server avviato. Il browser si e' aperto su http://localhost:8080
echo Il server si spegnera' automaticamente dopo l'elaborazione del PDF.
