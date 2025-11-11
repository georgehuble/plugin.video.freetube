#!/bin/bash
# Скрипт для создания нового релиза FreeTube for Kodi
# Использование: ./create_release.sh VERSION
# Пример: ./create_release.sh 1.1.0

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "❌ Ошибка: Не указана версия"
    echo "Использование: ./create_release.sh VERSION"
    echo "Пример: ./create_release.sh 1.1.0"
    exit 1
fi

echo "🚀 Создание релиза v${VERSION}..."

# Проверка, что мы в корне репозитория
if [ ! -f "addon.xml" ]; then
    echo "❌ Ошибка: addon.xml не найден"
    echo "Запустите скрипт из корня репозитория"
    exit 1
fi

# Обновление версии в addon.xml
echo "📝 Обновление addon.xml..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/version=\"[0-9.]*\"/version=\"${VERSION}\"/" addon.xml
else
    # Linux/Windows Git Bash
    sed -i "s/version=\"[0-9.]*\"/version=\"${VERSION}\"/" addon.xml
fi

# Добавление записи в changelog
echo "📝 Обновление changelog.txt..."
DATE=$(date +%Y-%m-%d)
{
    echo "v${VERSION} (${DATE})"
    echo "- TODO: Добавьте описание изменений"
    echo ""
    cat changelog.txt
} > changelog.txt.tmp
mv changelog.txt.tmp changelog.txt

# Создание ZIP файла
echo "📦 Создание ZIP файла..."
cd ..
ZIP_NAME="plugin.video.freetube-${VERSION}.zip"

if command -v zip &> /dev/null; then
    zip -r "$ZIP_NAME" plugin.video.freetube/ -x "*.git*" "*__pycache__*" "*.pyc" "*.pyo" "*/.*"
elif command -v powershell &> /dev/null; then
    powershell -Command "Compress-Archive -Path 'plugin.video.freetube' -DestinationPath '${ZIP_NAME}' -Force"
else
    echo "❌ Ошибка: zip или powershell не найдены"
    exit 1
fi

cd plugin.video.freetube

# Создание release notes
echo "📄 Создание RELEASE_NOTES_v${VERSION}.md..."
cat > "RELEASE_NOTES_v${VERSION}.md" << EOF
# FreeTube for Kodi v${VERSION}

**Release Date**: ${DATE}  
**Download**: [plugin.video.freetube-${VERSION}.zip](https://github.com/georgehuble/plugin.video.freetube/releases/download/v${VERSION}/plugin.video.freetube-${VERSION}.zip)

---

## 🎯 What's New in v${VERSION}

TODO: Добавьте описание изменений

### New Features
- TODO: Новая функция 1
- TODO: Новая функция 2

### Bug Fixes
- TODO: Исправленный баг 1
- TODO: Исправленный баг 2

### Improvements
- TODO: Улучшение 1
- TODO: Улучшение 2

---

## 📦 Installation

Download \`plugin.video.freetube-${VERSION}.zip\` and install via Kodi:
\`Settings → Add-ons → Install from zip file\`

See [KODI_ZIP_INSTALL.md](https://github.com/georgehuble/plugin.video.freetube/blob/master/KODI_ZIP_INSTALL.md)

---

## 🔄 Upgrading from Previous Version

1. Install new ZIP over existing installation
2. Kodi will automatically update
3. Data (subscriptions, history) will be preserved

---

## 📜 Full Changelog

See [changelog.txt](https://github.com/georgehuble/plugin.video.freetube/blob/master/changelog.txt)

---

**Previous Release**: [v1.0.0](https://github.com/georgehuble/plugin.video.freetube/releases/tag/v1.0.0)
EOF

echo ""
echo "✅ Готово!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Отредактируйте RELEASE_NOTES_v${VERSION}.md"
echo "2. Отредактируйте changelog.txt"
echo "3. Закоммитьте изменения:"
echo "   git add ."
echo "   git commit -m \"Release v${VERSION}\""
echo "   git tag v${VERSION}"
echo "   git push origin master --tags"
echo "4. Создайте релиз на GitHub:"
echo "   https://github.com/georgehuble/plugin.video.freetube/releases/new"
echo "5. Прикрепите ZIP файл: ../${ZIP_NAME}"
echo ""

