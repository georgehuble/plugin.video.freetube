# FreeTube for Kodi - Project Summary

## 🎯 Project Overview

**FreeTube for Kodi** is a complete Kodi addon that brings FreeTube's privacy-first YouTube experience to Kodi media centers. Watch YouTube without Google account, manage subscriptions locally, and enjoy ad-free viewing with SponsorBlock.

## ✨ Key Features

### Privacy-First
- ✅ **No Google Authentication Required** - Access YouTube without logging in
- ✅ **Local Data Storage** - All subscriptions, history, and playlists stored locally
- ✅ **No Tracking** - No analytics, no cookies sent to Google
- ✅ **Invidious Support** - Use privacy-preserving proxy servers

### Full YouTube Access
- ✅ **Search** - Full YouTube search functionality
- ✅ **Trending** - Browse trending videos
- ✅ **Channels** - View channel content
- ✅ **Playlists** - Browse YouTube playlists
- ✅ **Video Playback** - HD video streaming

### Local Management
- ✅ **Subscriptions** - Subscribe to channels without account
- ✅ **Watch History** - Track viewed videos locally
- ✅ **Local Playlists** - Create and manage playlists
- ✅ **Multiple Profiles** - Separate profiles with independent data
- ✅ **Search History** - Local search history

### Advanced Features
- ✅ **SponsorBlock** - Skip sponsors, intros, outros automatically
- ✅ **DeArrow** - Better video titles and thumbnails
- ✅ **Import/Export** - Import subscriptions from YouTube, FreeTube, NewPipe
- ✅ **API Fallback** - Automatic fallback between Innertube and Invidious

## 🏗️ Architecture

### Technology Stack
- **Language**: Python 3.0+
- **Framework**: Kodi Plugin API
- **Database**: SQLite
- **APIs**: YouTube Innertube API, Invidious API
- **Integrations**: SponsorBlock, DeArrow

### Core Components

#### 1. API Layer (`freetube/api/`)
- **innertube.py** - Direct YouTube access without authentication
  - Uses Innertube API (YouTube's internal API)
  - Mimics web client requests
  - No OAuth/API keys required
  - Supports search, video info, channels, playlists
  
- **invidious.py** - Privacy-preserving proxy
  - Connects to public Invidious instances
  - Automatic instance health checks
  - Fallback when Innertube fails

#### 2. Storage Layer (`freetube/storage/`)
- **database.py** - SQLite database management
  - Tables: profiles, subscriptions, history, playlists, playlist_videos
  - Transaction management
  - Data export/import
  
- **subscriptions.py** - Subscription management
  - Subscribe/unsubscribe
  - Search subscriptions
  - Import from YouTube CSV, FreeTube DB, OPML, NewPipe JSON
  - Export to multiple formats
  
- **history.py** - Watch history tracking
  - Add to history
  - Search history
  - Watch progress tracking
  - Export/import history
  
- **profiles.py** - Multi-profile support
  - Create/delete profiles
  - Switch profiles
  - Profile statistics
  
- **playlists.py** - Local playlist management
  - Create/delete playlists
  - Add/remove videos
  - Reorder videos

#### 3. Integration Layer (`freetube/integrations/`)
- **sponsorblock.py** - SponsorBlock integration
  - Fetch skip segments
  - Skip categories: sponsor, intro, outro, etc.
  - Submission support
  
- **dearrow.py** - DeArrow integration
  - Fetch community titles
  - Fetch community thumbnails
  - Submission support

#### 4. Provider Layer (`freetube/`)
- **provider.py** - Main plugin logic
  - Route handling
  - UI generation
  - Video playback
  - Context menu handling
  
- **utils.py** - Helper utilities
  - Subscription import/export
  - Duration formatting
  - Number formatting
  - Dialog helpers

#### 5. Entry Points
- **plugin.py** - Main entry point
- **service.py** - Background service
  - API health checks
  - Data cleanup
  - Periodic tasks

## 📊 Data Flow

### Video Playback Flow
```
User selects video
    ↓
provider.py: play_video()
    ↓
API client: get_video_info()
    ↓
Parse formats & select quality
    ↓
Set playback URL
    ↓
Add to history (if enabled)
    ↓
Play video
```

### Subscription Flow
```
User subscribes to channel
    ↓
provider.py: subscribe action
    ↓
subscriptions.py: subscribe()
    ↓
database.py: INSERT INTO subscriptions
    ↓
Show notification
```

### API Fallback Flow
```
Primary API call fails
    ↓
Check if fallback enabled
    ↓
Try fallback API
    ↓
If successful, continue
    ↓
If fails, show error
```

## 🔐 Privacy Approach

### What Data is Stored
- ✅ Subscriptions (channel IDs and names)
- ✅ Watch history (video IDs, titles, timestamps)
- ✅ Local playlists
- ✅ Search history
- ✅ Profile settings

### What is NOT Stored
- ❌ Google account credentials
- ❌ Google cookies
- ❌ Tracking IDs
- ❌ Analytics data

### Network Requests
- **Innertube API**: Direct to YouTube servers
  - Headers set to mimic web browser
  - No authentication headers
  - Minimal tracking
  
- **Invidious API**: Through privacy proxy
  - Request goes to Invidious instance
  - Invidious fetches from YouTube
  - Additional privacy layer

## 📈 Performance

### Optimizations
- Local caching of API responses
- Lazy loading of subscription feeds
- Database indexing on frequent queries
- Background service for health checks
- Progress dialogs for long operations

### Resource Usage
- **Database**: ~10-50 MB (depends on history size)
- **Memory**: ~50-100 MB during operation
- **Network**: Variable (depends on video quality)

## 🔧 Configuration

### Settings Categories
1. **API Settings** - Backend configuration
2. **Content Settings** - Language, region, quality
3. **Privacy Settings** - History, cleanup
4. **Subscriptions** - Import/export
5. **SponsorBlock** - Skip categories
6. **DeArrow** - Title/thumbnail replacement
7. **Profiles** - Profile management
8. **Advanced** - Debug, cache, backup

## 🚀 Future Enhancements

### Potential Features
- [ ] Sync between devices (optional cloud backend)
- [ ] Download videos for offline viewing
- [ ] Live stream support improvements
- [ ] Comments viewing
- [ ] Channel community posts
- [ ] Chapters support
- [ ] Queue management
- [ ] Skin integration improvements

### Technical Improvements
- [ ] Unit tests coverage
- [ ] Integration tests
- [ ] Performance profiling
- [ ] Memory optimization
- [ ] Better error handling
- [ ] Localization (more languages)

## 📝 Credits

### Inspired By
- [FreeTubeApp/FreeTube](https://github.com/FreeTubeApp/FreeTube) - Original FreeTube application
- [anxdpanic/plugin.video.youtube](https://github.com/anxdpanic/plugin.video.youtube) - Kodi YouTube plugin
- [LuanRT/YouTube.js](https://github.com/LuanRT/YouTube.js) - Innertube API library

### APIs Used
- YouTube Innertube API (internal YouTube API)
- Invidious API (privacy-preserving proxy)
- SponsorBlock API (skip segments)
- DeArrow API (better titles/thumbnails)

## 📜 License

AGPL-3.0-or-later

## 🤝 Contributing

Contributions welcome! See BUILD.md for development setup.

## ⚠️ Disclaimer

This plugin is not affiliated with, endorsed by, or connected to:
- YouTube
- Google Inc.
- FreeTube project
- Kodi Foundation

This is an independent third-party addon.

