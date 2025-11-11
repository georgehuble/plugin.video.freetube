# Building FreeTube for Kodi

## Development Setup

1. Clone repository:
```bash
git clone https://github.com/yourusername/plugin.video.freetube.git
cd plugin.video.freetube
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Link to Kodi addons directory:
```bash
# Linux/macOS
ln -s $(pwd)/plugin.video.freetube ~/.kodi/addons/

# Windows (run as admin)
mklink /D "%APPDATA%\Kodi\addons\plugin.video.freetube" "%CD%\plugin.video.freetube"
```

4. Enable debug logging in Kodi:
   - Settings → System → Logging
   - Enable "Enable debug logging"

## Testing

Run tests:
```bash
python -m pytest tests/
```

## Building Release

Create release ZIP:
```bash
python build.py
```

Output: `plugin.video.freetube-X.Y.Z.zip`

## Code Structure

```
plugin.video.freetube/
├── addon.xml                 # Addon metadata
├── resources/
│   ├── lib/
│   │   ├── plugin.py         # Entry point
│   │   ├── service.py        # Background service
│   │   └── freetube/         # Main package
│   │       ├── api/          # API clients
│   │       │   ├── innertube.py
│   │       │   └── invidious.py
│   │       ├── storage/      # Database layer
│   │       │   ├── database.py
│   │       │   ├── subscriptions.py
│   │       │   ├── history.py
│   │       │   ├── profiles.py
│   │       │   └── playlists.py
│   │       ├── integrations/ # SponsorBlock, DeArrow
│   │       │   ├── sponsorblock.py
│   │       │   └── dearrow.py
│   │       ├── provider.py   # Main logic
│   │       └── utils.py      # Utilities
│   ├── settings.xml          # Settings definition
│   └── language/             # Translations
└── LICENSES/                 # License files
```

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## Coding Standards

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions/classes
- Write tests for new features
- Keep Python 2/3 compatibility (use `from __future__ import`)

## License

AGPL-3.0-or-later
