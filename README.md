# 🔍 Google Search Update Monitor (Google 搜索算法更新监控机器人)

> 一个全自动的 Python 脚本，用于监控 Google 搜索的**核心算法更新 (Core Updates)** 和 **官方博客 (Search Central Blog)**。一旦发现风吹草动，第一时间推送到你的 Telegram。

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Python](https://img.shields.io/badge/Python-3.9-yellow)

## ✨ 核心功能
* **双核监控**：同时监控 [Google 搜索状态仪表盘](https://status.search.google.com/) (突发故障/核心更新) 和 [官方博客](https://developers.google.com/search/blog) (SEO 技术文章)。
* **永不掉线**：利用 Google News 官方接口作为“中转站”，完美绕过 Google 博客的 404/反爬虫拦截。
* **自动翻译**：内置 `deep-translator`，自动将英文公告标题和摘要**翻译成中文**，无障碍阅读。
* **智能建议**：识别 Core Update、Spam Update 等关键词，自动在消息附带 SEO 应对建议。
* **0 成本部署**：完全基于 GitHub Actions 运行，无需购买服务器，永久免费。

---

## 🚀 3 分钟快速部署指南

### 第一步：Fork 本仓库
点击页面右上角的 **Fork** 按钮，将本项目完整复制到你自己的 GitHub 账号下。

### 第二步：获取 Telegram 配置 (保姆级教程)
你需要获取两个参数：`机器人 Token` (相当于账号密码) 和 `你的 Chat ID` (相当于收信地址)。

#### 1. 获取机器人 Token
1. 在 Telegram 中搜索 **[@BotFather](https://t.me/BotFather)** (这是官方的机器人之父)。
2. 点击 **Start**，发送指令 `/newbot`。
3. 按照提示，先给机器人起个显示名称（例如：`谷歌更新监控`）。
4. 再给机器人起个唯一的用户名（**必须以 `_bot` 结尾**，例如：`my_google_seo_bot`）。
5. 成功后，BotFather 会发给你一串长字符（如 `123456:ABC-DEF...`），这就是 **Token**，请复制备用。

#### 2. 获取你的 Chat ID
1. 在 Telegram 中搜索 **[@userinfobot](https://t.me/userinfobot)** (这是一个查 ID 的工具)。
2. 点击 **Start**。
3. 它会回复你的信息，其中 `Id` 后面的那串数字（例如 `12345678`）就是你的 **Chat ID**，请复制备用。

#### ⚠️ 关键一步 (不要漏掉！)
回到你刚才创建的那个新机器人（在第1步创建的那个），点击 **Start** 随便发句 "Hello"。
*(如果这一步不做，机器人没有权限主动给你发消息)*

### 第三步：配置 GitHub Secrets
为了安全，不要把密码直接写在代码里。我们需要把它存到仓库的保险箱里。

1. 进入你 Fork 后的仓库页面。
2. 点击顶部菜单的 **Settings** (设置)。
3. 在左侧边栏找到 **Secrets and variables** -> 点击 **Actions**。
4. 点击绿色的 **New repository secret** 按钮，依次添加以下两个变量：

| Secret Name (变量名) | Secret Value (填入内容) | 说明 |
| :--- | :--- | :--- |
| `TG_BOT_TOKEN` | `123456:ABC-DEF...` | 刚才找 BotFather 要的 Token |
| `TG_CHAT_ID` | `12345678` | 刚才找 userinfobot 要的数字 ID |

### 第四步：启动机器人
配置完成后，我们需要手动激活一次脚本。

1. 点击仓库顶部的 **Actions** 标签。
2. 在左侧点击 **Google Update Monitor**。
3. 在右侧点击 **Run workflow** 按钮 -> 绿色的 **Run workflow**。
4. 等待约 30 秒，如果显示绿色对勾 ✅，并且你的手机收到了测试消息，说明部署成功！

---

## 🛠️ 高级说明

### 运行频率
脚本默认 **每 4 小时** (Cron: `0 */4 * * *`) 运行一次。
如果你想修改频率，可以编辑 `.github/workflows/schedule.yml` 文件中的 `cron` 表达式。

### 技术栈
* **Requests & BeautifulSoup4**: 网页抓取与清洗。
* **Feedparser**: 处理 Atom/RSS 订阅源。
* **Deep Translator**: 调用 Google Translate API 进行免费翻译。
* **GitHub Actions**: 自动化定时任务托管。

## 🤝 贡献与支持
如果你发现 Google 更改了 RSS 地址，或者有新的功能建议（比如增加飞书/钉钉推送），欢迎提交 **Issue** 或 **Pull Request**！

## 📄 开源协议
本项目采用 [MIT License](LICENSE) 协议，你可以自由修改、分发或用于商业用途。
