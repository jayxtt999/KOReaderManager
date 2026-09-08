# KOReader Manager

A Windows GUI tool for managing KOReader plugins and ebooks on jailbroken Kindle devices.

## Features

### Plugin Management
- List all installed KOReader plugins with full name, description, file count, and size
- Enable / Disable / Uninstall plugins
- View plugin details (parsed from `_meta.lua`)

### Plugin Market
- Browse 34+ popular KOReader plugins from the community catalog
- One-click install from GitHub repositories
- Install from custom GitHub repo URL
- Install from local ZIP file
- Uninstall installed plugins directly from the market list
- Installed status indicator for each catalog entry

### Book Management
- Scan and list all ebooks on Kindle (EPUB, PDF, MOBI, AZW3, CBZ, TXT, FB2, DJVU, DOCX)
- Custom book directory path (defaults to `documents`)
- Import books from PC to Kindle with progress bar
- Delete books with confirmation and progress bar
- Double-click to open book with default PC application
- Right-click context menu: Open, Locate in Explorer, Details, Delete

### Backup & Restore
- Backup entire `koreader` directory to a ZIP file
- Restore from a previously created backup

### Log Viewer
- View `crash.log` for troubleshooting
- View `version.log` for version info

### Cleanup & Maintenance
- One-click cleanup of cache files, screenshots, residual `.bin` update files
- Remove `fill_disk` filler folders (from jailbreak process)
- Remove SpiderCat jailbreak files
- Shows disk space before and after cleanup

### Device Connection
- Auto-detect Kindle drive letter and volume label
- Manual drive letter selection from dropdown
- Browse for custom directory path
- Real-time disk space display

## Screenshots

| Tab | Description |
|-----|-------------|
| Plugin Management | List, enable/disable, uninstall plugins |
| Book Management | Scan, import, delete, open ebooks |
| Plugin Market | Browse and install 34+ community plugins |
| Backup & Restore | Backup/restore koreader directory |
| Log Viewer | View crash.log and version.log |
| Cleanup | Clean cache, filler files, jailbreak residue |

## Requirements

- Windows 10/11 (64-bit)
- Kindle connected via USB (mass storage mode)
- KOReader installed on Kindle (`koreader/` directory at root)

## Download

Download the latest release from the [Releases](../../releases) page:

- `KOReaderManager.exe` — Standalone executable, no installation required

## Usage

1. Connect your Kindle to your PC via USB
2. Run `KOReaderManager.exe`
3. Click "Auto Detect" or select your Kindle drive from the dropdown
4. Click "Connect"
5. Use the tabs to manage plugins, books, and more

## Build from Source

```bash
git clone https://github.com/your-username/KOReaderManager.git
cd KOReaderManager
pip install pyinstaller
pyinstaller KOReaderManager.py --onefile --windowed --name KOReaderManager
```

## Plugin Catalog

The built-in catalog includes plugins from these categories:

| Category | Examples |
|----------|----------|
| Store | AppStore, Storefront |
| UI | SimpleUI, ZenUI, ProjectTitle |
| Reading | CoverBrowser, CoverImage, ZenUI |
| Tools | KOAssistant, UpdatesManager, SSH |
| Audio | KinAMP, LARK |
| Learning | KAnki, AskAI |
| Games | Gambatte-K2, KWordle, Tetris, Chess |
| System | AutoSuspend, AutoStandby, BatteryStat |
| Dev | kTerm, UsbNetLite, ScreenControl |

## License

MIT License - feel free to modify and distribute.

## Acknowledgments

- [KOReader](https://github.com/koreader/koreader) — The best ebook reader for e-ink devices
- [KindleModding](https://kindlemodding.org/) — Kindle jailbreak community
- [SpiderCat](https://kindlemodding.org/jailbreaking/SpiderCat/) — Easiest Kindle jailbreak method
- All plugin authors whose work is included in the catalog
