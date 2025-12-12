# Google Search Update Monitor (Google 搜索算法更新监控机器人)

这是一个全自动的 Python 脚本，用于监控 Google 搜索的**核心算法更新 (Core Updates)** 和 **官方博客 (Search Central Blog)**。

一旦发现新动态，它会自动通过 Google 翻译将内容**翻译成中文**，并第一时间推送到你的 **Telegram**。

## ✨ 功能特点
* **双核监控**：同时监控 [Google 搜索状态仪表盘](https://status.search.google.com/) 和 [官方博客](https://developers.google.com/search/blog)。
* **永不掉线**：利用 Google News 接口绕过官方博客的 404/反爬拦截。
* **自动翻译**：引入 `deep-translator`，自动将英文公告翻译为中文摘要。
* **智能建议**：针对 Core Update、Spam Update 等不同更新，自动附带 SEO 应对建议。
* **0 成本部署**：完全基于 GitHub Actions 运行，无需服务器。

## 🚀 如何使用 (3 分钟部署)

### 1. Fork 本仓库
点击右上角的 **Fork** 按钮，将本项目复制到你的 GitHub 账号下。

### 2. 获取 Telegram 配置
1.  找 [@BotFather](https://t.me/BotFather) 创建机器人，获取 **Token**。
2.  获取你自己的 **Chat ID** (user ID)。

### 3. 配置 GitHub Secrets
进入你 Fork 后的仓库，点击 `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`，添加以下两个变量：

| Name | Value | 说明 |
| :--- | :--- | :--- |
| `TG_BOT_TOKEN` | `123456:ABC-DEF...` | 你的机器人 Token |
| `TG_CHAT_ID` | `12345678` | 你的 Chat ID |

### 4. 启动
1.  点击仓库顶部的 `Actions` 标签。
2.  点击左侧的 `Google Update Monitor`。
3.  点击 `Run workflow` 手动触发一次初始化。
4.  **完成！** 以后每 4 小时脚本会自动运行一次。

## 🛠️ 技术栈
* Python 3.9
* GitHub Actions (Cron Job)
* Feedparser (RSS 解析)
* Deep Translator (翻译)

## 📄 License
MIT License
