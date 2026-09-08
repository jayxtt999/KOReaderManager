import os
import sys
import shutil
import json
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import urllib.request
import urllib.parse
import tempfile
import zipfile
import threading
import re
from datetime import datetime

KINDLE_LABEL = "Kindle"
PLUGINS_DIR_REL = "koreader/plugins"
SETTINGS_DIR_REL = "koreader/settings"
KOREADER_DIR_REL = "koreader"
CRASH_LOG = "koreader/crash.log"
VERSION_LOG = "koreader/version.log"

PLUGIN_CATALOG = [
    {"name": "AppStore", "repo": "omer-faruq/appstore.koplugin", "category": "商店", "description": "KOReader 插件商店，浏览/搜索/一键安装其他插件"},
    {"name": "Storefront", "repo": "ultimatejimmy/storefront.koplugin", "category": "商店", "description": "另一个插件商店，界面风格不同"},
    {"name": "SimpleUI", "repo": "doctorhetfield-cmd/simpleui.koplugin", "category": "美化", "description": "KOReader 界面美化，自定义底栏/快捷操作"},
    {"name": "ZenUI", "repo": "AnthonyGress/zen_ui.koplugin", "category": "美化", "description": "Zen 风格 UI 美化，简洁优雅的界面主题"},
    {"name": "CoverBrowser", "repo": "robert006o/koreader-coverbrowser", "category": "美化", "description": "书架封面墙浏览，支持列表/网格视图切换"},
    {"name": "觅阅 (WeRead)", "repo": "finlater/weread.koplugin", "category": "阅读", "description": "微信读书插件，书架浏览/全书下载/进度同步/划线/书评"},
    {"name": "AskAI", "repo": "abhignan-rakshith/kindle-askai", "category": "阅读", "description": "AI 阅读伴侣，选词翻译/总结/问答"},
    {"name": "KOAssistant", "repo": "zeeyado/koassistant.koplugin", "category": "工具", "description": "KOReader 助手，快捷操作和自动化"},
    {"name": "UpdatesManager", "repo": "advokatb/updatesmanager.koplugin", "category": "工具", "description": "插件更新管理器，批量检查和更新已安装插件"},
    {"name": "Bluetooth翻页器", "repo": "QiuYukang/kindlebtcontroller.koplugin", "category": "工具", "description": "蓝牙手柄/遥控器翻页，支持音频输出"},
    {"name": "KinAMP", "repo": "pkkbj/kindleinamp.koplugin", "category": "音频", "description": "蓝牙连接听音乐，支持播放列表"},
    {"name": "LARK", "repo": "elverb/lark.koplugin", "category": "音频", "description": "有声书播放器，支持封面显示和章节导航"},
    {"name": "dtDisplay Clock", "repo": "zeroxia/dtdisplay-clock.koplugin", "category": "工具", "description": "全屏时钟，常显时间和日期"},
    {"name": "KOWeather", "repo": "smacz/koweather.koplugin", "category": "工具", "description": "在 KOReader 中查看天气预报"},
    {"name": "PIN Lock Screen", "repo": "robert006o/pinlock.koplugin", "category": "工具", "description": "KOReader 密码锁屏，保护隐私"},
    {"name": "ProjectTitle", "repo": "davidgarea/projecttitle.koplugin", "category": "美化", "description": "KOReader 书架视图增强，封面墙浏览"},
    {"name": "KAnki", "repo": "ptechan/kanki.koplugin", "category": "学习", "description": "Anki 记忆卡片，用 Kindle 背单词"},
    {"name": "KPomo", "repo": "pkkbj/kpomo.koplugin", "category": "工具", "description": "番茄钟计时器，专注阅读辅助"},
    {"name": "Kreate", "repo": "pkkbj/kreate.koplugin", "category": "工具", "description": "Kindle 绘画工具"},
    {"name": "kTerm", "repo": "elverb/kterm.koplugin", "category": "开发", "description": "E-ink 优化终端，在 Kindle 上执行命令"},
    {"name": "UsbNetLite", "repo": "elverb/usbnetlite.koplugin", "category": "开发", "description": "SSH 远程连接 Kindle，无需 USB"},
    {"name": "ScreenControl", "repo": "elverb/screencontrol.koplugin", "category": "开发", "description": "在线投屏，远程操控 Kindle"},
    {"name": "Gambatte-K2", "repo": "pkkbj/gambatte-k2.koplugin", "category": "游戏", "description": "Game Boy 模拟器，支持蓝牙音频"},
    {"name": "KWordle", "repo": "pkkbj/kwordle.koplugin", "category": "游戏", "description": "Kindle 版 Wordle 猜词游戏"},
    {"name": "IllusionChess", "repo": "pkkbj/illusionchess.koplugin", "category": "游戏", "description": "快速国际象棋"},
    {"name": "Tetris", "repo": "pkkbj/tetris.koplugin", "category": "游戏", "description": "俄罗斯方块"},
    {"name": "Disable ADs", "repo": "phrdbt/disableads.koplugin", "category": "系统", "description": "去除 Kindle 锁屏广告"},
    {"name": "Wallberry", "repo": "pkkbj/wallberry.koplugin", "category": "美化", "description": "自定义锁屏壁纸，支持定时更换"},
    {"name": "AutoSuspend", "repo": "pkkbj/autosuspend.koplugin", "category": "系统", "description": "自动休眠管理，省电优化"},
    {"name": "KOSync", "repo": "ozunes/kosync.koplugin", "category": "阅读", "description": "多设备阅读进度同步"},
    {"name": "WordDict", "repo": "koreader/worddict.koplugin", "category": "阅读", "description": "划词查词典，支持多语言"},
    {"name": "Translator", "repo": "koreader/translator.koplugin", "category": "阅读", "description": "划词翻译，支持多引擎"},
    {"name": "PokeInfo", "repo": "phrdbt/pokeinfo.koplugin", "category": "工具", "description": "状态栏显示时间/电量/页数等信息"},
]

PLUGIN_CATEGORIES = ["全部", "商店", "美化", "阅读", "工具", "音频", "学习", "游戏", "系统", "开发"]


