# 📤 Загрузка FreeTube for Kodi на GitHub

## 🔗 Ваш репозиторий
**https://github.com/georgehuble/plugin.video.freetube**

---

## 📋 Пошаговая инструкция

### Вариант 1: Через GitHub Desktop (Простой)

#### 1. Установите GitHub Desktop
- Скачайте: https://desktop.github.com/
- Установите и войдите в свой аккаунт

#### 2. Клонируйте репозиторий
1. Откройте GitHub Desktop
2. **File** → **Clone repository**
3. Выберите: **georgehuble/plugin.video.freetube**
4. Выберите папку для сохранения
5. Нажмите **Clone**

#### 3. Скопируйте файлы
```bash
# Скопируйте все файлы из plugin.video.freetube в клонированный репозиторий
# Кроме .git папки!

Источник: C:\Users\nevaj\OneDrive\Desktop\Freetube_kodi_plugin\plugin.video.freetube\
Назначение: [ваша папка с клонированным репозиторием]
```

#### 4. Commit и Push
1. В GitHub Desktop увидите все новые файлы
2. Внизу слева напишите commit message:
   ```
   Initial release v1.0.0 - Full FreeTube functionality for Kodi
   ```
3. Нажмите **Commit to master**
4. Нажмите **Push origin**

✅ Готово! Код на GitHub!

---

### Вариант 2: Через Git командную строку

#### 1. Клонируйте репозиторий
```bash
cd C:\Users\nevaj\OneDrive\Desktop\Freetube_kodi_plugin
git clone https://github.com/georgehuble/plugin.video.freetube.git github-repo
cd github-repo
```

#### 2. Скопируйте файлы
```bash
# Скопируйте все файлы из plugin.video.freetube, КРОМЕ самой папки plugin.video.freetube
# То есть содержимое должно быть в корне репозитория

xcopy /E /I /Y ..\plugin.video.freetube\* .
```

#### 3. Добавьте файлы в Git
```bash
git add .
git commit -m "Initial release v1.0.0 - Full FreeTube functionality for Kodi"
git push origin master
```

✅ Готово!

---

### Вариант 3: Через веб-интерфейс GitHub (Самый простой, но медленный)

#### 1. Перейдите в репозиторий
https://github.com/georgehuble/plugin.video.freetube

#### 2. Удалите LICENSE (если хотите заменить структуру)
- Нажмите на **LICENSE**
- Нажмите иконку корзины (Delete)
- Commit changes

#### 3. Загрузите файлы
1. Нажмите **Add file** → **Upload files**
2. Перетащите ВСЕ файлы и папки из `plugin.video.freetube/` в окно браузера
3. Commit message:
   ```
   Initial release v1.0.0 - Full FreeTube functionality for Kodi
   ```
4. Нажмите **Commit changes**

⚠️ **Внимание**: Этот метод может не сохранить структуру папок корректно. Лучше используйте Вариант 1 или 2.

---

## 📁 Структура для загрузки на GitHub

Корень репозитория должен выглядеть так:

```
plugin.video.freetube/          ← РЕПОЗИТОРИЙ
├── .github/                     ← (опционально, для CI/CD)
├── .gitignore
├── LICENSE                      ← Уже есть (AGPL-3.0)
├── README.md                    ← Главное описание
├── INSTALL.md
├── QUICK_START.md
├── BUILD.md
├── PROJECT_SUMMARY.md
├── COMPLETION_REPORT.md
├── KODI_ZIP_INSTALL.md
├── GITHUB_UPLOAD_GUIDE.md       ← Этот файл
├── addon.xml
├── changelog.txt
├── LICENSES/
│   └── AGPL-3.0-or-later.txt
└── resources/
    ├── settings.xml
    ├── language/
    │   └── resource.language.en_gb/
    │       └── strings.po
    ├── media/                   ← (добавьте иконки, если есть)
    │   ├── icon.png
    │   └── fanart.jpg
    └── lib/
        ├── __init__.py
        ├── plugin.py
        ├── service.py
        └── freetube/
            ├── __init__.py
            ├── provider.py
            ├── utils.py
            ├── api/
            ├── storage/
            └── integrations/
```

---

## 📝 Рекомендуемый README.md для GitHub

После загрузки отредактируйте `README.md`:

