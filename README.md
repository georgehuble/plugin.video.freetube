# FreeTube for Kodi

![FreeTube Logo](resources/media/icon.png)

**Watch YouTube privately on Kodi with full FreeTube functionality**

## 🎯 Features

- ✅ **No Google Account Required** - Access YouTube without authentication
- ✅ **Local Subscriptions** - Subscribe to channels, all data stored locally
- ✅ **Watch History** - Track your viewing history locally
- ✅ **Profiles** - Multiple user profiles with separate subscriptions
- ✅ **Local Playlists** - Create and manage playlists locally
- ✅ **SponsorBlock** - Skip sponsors, intros, outros automatically
- ✅ **DeArrow** - Better video titles and thumbnails
- ✅ **Invidious Fallback** - Automatic fallback to Invidious API
- ✅ **Import/Export** - Import subscriptions from YouTube, NewPipe, FreeTube
- ✅ **Privacy First** - No tracking, no Google login

## 🚀 Installation

1. Download the latest release
2. Install via Kodi: **Settings → Add-ons → Install from zip file**
3. Select the downloaded zip file
4. Done! Find "FreeTube" in Video Add-ons

## 📖 How It Works

This plugin uses the same approach as the FreeTube desktop application:

1. **Innertube API** - Direct access to YouTube's internal API without authentication
2. **Local Storage** - All subscriptions, history, and playlists stored in Kodi's database
3. **Invidious Fallback** - If direct access fails, automatically switches to Invidious instances

## 🎮 Usage

### Main Menu
- **Subscriptions** - View videos from your subscribed channels
- **Trending** - See what's trending
- **Search** - Search for videos
- **History** - View your watch history
- **Playlists** - Manage local playlists
- **Profiles** - Switch between different profiles

### Managing Subscriptions
1. Find a channel you like
2. Open context menu (C key or long press on remote)
3. Select "Subscribe"
4. Videos will appear in your Subscriptions feed

### Import Subscriptions
1. Go to Settings → Data Management
2. Select "Import Subscriptions"
3. Choose file format (YouTube CSV, FreeTube DB, NewPipe JSON, OPML)
4. Select your file

## ⚙️ Settings

### API Backend
- **Local API** (Default) - Direct Innertube API access
- **Invidious** - Use public Invidious instances
- **Auto Fallback** - Automatically switch if primary fails

### Privacy
- **Enable Watch History** - Track viewed videos
- **Enable Search History** - Save search queries
- **Clear Data** - Delete all local data

### SponsorBlock
- **Enable SponsorBlock** - Skip video segments
- **Categories** - Choose which categories to skip
  - Sponsor
  - Intro
  - Outro
  - Self Promotion
  - Interaction Reminder
  - Preview/Recap

### Profiles
- **Default Profile** - Main profile
- **Create Profile** - Add new profiles
- **Switch Profile** - Change active profile

## 🔧 Technical Details

### Architecture
```
plugin.video.freetube/
├── Innertube API Client (No auth required)
├── Invidious API Client (Fallback)
├── Local Database (SQLite)
│   ├── Subscriptions
│   ├── History
│   ├── Profiles
│   └── Playlists
└── UI Layer (Kodi navigation)
```

### Privacy Approach
Based on [FreeTube](https://github.com/FreeTubeApp/FreeTube):
- No Google authentication
- No tracking cookies
- All data stored locally
- Optional proxy support
- Invidious instances as privacy layer

### Credits
- Inspired by [FreeTubeApp/FreeTube](https://github.com/FreeTubeApp/FreeTube)
- Uses concepts from [plugin.video.youtube](https://github.com/anxdpanic/plugin.video.youtube)
- Built with [youtubei.js](https://github.com/LuanRT/YouTube.js) methodology

## 📝 License

AGPL-3.0-or-later - See [LICENSE](LICENSES/AGPL-3.0-or-later.txt)

## ⚠️ Disclaimer

This plugin is not affiliated with, endorsed by, or connected to YouTube, Google Inc., or the FreeTube project.