class KindleManager:
    @staticmethod
    def find_kindle():
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-Volume | Where-Object { $_.FileSystemLabel -eq 'Kindle' } | Select-Object -ExpandProperty DriveLetter"],
                capture_output=True, text=True, timeout=10)
            letter = result.stdout.strip()
            if letter and os.path.exists(f"{letter}:\\"):
                return f"{letter}:\\"
        except Exception:
            pass
        for letter in "DEFGHIJKLMNOP":
            drive = f"{letter}:\\"
            if os.path.exists(drive) and os.path.exists(os.path.join(drive, "koreader")):
                return drive
        return None

    @staticmethod
    def detect_all_drives():
        drives = []
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-Volume | Sort-Object DriveLetter | Select-Object DriveLetter, FileSystemLabel, @{N='Size';E={$_.Size}}, @{N='Free';E={$_.SizeRemaining}} | Format-List"],
                capture_output=True, text=True, timeout=10)
            blocks = result.stdout.strip().split("\n\n")
            for block in blocks:
                info = {}
                for line in block.strip().split("\n"):
                    if ":" in line:
                        key, val = line.split(":", 1)
                        info[key.strip()] = val.strip()
                letter = info.get("DriveLetter", "")
                if letter and os.path.exists(f"{letter}:\\"):
                    label = info.get("FileSystemLabel", "")
                    drives.append({
                        "path": f"{letter}:\\",
                        "label": label,
                        "has_koreader": os.path.exists(os.path.join(f"{letter}:\\", "koreader")),
                    })
        except Exception:
            pass
        for letter in "DEFGHIJKLMNOP":
            drive = f"{letter}:\\"
            if os.path.exists(drive) and not any(d["path"] == drive for d in drives):
                drives.append({
                    "path": drive,
                    "label": "",
                    "has_koreader": os.path.exists(os.path.join(drive, "koreader")),
                })
        return drives

    @staticmethod
    def parse_meta_lua(meta_path):
        meta = {}
        try:
            with open(meta_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            patterns = {
                "fullname": r'fullname\s*=\s*_\(\s*\[=*\[(.*?)\]=*\]\s*\)|fullname\s*=\s*_\(\s*"(.*?)"\s*\)|fullname\s*=\s*"(.*?)"',
                "description": r'description\s*=\s*_\(\s*\[=*\[(.*?)\]=*\]\s*\)|description\s*=\s*_\(\s*"(.*?)"\s*\)|description\s*=\s*"(.*?)"',
                "name": r'name\s*=\s*"(.*?)"',
            }
            for key, pat in patterns.items():
                m = re.search(pat, content, re.DOTALL)
                if m:
                    val = None
                    for g in m.groups():
                        if g:
                            val = g.strip()
                            break
                    if val:
                        meta[key] = val
        except Exception:
            pass
        return meta

    @staticmethod
    def get_plugins(kindle_drive):
        plugins_path = os.path.join(kindle_drive, PLUGINS_DIR_REL)
        if not os.path.exists(plugins_path):
            return []
        plugins = []
        for name in sorted(os.listdir(plugins_path)):
            full = os.path.join(plugins_path, name)
            meta = os.path.join(full, "_meta.lua")
            main_lua = os.path.join(full, "main.lua")
            if os.path.isdir(full) and (os.path.exists(meta) or os.path.exists(main_lua)):
                disabled = name.endswith(".disabled")
                file_count = sum(len(files) for _, _, files in os.walk(full))
                size = 0
                for dirpath, _, files in os.walk(full):
                    for f in files:
                        fp = os.path.join(dirpath, f)
                        try:
                            size += os.path.getsize(fp)
                        except Exception:
                            pass
                meta_info = KindleManager.parse_meta_lua(meta) if os.path.exists(meta) else {}
                description = meta_info.get("description", "")
                fullname = meta_info.get("fullname", "")
                plugins.append({
                    "name": name,
                    "path": full,
                    "disabled": disabled,
                    "files": file_count,
                    "size_kb": round(size / 1024, 1),
                    "has_meta": os.path.exists(meta),
                    "fullname": fullname,
                    "description": description
                })
        return plugins

    @staticmethod
    def toggle_plugin(plugin_info, enable):
        old_path = plugin_info["path"]
        name = plugin_info["name"]
        if name.endswith(".disabled"):
            name = name[:-len(".disabled")]
        if enable:
            new_path = old_path.replace(".disabled", "")
        else:
            if not old_path.endswith(".disabled"):
                new_path = old_path + ".disabled"
            else:
                new_path = old_path
        if old_path != new_path:
            try:
                os.rename(old_path, new_path)
                return True
            except Exception as e:
                print(f"Error toggling plugin: {e}")
        return False

    @staticmethod
    def delete_plugin(plugin_info):
        path = plugin_info["path"]
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
            return not os.path.exists(path)
        return False

    @staticmethod
    def install_from_github(repo, status_callback, kindle_drive):
        temp_dir = tempfile.mkdtemp(prefix="koreader_install_")
        try:
            api_url = f"https://api.github.com/repos/{repo}/releases/latest"
            status_callback(f"获取 {repo} 最新版本...")
            req = urllib.request.Request(api_url, headers={"User-Agent": "KOReaderManager"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
            tag = data.get("tag_name", "unknown")
            zip_url = data.get("zipball_url", "")
            if not zip_url:
                status_callback("未找到下载链接!")
                return False
            status_callback(f"最新版本: {tag}, 下载中...")
            zip_path = os.path.join(temp_dir, "plugin.zip")
            req2 = urllib.request.Request(zip_url, headers={"User-Agent": "KOReaderManager"})
            with urllib.request.urlopen(req2, timeout=120) as resp2:
                with open(zip_path, "wb") as f:
                    while True:
                        chunk = resp2.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
            status_callback("解压中...")
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(temp_dir)
            extracted_dirs = [d for d in os.listdir(temp_dir)
                              if os.path.isdir(os.path.join(temp_dir, d)) and d != "plugin.zip"]
            if not extracted_dirs:
                status_callback("解压失败!")
                return False
            extracted_path = os.path.join(temp_dir, extracted_dirs[0])
            meta_path = os.path.join(extracted_path, "_meta.lua")
            if os.path.exists(meta_path):
                plugin_name = f"{repo.split('/')[-1].replace('.koplugin', '')}.koplugin"
                dest = os.path.join(kindle_drive, PLUGINS_DIR_REL, plugin_name)
            else:
                sub = None
                for d in os.listdir(extracted_path):
                    if os.path.exists(os.path.join(extracted_path, d, "_meta.lua")):
                        sub = d
                        break
                if sub:
                    extracted_path = os.path.join(extracted_path, sub)
                    plugin_name = sub
                else:
                    plugin_name = f"{repo.split('/')[-1]}.koplugin"
                dest = os.path.join(kindle_drive, PLUGINS_DIR_REL, plugin_name)
            if os.path.exists(dest):
                shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(extracted_path, dest)
            status_callback(f"安装成功: {plugin_name}")
            return True
        except Exception as e:
            status_callback(f"安装失败: {e}")
            return False
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def install_from_zip(zip_path, kindle_drive):
        temp_dir = tempfile.mkdtemp(prefix="koreader_zip_")
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(temp_dir)
            extracted_dirs = [d for d in os.listdir(temp_dir)
                              if os.path.isdir(os.path.join(temp_dir, d))]
            installed = []
            for d in extracted_dirs:
                full = os.path.join(temp_dir, d)
                if os.path.exists(os.path.join(full, "_meta.lua")) or \
                   os.path.exists(os.path.join(full, "main.lua")):
                    dest = os.path.join(kindle_drive, PLUGINS_DIR_REL, d)
                    if os.path.exists(dest):
                        shutil.rmtree(dest, ignore_errors=True)
                    shutil.copytree(full, dest)
                    installed.append(d)
            if not installed:
                for d in extracted_dirs:
                    full = os.path.join(temp_dir, d)
                    for sub in os.listdir(full):
                        subfull = os.path.join(full, sub)
                        if os.path.isdir(subfull) and \
                           (os.path.exists(os.path.join(subfull, "_meta.lua")) or
                            os.path.exists(os.path.join(subfull, "main.lua"))):
                            dest = os.path.join(kindle_drive, PLUGINS_DIR_REL, sub)
                            if os.path.exists(dest):
                                shutil.rmtree(dest, ignore_errors=True)
                            shutil.copytree(subfull, dest)
                            installed.append(sub)
            return installed
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def backup(kindle_drive, backup_path):
        koreader_dir = os.path.join(kindle_drive, KOREADER_DIR_REL)
        if not os.path.exists(koreader_dir):
            return False
        shutil.make_archive(backup_path, "zip", koreader_dir)
        return os.path.exists(f"{backup_path}.zip")

    @staticmethod
    def get_logs(kindle_drive):
        logs = {}
        for log_file in [CRASH_LOG, VERSION_LOG]:
            path = os.path.join(kindle_drive, log_file)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    logs[os.path.basename(log_file)] = content[-5000:] if len(content) > 5000 else content
                except Exception as e:
                    logs[os.path.basename(log_file)] = f"读取失败: {e}"
        return logs

    @staticmethod
    def get_free_space(kindle_drive):
        try:
            total = 0
            used = 0
            for dirpath, dirnames, filenames in os.walk(kindle_drive):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        used += os.path.getsize(fp)
                    except Exception:
                        pass
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(kindle_drive), None, None, ctypes.byref(free_bytes))
            free_mb = free_bytes.value / (1024 * 1024)
            return {"free_mb": round(free_mb, 1), "used_mb": round(used / (1024 * 1024), 1)}
        except Exception:
            return {"free_mb": 0, "used_mb": 0}

    @staticmethod
    def clean_temp(kindle_drive):
        cleaned = []
        temp_items = [
            "koreader/cache",
            "koreader/clipboard",
            "koreader/screenshots",
        ]
        for item in temp_items:
            path = os.path.join(kindle_drive, item)
            if os.path.exists(path):
                try:
                    for f in os.listdir(path):
                        fp = os.path.join(path, f)
                        if os.path.isfile(fp):
                            os.remove(fp)
                    cleaned.append(item)
                except Exception:
                    pass
        bin_files = []
        root = kindle_drive
        for f in os.listdir(root):
            if f.endswith(".bin") or f.endswith(".partial"):
                bin_files.append(f)
                try:
                    os.remove(os.path.join(root, f))
                except Exception:
                    pass
        if bin_files:
            cleaned.append(f"删除更新文件: {', '.join(bin_files)}")
        filler_path = os.path.join(kindle_drive, "fill_disk")
        if os.path.exists(filler_path):
            shutil.rmtree(filler_path, ignore_errors=True)
            cleaned.append("fill_disk 文件夹")
        filler_script = os.path.join(kindle_drive, "Filler.ps1")
        if os.path.exists(filler_script):
            os.remove(filler_script)
            cleaned.append("Filler.ps1")
        spidercat = os.path.join(kindle_drive, "documents", "spidercat.azw3")
        if os.path.exists(spidercat):
            os.remove(spidercat)
            cleaned.append("spidercat.azw3")
        return cleaned


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("KOReader 管理工具")
        self.root.geometry("960x620")
        self.kindle_drive = None
        self.setup_ui()
        self.show_welcome()

    def show_welcome(self):
        win = tk.Toplevel(self.root)
        win.title("欢迎使用 KOReader 管理工具")
        win.geometry("520x560")
        win.transient(self.root)
        win.grab_set()
        win.resizable(False, False)
        win.configure(bg="#2b2b2b")

        header = tk.Label(win, text="KOReader 管理工具", font=("Segoe UI", 16, "bold"),
                         bg="#2b2b2b", fg="#4ec9b0")
        header.pack(pady=(15, 5))
        sub = tk.Label(win, text="操作说明", font=("Segoe UI", 11),
                       bg="#2b2b2b", fg="#e0e0e0")
        sub.pack(pady=(0, 10))

        text = tk.Text(win, bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 10),
                       wrap=tk.WORD, relief=tk.FLAT, padx=12, pady=12,
                       insertbackground="#e0e0e0")
        text.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 10))

        info = (
            "1. 连接 Kindle (三种方式)\n"
            "   • [自动识别] 扫描所有盘符，自动选中含 koreader 目录的盘\n"
            "   • [浏览...]   手动选择 Kindle 根目录(自定义路径/U盘模式)\n"
            "   • [下拉框]   从已检测到的盘符中手动选择，点「连接」\n\n"
            "2. 插件管理\n"
            "   查看已安装插件列表，支持启用/禁用/卸载/查看详情\n\n"
            "3. 安装插件\n"
            "   从 GitHub 一键下载安装(内置 10 个常用插件)\n"
            "   或从本地 ZIP 文件安装\n\n"
            "4. 备份恢复\n"
            "   备份整个 koreader 目录到本地 ZIP\n"
            "   支持从备份 ZIP 恢复\n\n"
            "5. 清理维护\n"
            "   一键清理缓存/截图/.bin残留/填充文件/越狱文件\n\n"
            "6. 日志查看\n"
            "   查看 crash.log 和 version.log 排查问题\n\n"
            "提示: 请确保 Kindle 已通过 USB 连接并在 U 盘模式下。"
        )
        text.insert("1.0", info)
        text.config(state=tk.DISABLED)

        btn = tk.Button(win, text="确定", command=win.destroy,
                        bg="#007acc", fg="white", font=("Segoe UI", 10, "bold"),
                        relief=tk.FLAT, padx=30, pady=6, cursor="hand2")
        btn.pack(pady=(0, 15))

        win.update_idletasks()
        cx = self.root.winfo_x() + (self.root.winfo_width() - 520) // 2
        cy = self.root.winfo_y() + (self.root.winfo_height() - 560) // 2
        win.geometry(f"+{max(0,cx)}+{max(0,cy)}")

        win.bind("<Return>", lambda e: win.destroy())
        win.bind("<Escape>", lambda e: win.destroy())
        self.root.wait_window(win)
        self.auto_detect()

    def setup_ui(self):
        menubar = tk.Menu(self.root, bg="#2b2b2b", fg="#e0e0e0", activebackground="#404040")
        self.root.config(menu=menubar)

        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Kindle 目录:", font=("Segoe UI", 10)).pack(side=tk.LEFT)

        self.drive_combo = ttk.Combobox(top, width=35, font=("Segoe UI", 9))
        self.drive_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(top, text="自动识别", command=self.auto_detect).pack(side=tk.LEFT, padx=3)
        ttk.Button(top, text="浏览...", command=self.browse_directory).pack(side=tk.LEFT, padx=3)
        ttk.Button(top, text="连接", command=self.manual_connect).pack(side=tk.LEFT, padx=3)
        ttk.Button(top, text="刷新列表", command=self.refresh_plugins).pack(side=tk.LEFT, padx=5)

        self.space_var = tk.StringVar(value="")
        ttk.Label(top, textvariable=self.space_var, font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=10)

        self.status_var = tk.StringVar(value="就绪")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        self.tab_plugins = ttk.Frame(notebook)
        notebook.add(self.tab_plugins, text="  插件管理  ")
        self.setup_plugins_tab()

        self.tab_books = ttk.Frame(notebook)
        notebook.add(self.tab_books, text="  图书管理  ")
        self.setup_books_tab()

        self.tab_install = ttk.Frame(notebook)
        notebook.add(self.tab_install, text="  安装插件  ")
        self.setup_install_tab()

        self.tab_backup = ttk.Frame(notebook)
        notebook.add(self.tab_backup, text="  备份恢复  ")
        self.setup_backup_tab()

        self.tab_logs = ttk.Frame(notebook)
        notebook.add(self.tab_logs, text="  日志查看  ")
        self.setup_logs_tab()

        self.tab_clean = ttk.Frame(notebook)
        notebook.add(self.tab_clean, text="  清理维护  ")
        self.setup_clean_tab()

        status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        ttk.Label(status_bar, textvariable=self.status_var, font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=8)

    def setup_plugins_tab(self):
        cols = ("name", "fullname", "status", "description", "files", "size")
        self.plugin_tree = ttk.Treeview(self.tab_plugins, columns=cols, show="headings", height=18)
        self.plugin_tree.heading("name", text="插件目录")
        self.plugin_tree.heading("fullname", text="全名")
        self.plugin_tree.heading("status", text="状态")
        self.plugin_tree.heading("description", text="描述")
        self.plugin_tree.heading("files", text="文件数")
        self.plugin_tree.heading("size", text="大小(KB)")
        self.plugin_tree.column("name", width=160)
        self.plugin_tree.column("fullname", width=120)
        self.plugin_tree.column("status", width=60)
        self.plugin_tree.column("description", width=280)
        self.plugin_tree.column("files", width=60)
        self.plugin_tree.column("size", width=80)
        self.plugin_tree.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        btn_frame = ttk.Frame(self.tab_plugins)
        btn_frame.pack(fill=tk.X, padx=4, pady=4)
        ttk.Button(btn_frame, text="启用", command=lambda: self.toggle_plugin(True)).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="禁用", command=lambda: self.toggle_plugin(False)).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="卸载", command=self.uninstall_plugin).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="查看详情", command=self.show_plugin_detail).pack(side=tk.LEFT, padx=3)
        self.plugin_tree.bind("<Double-1>", lambda e: self.show_plugin_detail())

    def setup_books_tab(self):
        top = ttk.Frame(self.tab_books, padding=6)
        top.pack(fill=tk.X)
        ttk.Label(top, text="书籍目录:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(4, 3))
        self.books_dir_var = tk.StringVar(value="documents")
        ttk.Entry(top, textvariable=self.books_dir_var, width=25).pack(side=tk.LEFT, padx=3)
        ttk.Button(top, text="浏览...", command=self.browse_books_dir).pack(side=tk.LEFT, padx=3)
        ttk.Button(top, text="刷新", command=self.refresh_books).pack(side=tk.LEFT, padx=3)
        ttk.Button(top, text="导入书籍", command=self.import_books).pack(side=tk.LEFT, padx=3)
        ttk.Button(top, text="删除选中", command=self.delete_books).pack(side=tk.LEFT, padx=3)

        cols = ("filename", "format", "size", "path")
        self.book_tree = ttk.Treeview(self.tab_books, columns=cols, show="headings", height=18)
        self.book_tree.heading("filename", text="文件名")
        self.book_tree.heading("format", text="格式")
        self.book_tree.heading("size", text="大小")
        self.book_tree.heading("path", text="路径")
        self.book_tree.column("filename", width=300)
        self.book_tree.column("format", width=60)
        self.book_tree.column("size", width=80)
        self.book_tree.column("path", width=300)
        self.book_tree.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.book_tree.bind("<Double-1>", lambda e: self.open_book_file())
        self.book_tree.bind("<Button-3>", self.on_book_right_click)
        self.book_menu = tk.Menu(self.root, tearoff=0)
        self.book_menu.add_command(label="打开书籍", command=self.open_book_file)
        self.book_menu.add_command(label="定位到目录", command=self.locate_book)
        self.book_menu.add_separator()
        self.book_menu.add_command(label="查看详情", command=self.show_book_detail)
        self.book_menu.add_command(label="删除", command=self.delete_books)

    def get_books_dir(self):
        if not self.kindle_drive:
            return None
        rel = self.books_dir_var.get().strip()
        if not rel:
            rel = "documents"
        return os.path.join(self.kindle_drive, rel.replace("/", os.sep))

    def browse_books_dir(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        current = self.get_books_dir()
        path = filedialog.askdirectory(title="选择书籍目录", initialdir=current or self.kindle_drive)
        if path:
            try:
                rel = os.path.relpath(path, self.kindle_drive)
            except Exception:
                rel = path
            self.books_dir_var.set(rel)
            self.refresh_books()

    def refresh_books(self):
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        if not self.kindle_drive:
            return
        books_dir = self.get_books_dir()
        if not books_dir or not os.path.isdir(books_dir):
            self.book_tree.insert("", tk.END, values=("目录不存在", "", "", books_dir or ""))
            return
        BOOK_EXTS = {".epub", ".pdf", ".mobi", ".azw3", ".azw", ".cbz", ".cbr", ".txt", ".fb2", ".djvu", ".docx"}
        books = []
        for dirpath, dirnames, filenames in os.walk(books_dir):
            for f in filenames:
                ext = os.path.splitext(f)[1].lower()
                if ext in BOOK_EXTS:
                    fp = os.path.join(dirpath, f)
                    try:
                        size = os.path.getsize(fp)
                    except Exception:
                        size = 0
                    books.append((f, ext.lstrip("."), size, fp))
        books.sort(key=lambda x: x[0].lower())
        if not books:
            self.book_tree.insert("", tk.END, values=("无书籍文件", "", "", ""))
            self.status_var.set("图书管理: 无书籍")
            return
        for fname, fmt, size, fpath in books:
            size_str = f"{size/1024/1024:.1f} MB" if size >= 1048576 else f"{size/1024:.0f} KB"
            try:
                rel_path = os.path.relpath(fpath, self.kindle_drive)
            except Exception:
                rel_path = fpath
            self.book_tree.insert("", tk.END, values=(fname, fmt.upper(), size_str, rel_path))
        total = len(books)
        total_size = sum(b[2] for b in books)
        total_str = f"{total_size/1024/1024:.1f} MB" if total_size >= 1048576 else f"{total_size/1024:.0f} KB"
        self.status_var.set(f"图书管理: {total} 本书, 共 {total_str}")

    def import_books(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        files = filedialog.askopenfilenames(
            title="选择要导入的电子书",
            filetypes=[("电子书", "*.epub *.pdf *.mobi *.azw3 *.azw *.cbz *.cbr *.txt *.fb2 *.djvu *.docx"),
                       ("所有文件", "*.*")])
        if not files:
            return
        books_dir = self.get_books_dir()
        if not os.path.isdir(books_dir):
            os.makedirs(books_dir, exist_ok=True)
        files_list = list(files)
        total = len(files_list)
        prog = tk.Toplevel(self.root)
        prog.title("导入进度")
        prog.geometry("400x120")
        prog.transient(self.root)
        prog.grab_set()
        ttk.Label(prog, text=f"正在导入 0/{total}...", font=("Segoe UI", 10)).pack(pady=10)
        pb = ttk.Progressbar(prog, maximum=total, value=0, length=360)
        pb.pack(pady=5)
        info_lbl = ttk.Label(prog, text="", font=("Segoe UI", 8))
        info_lbl.pack(pady=2)
        prog.update()
        imported = 0
        errors = []
        for i, src in enumerate(files_list):
            fname = os.path.basename(src)
            info_lbl.config(text=fname)
            prog.title(f"导入进度 {i+1}/{total}")
            pb["value"] = i
            prog.update()
            dst = os.path.join(books_dir, fname)
            if os.path.exists(dst):
                if not messagebox.askyesno("确认", f"已存在: {fname}\n覆盖?"):
                    continue
            try:
                shutil.copy2(src, dst)
                imported += 1
            except Exception as e:
                errors.append(f"{fname}: {e}")
            pb["value"] = i + 1
            prog.update()
        prog.destroy()
        self.refresh_books()
        if errors:
            messagebox.showwarning("部分失败", f"成功导入 {imported}/{total} 本\n失败:\n" + "\n".join(errors))
        else:
            messagebox.showinfo("成功", f"成功导入 {imported}/{total} 本书")
        self.status_var.set(f"导入完成: {imported}/{total} 本")

    def delete_books(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        sel = self.book_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择要删除的书籍!")
            return
        files = []
        for s in sel:
            item = self.book_tree.item(s)
            fname = item["values"][0]
            rel = item["values"][3]
            fpath = os.path.join(self.kindle_drive, rel.replace("/", os.sep))
            files.append((fname, fpath))
        names = "\n".join(f[0] for f in files)
        if not messagebox.askyesno("确认", f"确定删除以下 {len(files)} 本书?\n\n{names}\n\n此操作不可撤销!"):
            return
        total = len(files)
        prog = tk.Toplevel(self.root)
        prog.title("删除进度")
        prog.geometry("400x120")
        prog.transient(self.root)
        prog.grab_set()
        ttk.Label(prog, text=f"正在删除 0/{total}...", font=("Segoe UI", 10)).pack(pady=10)
        pb = ttk.Progressbar(prog, maximum=total, value=0, length=360)
        pb.pack(pady=5)
        info_lbl = ttk.Label(prog, text="", font=("Segoe UI", 8))
        info_lbl.pack(pady=2)
        prog.update()
        deleted = 0
        for i, (fname, fpath) in enumerate(files):
            info_lbl.config(text=fname)
            prog.title(f"删除进度 {i+1}/{total}")
            pb["value"] = i
            prog.update()
            try:
                if os.path.exists(fpath):
                    os.remove(fpath)
                    deleted += 1
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {fname}\n{e}")
            pb["value"] = i + 1
            prog.update()
        prog.destroy()
        self.refresh_books()
        self.status_var.set(f"已删除 {deleted}/{total} 本书")

    def on_book_right_click(self, event):
        item = self.book_tree.identify_row(event.y)
        if item:
            self.book_tree.selection_set(item)
            self.book_menu.post(event.x_root, event.y_root)

    def open_book_file(self):
        sel = self.book_tree.selection()
        if not sel:
            return
        item = self.book_tree.item(sel[0])
        rel = item["values"][3]
        fpath = os.path.join(self.kindle_drive, rel.replace("/", os.sep))
        if not os.path.exists(fpath):
            messagebox.showwarning("提示", f"文件不存在: {rel}")
            return
        try:
            os.startfile(fpath)
        except Exception as e:
            messagebox.showerror("错误", f"无法打开: {e}")

    def locate_book(self):
        sel = self.book_tree.selection()
        if not sel:
            return
        item = self.book_tree.item(sel[0])
        rel = item["values"][3]
        fpath = os.path.join(self.kindle_drive, rel.replace("/", os.sep))
        if not os.path.exists(fpath):
            messagebox.showwarning("提示", f"文件不存在: {rel}")
            return
        try:
            subprocess.Popen(['explorer', '/select,', fpath])
        except Exception as e:
            messagebox.showerror("错误", f"无法定位: {e}")

    def show_book_detail(self):
        sel = self.book_tree.selection()
        if not sel:
            return
        item = self.book_tree.item(sel[0])
        messagebox.showinfo("书籍详情",
            f"文件名: {item['values'][0]}\n"
            f"格式: {item['values'][1]}\n"
            f"大小: {item['values'][2]}\n"
            f"路径: {item['values'][3]}")

    def setup_install_tab(self):
        cols = ("name", "category", "description", "repo", "installed")
        self.catalog_tree = ttk.Treeview(self.tab_install, columns=cols, show="headings", height=16)
        self.catalog_tree.heading("name", text="插件名称")
        self.catalog_tree.heading("category", text="分类")
        self.catalog_tree.heading("description", text="描述")
        self.catalog_tree.heading("repo", text="GitHub 仓库")
        self.catalog_tree.heading("installed", text="已装")
        self.catalog_tree.column("name", width=140)
        self.catalog_tree.column("category", width=60)
        self.catalog_tree.column("description", width=340)
        self.catalog_tree.column("repo", width=200)
        self.catalog_tree.column("installed", width=40)
        self.catalog_tree.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.catalog_tree.bind("<Double-1>", lambda e: self.install_catalog_plugin())

        btn_frame = ttk.Frame(self.tab_install)
        btn_frame.pack(fill=tk.X, padx=4, pady=4)
        ttk.Button(btn_frame, text="安装选中插件", command=self.install_catalog_plugin).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="卸载选中插件", command=self.uninstall_catalog_plugin).pack(side=tk.LEFT, padx=3)
        ttk.Separator(btn_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Label(btn_frame, text="自定义仓库:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=3)
        self.repo_var = tk.StringVar()
        ttk.Entry(btn_frame, textvariable=self.repo_var, width=30).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="安装", command=self.install_from_github).pack(side=tk.LEFT, padx=3)
        ttk.Separator(btn_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=8)
        ttk.Label(btn_frame, text="ZIP:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=3)
        self.zip_var = tk.StringVar()
        ttk.Entry(btn_frame, textvariable=self.zip_var, width=20).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="浏览", command=self.browse_zip).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="安装", command=self.install_from_zip).pack(side=tk.LEFT, padx=2)

        self.install_log = tk.Text(self.tab_install, height=5, bg="#1e1e1e", fg="#4ec9b0",
                                   font=("Consolas", 9), insertbackground="#e0e0e0")
        self.install_log.pack(fill=tk.BOTH, expand=False, padx=8, pady=(4, 8))
        self.do_filter_catalog()

    def setup_backup_tab(self):
        frame = ttk.Frame(self.tab_backup, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="备份 koreader 整个目录到本地 ZIP 文件\n（包含插件、设置、字体等）",
                  font=("Segoe UI", 10)).pack(pady=10)
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="备份", command=self.do_backup, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="恢复", command=self.do_restore, width=20).pack(side=tk.LEFT, padx=10)
        info_text = (
            "备份说明:\n"
            "  - 备份将整个 koreader 目录打包为 ZIP\n"
            "  - 恢复时请选择之前备份的 ZIP 文件\n"
            "  - 恢复前建议先退出 KOReader\n"
            "\n"
            "建议在安装新插件前先备份!"
        )
        ttk.Label(frame, text=info_text, font=("Segoe UI", 9), justify=tk.LEFT).pack(pady=20)

    def setup_logs_tab(self):
        self.log_text = tk.Text(self.tab_logs, bg="#1e1e1e", fg="#ce9178",
                                font=("Consolas", 9), wrap=tk.NONE)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        btn_frame = ttk.Frame(self.tab_logs)
        btn_frame.pack(fill=tk.X, padx=4, pady=4)
        ttk.Button(btn_frame, text="刷新日志", command=self.refresh_logs).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="清空显示", command=lambda: self.log_text.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=3)

    def setup_clean_tab(self):
        frame = ttk.Frame(self.tab_clean, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="清理 Kindle 上的临时文件和越狱残留",
                  font=("Segoe UI", 11, "bold")).pack(pady=10)
        items_frame = ttk.Frame(frame)
        items_frame.pack(pady=5)
        ttk.Button(items_frame, text="一键清理", command=self.do_clean, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(items_frame, text="查看空间", command=self.update_space, width=20).pack(side=tk.LEFT, padx=10)
        self.clean_log = tk.Text(frame, height=12, bg="#1e1e1e", fg="#dcdcaa",
                                 font=("Consolas", 9))
        self.clean_log.pack(fill=tk.BOTH, expand=True, padx=4, pady=8)
        info = (
            "清理项目:\n"
            "  - koreader/cache 缓存文件\n"
            "  - koreader/clipboard 剪贴板\n"
            "  - koreader/screenshots 截图\n"
            "  - 根目录 .bin 更新残留文件\n"
            "  - fill_disk 填充文件夹 (越狱后可删)\n"
            "  - Filler.ps1 填充脚本\n"
            "  - spidercat.azw3 越狱文件 (越狱后可删)\n"
        )
        ttk.Label(frame, text=info, font=("Segoe UI", 9), justify=tk.LEFT).pack(pady=5)

    def auto_detect(self):
        drives = KindleManager.detect_all_drives()
        display = []
        best_path = None
        for d in drives:
            label = d["label"]
            tag = ""
            if d["has_koreader"]:
                tag = " [KOReader]"
                if best_path is None:
                    best_path = d["path"]
            if label:
                display.append(f"{d['path']} ({label}){tag}")
            else:
                display.append(f"{d['path']}{tag}")
        self.drive_combo['values'] = display
        if best_path:
            for i, item in enumerate(display):
                if item.startswith(best_path):
                    self.drive_combo.current(i)
                    break
            self.manual_connect()
        elif display:
            self.drive_combo.current(0)
            self.status_var.set(f"检测到 {len(display)} 个盘符，请选择后点「连接」")
        else:
            self.drive_combo.set("")
            self.status_var.set("未检测到任何盘符，请用 USB 连接 Kindle 后点「自动识别」")

    def browse_directory(self):
        path = filedialog.askdirectory(title="选择 Kindle 根目录 (含 koreader 文件夹的目录)")
        if path:
            self.drive_combo.set(path)
            self.manual_connect()

    def manual_connect(self):
        raw = self.drive_combo.get().strip()
        if not raw:
            messagebox.showwarning("提示", "请先选择或输入 Kindle 目录!")
            return
        if " (" in raw:
            path = raw.split(" (")[0]
        else:
            path = raw
        if not os.path.exists(path):
            messagebox.showwarning("提示", f"路径不存在: {path}")
            return
        self.kindle_drive = path
        self.update_space()
        self.refresh_plugins()
        self.do_filter_catalog()
        self.refresh_books()
        has_koreader = os.path.exists(os.path.join(path, "koreader"))
        if has_koreader:
            self.status_var.set(f"已连接: {path}")
        else:
            self.status_var.set(f"已连接: {path} (未找到 koreader 目录)")

    def update_space(self):
        if not self.kindle_drive:
            return
        info = KindleManager.get_free_space(self.kindle_drive)
        self.space_var.set(f"可用: {info['free_mb']} MB | 已用: {info['used_mb']} MB")

    def refresh_plugins(self):
        if not self.kindle_drive:
            return
        for item in self.plugin_tree.get_children():
            self.plugin_tree.delete(item)
        plugins = KindleManager.get_plugins(self.kindle_drive)
        if not plugins:
            self.plugin_tree.insert("", tk.END, values=("未找到插件目录或插件为空", "", "", "", "", ""))
            self.status_var.set("未找到插件")
            return
        for p in plugins:
            status = "已禁用" if p["disabled"] else "已启用"
            desc = p.get("description", "")
            if not desc:
                desc = p.get("fullname", "") or "(无描述)"
            fn = p.get("fullname", "") or "-"
            self.plugin_tree.insert("", tk.END, values=(p["name"], fn, status, desc, p["files"], p["size_kb"]))
        self.status_var.set(f"共 {len(plugins)} 个插件")

    def get_selected_plugin(self):
        sel = self.plugin_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择一个插件")
            return None
        item = self.plugin_tree.item(sel[0])
        name = item["values"][0]
        plugins = KindleManager.get_plugins(self.kindle_drive)
        for p in plugins:
            if p["name"] == name:
                return p
        return None

    def toggle_plugin(self, enable):
        p = self.get_selected_plugin()
        if not p:
            return
        if KindleManager.toggle_plugin(p, enable):
            self.refresh_plugins()
            action = "启用" if enable else "禁用"
            self.status_var.set(f"已{action} {p['name']}")
        else:
            messagebox.showwarning("提示", "操作失败，可能已是该状态")

    def uninstall_plugin(self):
        p = self.get_selected_plugin()
        if not p:
            return
        if not messagebox.askyesno("确认", f"确定要卸载插件 {p['name']} 吗?\n此操作不可撤销!"):
            return
        if KindleManager.delete_plugin(p):
            self.refresh_plugins()
            self.status_var.set(f"已卸载 {p['name']}")
        else:
            messagebox.showerror("错误", "卸载失败")

    def show_plugin_detail(self):
        p = self.get_selected_plugin()
        if not p:
            return
        info = (
            f"插件目录: {p['name']}\n"
            f"全名: {p.get('fullname', '-')}\n"
            f"描述: {p.get('description', '(无描述)')}\n"
            f"状态: {'已禁用' if p['disabled'] else '已启用'}\n"
            f"文件数: {p['files']}\n"
            f"大小: {p['size_kb']} KB\n"
            f"Meta文件: {'有' if p['has_meta'] else '无'}\n"
            f"路径: {p['path']}\n"
        )
        messagebox.showinfo("插件详情", info)

    def on_plugin_selected(self, event=None):
        pass

    def get_installed_plugin_names(self):
        if not self.kindle_drive:
            return set()
        return {p["name"] for p in KindleManager.get_plugins(self.kindle_drive)}

    def do_filter_catalog(self):
        for item in self.catalog_tree.get_children():
            self.catalog_tree.delete(item)
        installed = self.get_installed_plugin_names()
        for p in PLUGIN_CATALOG:
            repo_key = p["repo"].split("/")[-1].replace(".koplugin", "").lower()
            is_installed = any(repo_key in name.lower().replace(".koplugin", "").replace(".disabled", "") for name in installed)
            self.catalog_tree.insert("", tk.END,
                values=(p["name"], p["category"], p["description"], p["repo"],
                        "是" if is_installed else "—"))
        self.status_var.set(f"插件市场: 共 {len(PLUGIN_CATALOG)} 个插件")

    def install_catalog_plugin(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        sel = self.catalog_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择要安装的插件!")
            return
        item = self.catalog_tree.item(sel[0])
        repo = item["values"][3]
        name = item["values"][0]
        self.repo_var.set(repo)
        self.install_log.delete("1.0", tk.END)
        self.log_install(f"开始安装 {name} ({repo})...")

        def worker():
            success = KindleManager.install_from_github(
                repo,
                lambda msg: self.root.after(0, lambda m=msg: self.log_install(m)),
                self.kindle_drive
            )
            self.root.after(0, lambda: self.on_catalog_install_done(success, name))

        threading.Thread(target=worker, daemon=True).start()

    def on_catalog_install_done(self, success, name):
        self.refresh_plugins()
        self.do_filter_catalog()
        if success:
            self.log_install(f"{name} 安装成功!")
        else:
            self.log_install(f"{name} 安装失败!")
        self.status_var.set(f"{'安装成功' if success else '安装失败'}: {name}")

    def uninstall_catalog_plugin(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        sel = self.catalog_tree.selection()
        if not sel:
            messagebox.showwarning("提示", "请先选择要卸载的插件!")
            return
        item = self.catalog_tree.item(sel[0])
        name = item["values"][0]
        installed_status = item["values"][4]
        if installed_status != "是":
            messagebox.showinfo("提示", f"{name} 未安装，无需卸载")
            return
        repo_key = item["values"][3].split("/")[-1].replace(".koplugin", "").lower()
        plugins = KindleManager.get_plugins(self.kindle_drive)
        matched = [p for p in plugins if repo_key in p["name"].lower().replace(".koplugin", "").replace(".disabled", "")]
        if not matched:
            messagebox.showwarning("提示", f"未找到匹配的插件目录")
            return
        if len(matched) > 1:
            names = [p["name"] for p in matched]
            messagebox.showwarning("提示", f"匹配到多个插件: {', '.join(names)}")
            return
        folder_name = matched[0]["name"]
        plugin_path = matched[0]["path"]
        if not os.path.exists(plugin_path):
            messagebox.showwarning("提示", f"插件目录不存在: {folder_name}")
            return
        if not messagebox.askyesno("确认", f"确定卸载 {name} ({folder_name})?\n此操作不可撤销!"):
            return
        try:
            shutil.rmtree(plugin_path, ignore_errors=True)
            self.refresh_plugins()
            self.do_filter_catalog()
            self.log_install(f"{name} 卸载成功!")
            self.status_var.set(f"已卸载: {name}")
        except Exception as e:
            messagebox.showerror("错误", f"卸载失败: {e}")

    def install_from_github(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        repo = self.repo_var.get().strip()
        if not repo:
            messagebox.showwarning("提示", "请选择或输入 GitHub 仓库地址!")
            return
        self.install_log.delete("1.0", tk.END)
        self.log_install("开始安装...")

        def worker():
            success = KindleManager.install_from_github(
                repo,
                lambda msg: self.root.after(0, lambda m=msg: self.log_install(m)),
                self.kindle_drive
            )
            self.root.after(0, lambda: self.on_install_done(success))

        threading.Thread(target=worker, daemon=True).start()

    def install_from_zip(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        zip_path = self.zip_var.get().strip()
        if not zip_path or not os.path.exists(zip_path):
            messagebox.showwarning("提示", "请先选择有效的 ZIP 文件!")
            return
        try:
            installed = KindleManager.install_from_zip(zip_path, self.kindle_drive)
            if installed:
                self.refresh_plugins()
                messagebox.showinfo("成功", f"已安装 {len(installed)} 个插件:\n" + "\n".join(installed))
                self.status_var.set(f"从 ZIP 安装了 {len(installed)} 个插件")
            else:
                messagebox.showwarning("提示", "未在 ZIP 中找到有效的插件文件夹")
        except Exception as e:
            messagebox.showerror("错误", f"安装失败: {e}")

    def browse_zip(self):
        path = filedialog.askopenfilename(
            title="选择插件 ZIP 文件",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")])
        if path:
            self.zip_var.set(path)

    def log_install(self, msg):
        self.install_log.insert(tk.END, msg + "\n")
        self.install_log.see(tk.END)

    def install_btn_state(self, enabled):
        pass

    def on_install_done(self, success):
        self.refresh_plugins()
        self.status_var.set("安装完成" if success else "安装失败")

    def do_backup(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        path = filedialog.asksaveasfilename(
            title="选择备份保存位置",
            defaultextension=".zip",
            initialdir=os.path.expanduser("~"),
            initialfile=f"koreader_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            filetypes=[("ZIP files", "*.zip")])
        if not path:
            return
        self.status_var.set("备份中...")
        self.root.update()
        try:
            if KindleManager.backup(self.kindle_drive, path):
                sz = os.path.getsize(f"{path}.zip") / (1024 * 1024)
                messagebox.showinfo("成功", f"备份完成!\n文件: {path}.zip\n大小: {sz:.1f} MB")
                self.status_var.set(f"备份完成 ({sz:.1f} MB)")
            else:
                messagebox.showerror("错误", "备份失败，koreader 目录不存在")
        except Exception as e:
            messagebox.showerror("错误", f"备份失败: {e}")
            self.status_var.set("备份失败")

    def do_restore(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        path = filedialog.askopenfilename(
            title="选择备份文件",
            filetypes=[("ZIP files", "*.zip")])
        if not path:
            return
        if not messagebox.askyesno("确认", "恢复将覆盖当前 koreader 目录!\n建议先退出 KOReader。\n继续?"):
            return
        self.status_var.set("恢复中...")
        self.root.update()
        try:
            koreader_dir = os.path.join(self.kindle_drive, KOREADER_DIR_REL)
            backup_tmp = os.path.join(self.kindle_drive, "koreader_backup_tmp")
            if os.path.exists(backup_tmp):
                shutil.rmtree(backup_tmp, ignore_errors=True)
            os.makedirs(backup_tmp, exist_ok=True)
            with zipfile.ZipFile(path, "r") as zf:
                zf.extractall(backup_tmp)
            extracted_items = os.listdir(backup_tmp)
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(backup_tmp, extracted_items[0])):
                src = os.path.join(backup_tmp, extracted_items[0])
            else:
                src = backup_tmp
            old_dir = os.path.join(self.kindle_drive, "koreader_old")
            if os.path.exists(old_dir):
                shutil.rmtree(old_dir, ignore_errors=True)
            if os.path.exists(koreader_dir):
                os.rename(koreader_dir, old_dir)
            os.rename(src, koreader_dir)
            if os.path.exists(backup_tmp):
                shutil.rmtree(backup_tmp, ignore_errors=True)
            if os.path.exists(old_dir):
                shutil.rmtree(old_dir, ignore_errors=True)
            self.refresh_plugins()
            messagebox.showinfo("成功", "恢复完成! 请重启 KOReader。")
            self.status_var.set("恢复完成")
        except Exception as e:
            messagebox.showerror("错误", f"恢复失败: {e}")
            self.status_var.set("恢复失败")

    def refresh_logs(self):
        if not self.kindle_drive:
            return
        self.log_text.delete("1.0", tk.END)
        logs = KindleManager.get_logs(self.kindle_drive)
        for name, content in logs.items():
            self.log_text.insert(tk.END, f"{'=' * 50}\n")
            self.log_text.insert(tk.END, f"  {name}\n")
            self.log_text.insert(tk.END, f"{'=' * 50}\n")
            self.log_text.insert(tk.END, content + "\n\n")
        if not logs:
            self.log_text.insert(tk.END, "未找到日志文件")
        self.status_var.set("日志已刷新")

    def do_clean(self):
        if not self.kindle_drive:
            messagebox.showwarning("提示", "请先连接 Kindle!")
            return
        self.clean_log.delete("1.0", tk.END)
        self.clean_log.insert(tk.END, "开始清理...\n")
        self.root.update()
        cleaned = KindleManager.clean_temp(self.kindle_drive)
        if cleaned:
            for item in cleaned:
                self.clean_log.insert(tk.END, f"  [OK] {item}\n")
        else:
            self.clean_log.insert(tk.END, "  没有需要清理的文件\n")
        self.clean_log.insert(tk.END, "\n清理完成!\n")
        self.update_space()
        self.refresh_plugins()
        self.status_var.set("清理完成")


def main():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("TButton", font=("Segoe UI", 9))
    style.configure("TLabel", font=("Segoe UI", 9))
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