```markdown
# FreeTube for Kodi

![FreeTube Logo](resources/media/icon.png)

**Watch YouTube privately on Kodi with full FreeTube functionality**

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Kodi Version](https://img.shields.io/badge/kodi-19%2B-blue.svg)](https://kodi.tv/)
[![Python](https://img.shields.io/badge/python-3.0%2B-blue.svg)](https://www.python.org/)

## ✨ Features

- ✅ **No Google Account Required** - Access YouTube without authentication
- ✅ **Local Subscriptions** - All data stored locally
- ✅ **Privacy First** - No tracking, no cookies
- ✅ **SponsorBlock** - Skip sponsors automatically
- ✅ **DeArrow** - Better titles and thumbnails
- ✅ **Multiple Profiles** - Separate data for different users
- ✅ **Import/Export** - From YouTube, FreeTube, NewPipe

## 🚀 Quick Install

### Method 1: Install from ZIP (Easiest)

1. Download: [plugin.video.freetube-1.0.0.zip](https://github.com/georgehuble/plugin.video.freetube/releases)
2. Kodi: **Settings → Add-ons → Install from zip file**
3. Select downloaded ZIP
4. Done!

See [KODI_ZIP_INSTALL.md](KODI_ZIP_INSTALL.md) for detailed instructions.

### Method 2: Manual Installation

See [INSTALL.md](INSTALL.md)

## 📖 Documentation

- [Quick Start Guide](QUICK_START.md) - 5-minute setup
- [Installation Guide](INSTALL.md) - Detailed instructions
- [Project Summary](PROJECT_SUMMARY.md) - Architecture & tech details
- [Completion Report](COMPLETION_REPORT.md) - Full feature list

## 🎯 How It Works

FreeTube for Kodi uses the same approach as the FreeTube desktop app:
- **Innertube API** - Direct YouTube access without authentication
- **Invidious Fallback** - Privacy-preserving proxy
- **Local Storage** - SQLite database for all data

## 🔒 Privacy

- ❌ NO Google authentication
- ❌ NO tracking cookies
- ❌ NO analytics
- ✅ All data stored locally

## 📜 License

AGPL-3.0-or-later

## 🙏 Credits

Inspired by:
- [FreeTubeApp/FreeTube](https://github.com/FreeTubeApp/FreeTube)
- [anxdpanic/plugin.video.youtube](https://github.com/anxdpanic/plugin.video.youtube)
- [LuanRT/YouTube.js](https://github.com/LuanRT/YouTube.js)

## ⚠️ Disclaimer

This plugin is not affiliated with YouTube, Google, or the FreeTube project.
```

---

## 🏷️ Создание первого Release

После загрузки кода создайте Release:

1. Перейдите на вкладку **Releases**
2. Нажмите **Create a new release**
3. Tag version: **v1.0.0**
4. Release title: **FreeTube for Kodi v1.0.0 - Initial Release**
5. Description:
   ```markdown
   ## 🎉 Initial Release

   Full FreeTube functionality for Kodi!

   ### Features
   - ✅ YouTube without Google account
   - ✅ Local subscriptions & history
   - ✅ SponsorBlock integration
   - ✅ DeArrow support
   - ✅ Multiple profiles
   - ✅ Import/Export subscriptions

   ### Installation
   Download `plugin.video.freetube-1.0.0.zip` and install via Kodi.

   See [KODI_ZIP_INSTALL.md](KODI_ZIP_INSTALL.md) for instructions.

   ### Documentation
   - [Quick Start](QUICK_START.md)
   - [Full Install Guide](INSTALL.md)
   - [Project Summary](PROJECT_SUMMARY.md)
   ```

6. Прикрепите файл: **plugin.video.freetube-1.0.0.zip**
7. Нажмите **Publish release**

✅ Готово! Теперь пользователи могут скачать ZIP из Releases!

---

## 📊 Рекомендуемые настройки репозитория

### Topics (темы) для поиска
Добавьте в Settings → Topics:
- `kodi`
- `kodi-addon`
- `kodi-plugin`
- `youtube`
- `freetube`
- `privacy`
- `sponsorblock`
- `dearrow`
- `python`

### Description
```
Privacy-first YouTube addon for Kodi. Watch without Google account, manage subscriptions locally, SponsorBlock & DeArrow support.
```

### Website
```
https://github.com/georgehuble/plugin.video.freetube
```

---

## ✅ Контрольный список

- [ ] Код загружен на GitHub
- [ ] README.md обновлен
- [ ] Создан Release v1.0.0
- [ ] ZIP файл прикреплен к Release
- [ ] Topics добавлены
- [ ] Description обновлен
- [ ] LICENSE проверен (AGPL-3.0)

---

## 🎊 Готово!

Ваш проект на GitHub: **https://github.com/georgehuble/plugin.video.freetube**

Теперь пользователи могут:
- ⭐ Поставить звезду
- 🍴 Сделать Fork
- 📥 Скачать ZIP из Releases
- 📝 Создавать Issues
- 🤝 Делать Pull Requests

**Удачи с проектом!** 🚀

