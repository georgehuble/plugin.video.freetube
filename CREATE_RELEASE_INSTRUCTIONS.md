# 📦 Инструкция по созданию релиза на GitHub

## 🎯 Создание v1.0.0 Release

### Шаг 1: Перейдите на страницу создания релиза

**Прямая ссылка**: https://github.com/georgehuble/plugin.video.freetube/releases/new

Или:
1. Откройте: https://github.com/georgehuble/plugin.video.freetube
2. Справа найдите **Releases** → **Create a new release**

---

### Шаг 2: Заполните форму релиза

#### 🏷️ Choose a tag
- Введите: **`v1.0.0`**
- Нажмите: **"Create new tag: v1.0.0 on publish"**

#### 📝 Release title
```
FreeTube for Kodi v1.0.0 - Initial Release
```

#### 📄 Description

Скопируйте и вставьте:

```markdown
## 🎉 Initial Release - Full FreeTube Functionality for Kodi!

Watch YouTube privately on Kodi without Google account!

### ✨ Key Features

- ✅ **No Google Authentication Required** - Access YouTube without logging in
- ✅ **Local Subscriptions & History** - All data stored locally on your device
- ✅ **Privacy First** - No tracking, no cookies, no Google account needed
- ✅ **SponsorBlock Integration** - Skip sponsors, intros, outros automatically
- ✅ **DeArrow Support** - Better video titles and thumbnails from community
- ✅ **Multiple Profiles** - Separate profiles with independent data
- ✅ **Import/Export** - From YouTube CSV, FreeTube .db, NewPipe JSON, OPML

### 📦 Quick Installation

**3 Simple Steps:**

1. **Download** `plugin.video.freetube-1.0.0.zip` below ⬇️
2. **Install** in Kodi: `Settings → Add-ons → Install from zip file`
3. **Launch**: `Videos → Video add-ons → FreeTube for Kodi`

**Detailed Instructions**: [KODI_ZIP_INSTALL.md](https://github.com/georgehuble/plugin.video.freetube/blob/master/KODI_ZIP_INSTALL.md)

---

### 📖 Documentation

- 🚀 **[Quick Start](https://github.com/georgehuble/plugin.video.freetube/blob/master/QUICK_START.md)** - 5-minute setup guide
- 📚 **[Installation Guide](https://github.com/georgehuble/plugin.video.freetube/blob/master/INSTALL.md)** - Detailed instructions
- 🏗️ **[Project Summary](https://github.com/georgehuble/plugin.video.freetube/blob/master/PROJECT_SUMMARY.md)** - Architecture & tech details
- 📋 **[Full Release Notes](https://github.com/georgehuble/plugin.video.freetube/blob/master/RELEASE_NOTES_v1.0.0.md)** - Complete changelog

---

### 🔧 Requirements

- **Kodi**: 19.0 (Matrix) or newer
- **Python**: 3.0+
- **Auto-installed**: `script.module.requests`, `inputstream.adaptive`

---

### 📊 What's Included

- **32 files** with **6336+ lines** of code
- **3250+ lines** of Python
- **18 Python modules**
- **4 API integrations** (Innertube, Invidious, SponsorBlock, DeArrow)
- **7 database tables** for local storage
- **8 settings categories**

---

### 🔒 Privacy & Security

**What it does:**
- ✅ Accesses YouTube through Innertube API (no auth needed)
- ✅ Stores all data locally in SQLite
- ✅ Uses Invidious as privacy proxy (optional)

**What it does NOT do:**
- ❌ NO Google account required
- ❌ NO tracking or analytics
- ❌ NO cookies sent to Google
- ❌ NO OAuth or API keys needed

---

### 🙏 Credits

Inspired by:
- [FreeTubeApp/FreeTube](https://github.com/FreeTubeApp/FreeTube) - Original desktop app
- [anxdpanic/plugin.video.youtube](https://github.com/anxdpanic/plugin.video.youtube) - Kodi YouTube plugin
- [LuanRT/YouTube.js](https://github.com/LuanRT/YouTube.js) - Innertube API library

---

### ⚠️ Disclaimer

Not affiliated with YouTube, Google, FreeTube project, or Kodi Foundation.

---

### 🆘 Support

- **Issues**: https://github.com/georgehuble/plugin.video.freetube/issues
- **Discussions**: https://github.com/georgehuble/plugin.video.freetube/discussions

---

## 🎊 Enjoy YouTube Without Google!

**Happy Watching! 🍿📺**
```

