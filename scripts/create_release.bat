@echo off
REM Скрипт для создания нового релиза FreeTube for Kodi (Windows)
REM Использование: create_release.bat VERSION
REM Пример: create_release.bat 1.1.0

setlocal enabledelayedexpansion

set VERSION=%1

if "%VERSION%"=="" (
    echo ❌ Ошибка: Не указана версия
    echo Использование: create_release.bat VERSION
    echo Пример: create_release.bat 1.1.0
    exit /b 1
)

echo 🚀 Создание релиза v%VERSION%...

REM Проверка, что мы в корне репозитория
if not exist "addon.xml" (
    echo ❌ Ошибка: addon.xml не найден
    echo Запустите скрипт из корня репозитория
    exit /b 1
)

REM Обновление версии в addon.xml
echo 📝 Обновление addon.xml...
powershell -Command "(Get-Content addon.xml) -replace 'version=\"[0-9.]*\"', 'version=\"%VERSION%\"' | Set-Content addon.xml"

REM Получение даты
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "DATE=%dt:~0,4%-%dt:~4,2%-%dt:~6,2%"

REM Создание временного файла для changelog
echo v%VERSION% (%DATE%) > changelog.txt.tmp
echo - TODO: Добавьте описание изменений >> changelog.txt.tmp
echo. >> changelog.txt.tmp
type changelog.txt >> changelog.txt.tmp
move /y changelog.txt.tmp changelog.txt

REM Создание ZIP файла
echo 📦 Создание ZIP файла...
cd ..
set ZIP_NAME=plugin.video.freetube-%VERSION%.zip
powershell -Command "Compress-Archive -Path 'plugin.video.freetube' -DestinationPath '%ZIP_NAME%' -Force"
cd plugin.video.freetube

REM Создание release notes
echo 📄 Создание RELEASE_NOTES_v%VERSION%.md...
(
echo # FreeTube for Kodi v%VERSION%
echo.
echo **Release Date**: %DATE%
echo **Download**: [plugin.video.freetube-%VERSION%.zip]^(https://github.com/georgehuble/plugin.video.freetube/releases/download/v%VERSION%/plugin.video.freetube-%VERSION%.zip^)
echo.
echo ---
echo.
echo ## 🎯 What's New in v%VERSION%
echo.
echo TODO: Добавьте описание изменений
echo.
echo ### New Features
echo - TODO: Новая функция 1
echo - TODO: Новая функция 2
echo.
echo ### Bug Fixes
echo - TODO: Исправленный баг 1
echo - TODO: Исправленный баг 2
echo.
echo ---
echo.
echo ## 📦 Installation
echo.
echo Download `plugin.video.freetube-%VERSION%.zip` and install via Kodi
echo.
echo See [KODI_ZIP_INSTALL.md]^(https://github.com/georgehuble/plugin.video.freetube/blob/master/KODI_ZIP_INSTALL.md^)
) > RELEASE_NOTES_v%VERSION%.md

echo.
echo ✅ Готово!
echo.
echo 📋 Следующие шаги:
echo 1. Отредактируйте RELEASE_NOTES_v%VERSION%.md
echo 2. Отредактируйте changelog.txt
echo 3. Закоммитьте изменения:
echo    git add .
echo    git commit -m "Release v%VERSION%"
echo    git tag v%VERSION%
echo    git push origin master --tags
echo 4. Создайте релиз на GitHub:
echo    https://github.com/georgehuble/plugin.video.freetube/releases/new
echo 5. Прикрепите ZIP файл: ..\%ZIP_NAME%
echo.

pause

