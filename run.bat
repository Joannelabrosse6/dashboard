@echo off
echo ==========================================
echo    Lancement du Projet VOD Analysis
echo ==========================================
echo.

echo [1/4] Demarrage du service MySQL...
net start MySQL80 2>nul
net start MySQL 2>nul

echo.
echo [2/4] Initialisation de la base de donnees (init_db.sql)...
cmd /c "mysql -u root -proot < init_db.sql"

echo.
echo [3/4] Lancement du Pipeline Python (Traitement et API)...
call .\venv\Scripts\python.exe pipeline.py

echo.
echo [4/4] Lancement du Dashboard (Dash/Plotly)...
call .\venv\Scripts\python.exe dashboard.py

pause
