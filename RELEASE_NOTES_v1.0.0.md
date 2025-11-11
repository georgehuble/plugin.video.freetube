# 🎉 FreeTube for Kodi v1.0.0 - Initial Release

**Release Date**: November 11, 2025  
**Download**: [plugin.video.freetube-1.0.0.zip](https://github.com/georgehuble/plugin.video.freetube/releases/download/v1.0.0/plugin.video.freetube-1.0.0.zip)

---

## 🎯 What's New

This is the **initial release** of FreeTube for Kodi - bringing full FreeTube functionality to your Kodi media center!

### ✨ Features

#### Core Functionality
- ✅ **YouTube without Google Account** - Access YouTube without authentication
- ✅ **Innertube API Client** - Direct YouTube access (no API keys needed)
- ✅ **Invidious Fallback** - Automatic fallback to privacy-preserving proxies
- ✅ **Local Data Storage** - All subscriptions, history, playlists stored locally

#### Subscriptions & History
- ✅ **Channel Subscriptions** - Subscribe to channels without Google account
- ✅ **Subscription Feed** - View latest videos from subscribed channels
- ✅ **Watch History** - Track viewed videos locally
- ✅ **Search History** - Save search queries locally

#### Playlists & Profiles
- ✅ **Local Playlists** - Create and manage playlists without YouTube account
- ✅ **Multiple Profiles** - Separate profiles with independent subscriptions/history
- ✅ **Profile Management** - Create, delete, switch between profiles

#### Import/Export
- ✅ **YouTube CSV Import** - Import subscriptions from YouTube Takeout
- ✅ **FreeTube .db Import** - Import from FreeTube desktop app
- ✅ **NewPipe JSON Import** - Import from NewPipe Android app
- ✅ **OPML Import** - Import from RSS readers
- ✅ **Multi-format Export** - Export to all above formats

#### Privacy Features
- ✅ **No Tracking** - No Google cookies or tracking
- ✅ **No Authentication** - No OAuth, no API keys
- ✅ **Optional History** - Disable history tracking if desired
- ✅ **Auto Cleanup** - Automatic old data cleanup

#### Advanced Features
- ✅ **SponsorBlock Integration** - Skip sponsors, intros, outros, etc.
- ✅ **DeArrow Support** - Better video titles and thumbnails
- ✅ **Background Service** - API health checks, automatic maintenance
- ✅ **API Fallback System** - Automatic switching between backends

#### Navigation
- ✅ **Search** - Full YouTube search with suggestions
- ✅ **Trending** - Browse trending videos
- ✅ **Channel Browsing** - View channel content
- ✅ **Video Playback** - HD video streaming with quality selection

---

## 📦 Installation

### Method 1: Install from ZIP (Recommended)

1. **Download**: [plugin.video.freetube-1.0.0.zip](https://github.com/georgehuble/plugin.video.freetube/releases/download/v1.0.0/plugin.video.freetube-1.0.0.zip)

2. **Enable Unknown Sources**:
   - Kodi: Settings → System → Add-ons
   - Enable "Unknown sources" → Yes

3. **Install**:
   - Settings → Add-ons → Install from zip file
   - Navigate to downloaded ZIP
   - Select and install

4. **Launch**:
   - Videos → Video add-ons → FreeTube for Kodi

See [KODI_ZIP_INSTALL.md](https://github.com/georgehuble/plugin.video.freetube/blob/master/KODI_ZIP_INSTALL.md) for detailed instructions.

### Method 2: Manual Installation

See [INSTALL.md](https://github.com/georgehuble/plugin.video.freetube/blob/master/INSTALL.md)

---

## 📖 Documentation

- **[Quick Start Guide](https://github.com/georgehuble/plugin.video.freetube/blob/master/QUICK_START.md)** - 5-minute setup
- **[Installation Guide](https://github.com/georgehuble/plugin.video.freetube/blob/master/INSTALL.md)** - Detailed installation
- **[Kodi ZIP Install](https://github.com/georgehuble/plugin.video.freetube/blob/master/KODI_ZIP_INSTALL.md)** - ZIP installation walkthrough
- **[Project Summary](https://github.com/georgehuble/plugin.video.freetube/blob/master/PROJECT_SUMMARY.md)** - Architecture & technical details
- **[Completion Report](https://github.com/georgehuble/plugin.video.freetube/blob/master/COMPLETION_REPORT.md)** - Full feature list

---

## 🔧 Requirements

- **Kodi Version**: 19.0 (Matrix) or newer
- **Python**: 3.0+
- **Dependencies** (auto-installed):
  - `script.module.requests` (2.27.1+)
  - `inputstream.adaptive` (19.0.0+)
  - `script.module.inputstreamhelper` (0.6.0+, optional)

---

## 📊 Statistics

- **Files**: 32
- **Lines of Code**: 3250+
- **Python Modules**: 18
- **API Integrations**: 4 (Innertube, Invidious, SponsorBlock, DeArrow)
- **Database Tables**: 7
- **Settings Categories**: 8

---

## 🔒 Privacy & Security

### What This Plugin Does
- ✅ Accesses YouTube through Innertube API (no authentication)
- ✅ Stores data locally in SQLite database
- ✅ Optionally uses Invidious as privacy proxy
- ✅ No tracking, no analytics, no Google cookies

### What This Plugin Does NOT Do
- ❌ Does NOT require Google account
- ❌ Does NOT send tracking data
- ❌ Does NOT use YouTube API keys
- ❌ Does NOT use OAuth authentication
- ❌ Does NOT sync with Google servers

---

## 🐛 Known Issues

None reported yet! This is the initial release.

If you find any issues, please report them at:
https://github.com/georgehuble/plugin.video.freetube/issues

---

## 🔄 Upgrade Path

This is v1.0.0 - no upgrades available yet.

Future versions will support:
- In-place upgrades (install new ZIP over old version)
- Data preservation (subscriptions, history, playlists)
- Automatic migration if needed

---

## 🙏 Credits

### Inspired By
- **[FreeTubeApp/FreeTube](https://github.com/FreeTubeApp/FreeTube)** - Original FreeTube desktop application
- **[anxdpanic/plugin.video.youtube](https://github.com/anxdpanic/plugin.video.youtube)** - Kodi YouTube plugin
- **[LuanRT/YouTube.js](https://github.com/LuanRT/YouTube.js)** - Innertube API library

### APIs Used
- **YouTube Innertube API** - Direct YouTube access
- **Invidious API** - Privacy-preserving proxy
- **SponsorBlock API** - Skip video segments
- **DeArrow API** - Better titles & thumbnails

---

## 📜 License

**AGPL-3.0-or-later**

See [LICENSE](https://github.com/georgehuble/plugin.video.freetube/blob/master/LICENSE)

---

## ⚠️ Disclaimer

This plugin is not affiliated with, endorsed by, or connected to:
- YouTube
- Google Inc.
- FreeTube project
- Kodi Foundation

This is an independent third-party addon created for educational and personal use.

---

## 🎊 Enjoy!

**Watch YouTube without Google! 🍿📺**

For support, questions, or feedback:
- **Issues**: https://github.com/georgehuble/plugin.video.freetube/issues
- **Discussions**: https://github.com/georgehuble/plugin.video.freetube/discussions

---

**Previous Releases**: None (this is v1.0.0)  
**Next Release**: v1.1.0 (planned features TBD)