---

### Шаг 3: Прикрепите ZIP файл

#### 📎 Attach binaries

В самом низу формы найдите секцию **"Attach binaries by dropping them here or selecting them"**

**Файл для прикрепления**:
- Имя: `plugin.video.freetube-1.0.0.zip`
- Расположение: `C:\Users\nevaj\OneDrive\Desktop\plugin.video.freetube\plugin.video.freetube-1.0.0.zip`
- Размер: 55 KB

**Способы прикрепления**:
1. **Drag & Drop**: Перетащите ZIP файл в область
2. **Click to select**: Нажмите на область и выберите файл

✅ После загрузки вы увидите: `plugin.video.freetube-1.0.0.zip` в списке

---

### Шаг 4: Опции релиза (необязательно)

#### Checkbox Options:
- ☐ **Set as a pre-release** - НЕ отмечайте (это стабильная версия)
- ☐ **Set as the latest release** - ОТМЕТЬТЕ (это последняя версия)
- ☐ **Create a discussion for this release** - По желанию

---

### Шаг 5: Публикация

Нажмите зеленую кнопку: **🚀 Publish release**

---

## ✅ Результат

После публикации релиз будет доступен:

- **Releases Page**: https://github.com/georgehuble/plugin.video.freetube/releases
- **Direct v1.0.0**: https://github.com/georgehuble/plugin.video.freetube/releases/tag/v1.0.0
- **ZIP Download**: https://github.com/georgehuble/plugin.video.freetube/releases/download/v1.0.0/plugin.video.freetube-1.0.0.zip

---

## 📋 Контрольный список

Перед публикацией убедитесь:

- [x] Tag: `v1.0.0`
- [x] Title: "FreeTube for Kodi v1.0.0 - Initial Release"
- [x] Description: Скопирован из инструкции выше
- [x] ZIP файл: `plugin.video.freetube-1.0.0.zip` прикреплен
- [ ] "Set as the latest release": ОТМЕЧЕНО
- [ ] "Set as a pre-release": НЕ ОТМЕЧЕНО

---

## 🔄 Создание будущих релизов

### Версионирование (Semantic Versioning)

Формат: `MAJOR.MINOR.PATCH`

**Примеры**:
- `v1.0.0` → Начальная версия (✅ текущая)
- `v1.0.1` → Багфиксы (patch)
- `v1.1.0` → Новые функции (minor)
- `v2.0.0` → Кардинальные изменения (major)

### Шаблон для будущих версий

При создании v1.1.0:

1. Обновите `addon.xml`:
   ```xml
   <addon id="plugin.video.freetube" name="FreeTube for Kodi" version="1.1.0" ...>
   ```

2. Обновите `changelog.txt`:
   ```
   v1.1.0 (2025-XX-XX)
   - Новая функция 1
   - Новая функция 2
   - Исправление бага X
   ```

3. Создайте новый ZIP:
   ```bash
   powershell -Command "Compress-Archive -Path 'plugin.video.freetube' -DestinationPath 'plugin.video.freetube-1.1.0.zip' -Force"
   ```

4. Создайте релиз на GitHub с новым тагом `v1.1.0`

---

## 🎯 Структура релизов

```
Releases:
├── v1.0.0 (Initial Release) ← СОЗДАЁМ СЕЙЧАС
│   ├── plugin.video.freetube-1.0.0.zip
│   └── Release Notes
│
├── v1.0.1 (Bugfixes) ← Будущее
│   ├── plugin.video.freetube-1.0.1.zip
│   └── Release Notes
│
└── v1.1.0 (New Features) ← Будущее
    ├── plugin.video.freetube-1.1.0.zip
    └── Release Notes
```

---

## 🎊 Готово!

После создания релиза пользователи смогут:

- ⬇️ Скачивать конкретную версию
- 📊 Видеть хронологию релизов
- 📝 Читать changelog для каждой версии
- 🔄 Обновляться с одной версии на другую

---

**Успешной публикации! 🚀**

