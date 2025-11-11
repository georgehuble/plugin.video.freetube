# FreeTube for Kodi - Installation Guide

## Requirements

- **Kodi Version**: 19.0 (Matrix) or newer
- **Python**: 3.0+
- **Dependencies**:
  - `script.module.requests` (2.27.1+)
  - `inputstream.adaptive` (19.0.0+)
  - `script.module.inputstreamhelper` (0.6.0+, optional)

## Installation Methods

### Method 1: From Repository (Recommended)

1. Open Kodi
2. Go to **Settings → Add-ons → Install from repository**
3. Find **FreeTube for Kodi** in Video add-ons
4. Click Install
5. Wait for dependencies to install
6. Done!

### Method 2: From ZIP File

1. Download the latest release ZIP file
2. Open Kodi
3. Go to **Settings → Add-ons → Install from zip file**
4. Navigate to the downloaded ZIP
5. Select the file and wait for installation
6. Done!

### Method 3: Manual Installation

1. Clone or download this repository
2. Copy the `plugin.video.freetube` folder to:
   - **Windows**: `%APPDATA%\Kodi\addons\`
   - **Linux**: `~/.kodi/addons/`
   - **macOS**: `~/Library/Application Support/Kodi/addons/`
   - **Android**: `/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/`
3. Restart Kodi
4. Enable the add-on in **Settings → Add-ons → My add-ons → Video add-ons**

## First Run Setup

### 1. Choose API Backend

Go to **Settings → API Settings** and choose:

- **Local (Innertube)** - Direct YouTube access (recommended)
- **Invidious** - Use public Invidious instances (more private)

### 2. Configure Language & Region

Go to **Settings → Content Settings**:

- **Content Language**: e.g., "en" for English, "ru" for Russian
- **Content Region**: e.g., "US" for United States, "RU" for Russia

### 3. Enable Privacy Features (Optional)

Go to **Settings → Privacy Settings**:

- Enable/disable watch history
- Enable/disable search history
- Configure auto-cleanup

### 4. Enable SponsorBlock (Optional)

Go to **Settings → SponsorBlock**:

- Enable SponsorBlock
- Choose categories to skip (sponsors, intros, outros, etc.)

### 5. Import Subscriptions (Optional)

If you have existing subscriptions:

1. Go to **Settings → Subscriptions → Import Subscriptions**
2. Select your subscription file:
   - YouTube CSV export
   - FreeTube .db file
   - NewPipe JSON export
   - OPML file

## Usage

### Subscribing to Channels

1. Find a channel or video
2. Open context menu (C key or long press)
3. Select "Subscribe"
4. Channel will appear in **Subscriptions** menu

### Creating Playlists

1. Go to **Playlists** menu
2. Create new playlist
3. Add videos from context menu: "Add to Playlist"

### Multiple Profiles

1. Go to **Profiles** menu
2. Create new profile
3. Each profile has separate subscriptions and history

## Troubleshooting

### Videos Won't Play

1. Check **Settings → API Settings → Enable API Fallback**
2. Try switching API backend (Local ↔ Invidious)
3. Check your internet connection
4. Clear cache: **Settings → Advanced → Clear All Data**

### Invidious Instance Not Working

1. Go to **Settings → API Settings → Find Working Instance**
2. Plugin will automatically find a working instance

### Subscriptions Not Loading

1. Go to **Subscriptions** menu
2. If empty, subscribe to channels first
3. Check **Subscriptions Feed** for latest videos

### Database Errors

1. Go to **Settings → Advanced → Export All Data** (backup)
2. Go to **Settings → Privacy → Clear All Data**
3. Go to **Settings → Advanced → Import All Data** (restore)

## Updating

### From Repository

Updates are automatic when available.

### Manual Update

1. Download new version
2. Install over existing installation
3. Data will be preserved

## Uninstalling

1. Go to **Settings → Add-ons → My add-ons → Video add-ons**
2. Select **FreeTube for Kodi**
3. Click **Uninstall**
4. To remove all data:
   - **Windows**: Delete `%APPDATA%\Kodi\userdata\addon_data\plugin.video.freetube\`
   - **Linux**: Delete `~/.kodi/userdata/addon_data/plugin.video.freetube/`

## Support

- **Issues**: https://github.com/yourusername/plugin.video.freetube/issues
- **Forum**: https://forum.kodi.tv
- **Wiki**: https://github.com/yourusername/plugin.video.freetube/wiki

## Privacy Notice

This plugin:
- ✅ Does NOT require Google account
- ✅ Does NOT send tracking data
- ✅ Stores all data locally
- ✅ Uses privacy-first APIs
- ⚠️ Still connects to YouTube/Invidious servers to fetch content

For maximum privacy, use Invidious backend with a VPN/Tor.

