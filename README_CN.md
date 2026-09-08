# KOReader 管理工具

一个 Windows 桌面 GUI 工具，用于管理已越狱 Kindle 设备上的 KOReader 插件和电子书。

## 功能概览

### 插件管理
- 列出所有已安装的 KOReader 插件，显示全名、描述、文件数和大小
- 启用 / 禁用 / 卸载插件
- 查看插件详情（从 `_meta.lua` 解析）

### 插件市场
- 浏览 34+ 个社区热门插件目录
- 从 GitHub 仓库一键安装
- 支持自定义仓库地址安装
- 支持从本地 ZIP 文件安装
- 直接在市场列表中卸载已安装的插件
- 每个插件显示已安装状态标记

### 图书管理
- 扫描并列出 Kindle 上所有电子书（EPUB、PDF、MOBI、AZW3、CBZ、TXT、FB2、DJVU、DOCX）
- 自定义书籍目录路径（默认 `documents`）
- 从电脑导入书籍到 Kindle，带进度条
- 批量删除书籍，带确认弹窗和进度条
- 双击用电脑默认程序打开书籍
- 右键菜单：打开、定位到目录、查看详情、删除

### 备份恢复
- 将整个 `koreader` 目录打包备份为 ZIP 文件
- 从备份 ZIP 恢复

### 日志查看
- 查看 `crash.log` 崩溃日志，排查问题
- 查看 `version.log` 版本信息

### 清理维护
- 一键清理缓存文件、截图、残留 `.bin` 更新文件
- 删除 `fill_disk` 填充文件夹（越狱后不再需要）
- 删除 SpiderCat 越狱文件
- 清理前后显示磁盘空间变化

### 设备连接
- 自动检测 Kindle 盘符和卷标
- 下拉手动选择盘符
- 浏览选择自定义目录路径
- 实时显示可用磁盘空间

## 截图说明

| 标签页 | 功能说明 |
|--------|---------|
| 插件管理 | 列出、启用/禁用/卸载插件 |
| 图书管理 | 扫描、导入、删除、打开电子书 |
| 插件市场 | 浏览和安装 34+ 社区插件 |
| 备份恢复 | 备份/恢复 koreader 目录 |
| 日志查看 | 查看 crash.log 和 version.log |
| 清理维护 | 清理缓存、填充文件、越狱残留 |

## 系统要求

- Windows 10/11（64 位）
- 通过 USB 连接的 Kindle（大容量存储模式）
- Kindle 上已安装 KOReader（根目录有 `koreader/` 目录）

## 下载

从 [Releases](../../releases) 页面下载最新版本：

- `KOReaderManager.exe` — 独立可执行文件，无需安装，双击即可运行

## 使用方法

1. 用 USB 线将 Kindle 连接到电脑
2. 运行 `KOReaderManager.exe`
3. 点击「自动识别」或从下拉框选择 Kindle 盘符
4. 点击「连接」
5. 使用顶部各标签页管理插件、图书等

## 从源码构建

```bash
git clone https://github.com/jayxtt999/KOReaderManager.git
cd KOReaderManager
pip install pyinstaller
pyinstaller KOReaderManager.py --onefile --windowed --name KOReaderManager
```

## 插件目录

内置插件市场包含以下分类的插件：

| 分类 | 示例插件 |
|------|---------|
| 商店 | AppStore（插件商店）、Storefront |
| 美化 | SimpleUI、ZenUI、ProjectTitle（封面墙） |
| 阅读 | CoverBrowser、CoverImage |
| 工具 | KOAssistant、UpdatesManager、SSH |
| 音频 | KinAMP（蓝牙音乐）、LARK（有声书） |
| 学习 | KAnki（记忆卡片）、AskAI（AI 阅读伴侣） |
| 游戏 | Gambatte-K2（GB模拟器）、KWordle、俄罗斯方块、国际象棋 |
| 系统 | AutoSuspend、AutoStandby、BatteryStat（电池统计） |
| 开发 | kTerm（终端）、UsbNetLite（SSH远程）、ScreenControl（投屏） |

## 越狱相关

本工具假设你的 Kindle 已越狱并安装了 KOReader。如果你的 Kindle 还没越狱：

1. 访问 [KindleModding 官网](https://kindlemodding.org/) 了解越狱方法
2. 推荐使用 [SpiderCat](https://kindlemodding.org/jailbreaking/SpiderCat/) — 目前最简单的越狱方法
3. 越狱后在 Kindle 搜索栏输入 `;kpm install koreader` 安装 KOReader

## 许可证

MIT License - 可自由修改和分发。

## 致谢

- [KOReader](https://github.com/koreader/koreader) — 最佳的电子墨水屏阅读器
- [KindleModding](https://kindlemodding.org/) — Kindle 越狱社区
- [SpiderCat](https://kindlemodding.org/jailbreaking/SpiderCat/) — 最简单的 Kindle 越狱工具
- 所有插件目录中收录的插件作者
