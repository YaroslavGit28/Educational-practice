@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
echo ВНИМАНИЕ: применит все 6 этапов с коммитами.
echo Убедитесь что git init уже выполнен.
echo.
set /p OK=Продолжить? (y/n): 
if /i not "%OK%"=="y" exit /b 0

call scripts\apply-stage.bat 1
git add -A
git commit -F git-stages/stage-01/COMMIT.txt --date="2026-06-02T15:30:00"

call scripts\apply-stage.bat 2
git add -A
git commit -F git-stages/stage-02/COMMIT.txt --date="2026-06-05T14:00:00"

call scripts\apply-stage.bat 3
git add -A
git commit -F git-stages/stage-03/COMMIT.txt --date="2026-06-09T16:45:00"

call scripts\apply-stage.bat 4
git add -A
git commit -F git-stages/stage-04/COMMIT.txt --date="2026-06-12T11:20:00"

call scripts\apply-stage.bat 5
git add -A
git commit -F git-stages/stage-05/COMMIT.txt --date="2026-06-16T13:10:00"

call scripts\apply-stage.bat 6
git add -A
git commit -F git-stages/stage-06/COMMIT.txt --date="2026-06-20T10:30:00"

echo.
echo Готово. Проверьте: git log --oneline
pause
