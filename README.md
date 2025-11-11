# FreeTube for Kodi

<p align="center">
  <img src="resources/media/icon.png" alt="FreeTube for Kodi logo" width="180">
</p>

<p align="center">
  <a href="#english">English</a> · <a href="#русский">Русский</a>
</p>

<p align="center">
  <a href="https://github.com/georgehuble/plugin.video.freetube/releases/latest"><img src="https://img.shields.io/github/v/release/georgehuble/plugin.video.freetube?label=Latest%20release&style=for-the-badge" alt="Latest release"></a>
  <a href="https://github.com/georgehuble/plugin.video.freetube/releases"><img src="https://img.shields.io/github/downloads/georgehuble/plugin.video.freetube/total?label=Downloads&style=for-the-badge" alt="Downloads"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/georgehuble/plugin.video.freetube?label=License&style=for-the-badge" alt="License"></a>
</p>

<a id="english"></a>

## English

### For Users

#### Quick Start
1. Download the latest `plugin.video.freetube-<version>.zip` package from the releases page.
2. In Kodi, open `Settings` → `Add-ons` → `Install from zip file`.
3. Select the downloaded archive. Kodi installs the add-on under `Video add-ons`.
4. Launch FreeTube, create a local profile, and start browsing subscriptions or search results.

#### Feature Highlights
- Private playback through the Innertube API with automatic fallback to trusted Invidious instances.
- Local subscriptions, history, playlists, and profiles stored only on your device.
- SponsorBlock and DeArrow integrations with configurable categories.
- Import and export of subscriptions from YouTube CSV, FreeTube database, NewPipe JSON, or OPML.

#### Updating
- Install a newer release zip to upgrade in place; Kodi preserves your local data.
- Review `changelog.txt` and the release notes before updating to understand behavioural changes.

#### Support and Feedback
- Report issues through GitHub with reproduction steps and Kodi logs when possible.
- Feature ideas are welcome; describe the user scenario and expected outcome.

### For Developers

#### Repository Layout
- `addon.xml` defines metadata, dependencies, and entry points.
- `resources/lib` contains the Kodi plug-in modules.
- `resources/lib/freetube/api` and `resources/lib/freetube/integrations` provide service clients and partner integrations.
- `resources/lib/freetube/storage` implements local persistence and migrations.
- `resources/media/icon.png` is the shared add-on icon for Kodi and project documentation.

#### Local Development
1. Clone the repository and place it in the Kodi add-ons directory (`%APPDATA%\Kodi\addons` on Windows or `~/.kodi/addons` on Linux).
2. Enable Kodi developer mode and set logging to verbose for easier troubleshooting.
3. Modify sources under `resources/lib`, reload Kodi, and monitor the Kodi log for errors.
4. Use `scripts/create_release.bat` (Windows) or `scripts/create_release.sh` (Linux/macOS) to package the add-on zip for distribution.

#### Contribution Workflow
1. Fork the repository and create a topic branch for your change.
2. Add tests or diagnostics where applicable, and verify the add-on inside a Kodi development environment.
3. Update documentation if behaviour or configuration changes.
4. Submit a pull request that references related issues and outlines validation steps.

#### License
FreeTube for Kodi is distributed under the AGPL-3.0-or-later license. See `LICENSE` for full terms.

---

<a id="русский"></a>

## Русский

### Для пользователей

#### Быстрый старт
1. Загрузите актуальный архив `plugin.video.freetube-<версия>.zip` со страницы релизов.
2. В Kodi откройте `Настройки` → `Дополнения` → `Установить из zip-файла`.
3. Укажите загруженный архив. Дополнение появится в разделе `Видео-дополнения`.
4. Запустите FreeTube, создайте локальный профиль и переходите к каналам или поиску.

#### Основные возможности
- Приватный просмотр через Innertube API с автоматическим переходом на доверенные экземпляры Invidious.
- Локальные подписки, история, плейлисты и профили хранятся только на вашем устройстве.
- Интеграции SponsorBlock и DeArrow с настраиваемыми категориями.
- Импорт и экспорт подписок из YouTube CSV, базы FreeTube, NewPipe JSON или OPML.

#### Обновление
- Для обновления установите новую версию zip поверх текущей; Kodi сохранит локальные данные.
- Перед установкой изучайте `changelog.txt` и заметки к релизу, чтобы понимать изменения.

#### Поддержка и обратная связь
- Сообщайте об ошибках в GitHub, прикладывая шаги воспроизведения и журналы Kodi.
- Предлагайте улучшения, описывая сценарий использования и ожидаемый результат.

### Для разработчиков

#### Структура репозитория
- `addon.xml` содержит метаданные, зависимости и точки входа.
- `resources/lib` включает исходный код дополнения для Kodi.
- `resources/lib/freetube/api` и `resources/lib/freetube/integrations` предоставляют сервисные клиенты и интеграции.
- `resources/lib/freetube/storage` отвечает за локальное хранилище и миграции.
- `resources/media/icon.png` — единый значок дополнения для Kodi и документации проекта.

#### Локальная разработка
1. Клонируйте репозиторий и поместите его в каталог дополнений Kodi (`%APPDATA%\Kodi\addons` в Windows или `~/.kodi/addons` в Linux).
2. Включите режим разработчика Kodi и подробное логирование для диагностики.
3. Вносите изменения в `resources/lib`, перезапускайте Kodi и анализируйте журнал Kodi.
4. Для подготовки релиза используйте `scripts/create_release.bat` (Windows) или `scripts/create_release.sh` (Linux/macOS), которые формируют дистрибутивный zip.

#### Процесс контрибуции
1. Сделайте форк репозитория и создайте ветку для правки.
2. Добавьте тесты или диагностические журналы при необходимости и проверьте работу дополнения в среде Kodi.
3. Обновите документацию, если поведение или настройки изменились.
4. Отправьте pull request с описанием изменений и указанием сценариев проверки.

#### Лицензия
FreeTube for Kodi распространяется по лицензии AGPL-3.0-or-later. Полный текст доступен в файле `LICENSE`.

