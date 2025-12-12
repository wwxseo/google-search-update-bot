import feedparser
import requests
import os
import sys
import json
from bs4 import BeautifulSoup
import re
from deep_translator import GoogleTranslator # 引入翻译神器

# --- 配置区域 ---
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")
STATE_FILE = "last_updates.json" 

FEEDS = [
    {
        "name": "🚨 状态仪表盘 (Status)",
        "url": "https://status.search.google.com/en/feed.atom",
        "type": "status"
    },
    {
        "name": "📰 官方博客 (Blog)",
        "url": "https://news.google.com/rss/search?q=site:developers.google.com/search/blog&hl=en-US&gl=US&ceid=US:en",
        "type": "blog"
    }
]

ADVICE_DICT = {
    "core update": "💡 **核心更新建议:**\n1. 关注整体内容质量而非单一页面。\n2. 排名波动正常，观察 2 周再调整。\n3. 对照 Google 质量指南自查。",
    "spam update": "💡 **垃圾内容更新建议:**\n1. 检查是否有采集/AI生成低质内容。\n2. 检查外链质量。\n3. 避免滥用过期域名。",
    "helpful content": "💡 **有用内容更新建议:**\n1. 确保内容是为“人”写的，而不是为“搜索引擎”写的。\n2. 展示真实的专业知识和体验。"
}

def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"发送失败: {e}")

def translate_text(text):
    """自动将英文翻译成中文"""
    if not text: return ""
    try:
        # 使用 Google 翻译引擎，源语言自动识别，目标语言中文
        translated = GoogleTranslator(source='auto', target='zh-CN').translate(text)
        return translated
    except Exception as e:
        print(f"翻译失败: {e}")
        return text # 如果翻译挂了，就返回原文，别报错

def get_smart_advice(title):
    title_lower = title.lower()
    for key, advice in ADVICE_DICT.items():
        if key in title_lower:
            return "\n\n" + advice
    return ""

def clean_html(html_content):
    if not html_content: return "暂无详情"
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator="\n").strip()
    text = re.sub(r'\n+', '\n', text)
    if len(text) > 500: # 翻译前稍微放宽一点长度
        return text[:500] + "..."
    return text

def check_updates():
    print("🔍 开始监控 (自动翻译模式)...")
    
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try: history = json.load(f)
            except: history = {}
    else:
        history = {}

    save_needed = False
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

    for feed_config in FEEDS:
        print(f"正在检查: {feed_config['name']}...")
        try:
            response = requests.get(feed_config['url'], headers=headers, timeout=20)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if not feed.entries: continue

                latest = feed.entries[0]
                entry_id = latest.id if 'id' in latest else latest.link
                link = latest.link
                updated = latest.published if 'published' in latest else "近期"
                
                # 1. 获取原文
                raw_title = latest.title
                raw_content = ""
                if 'summary' in latest: raw_content = latest.summary
                elif 'content' in latest: raw_content = latest.content[0].value
                clean_summary = clean_html(raw_content)

                last_id = history.get(feed_config['url'])

                if entry_id != last_id:
                    print(f"🚨 发现新内容: {raw_title}")
                    
                    # 2. 执行翻译 (关键步骤)
                    print("   正在翻译内容...")
                    cn_title = translate_text(raw_title)
                    cn_summary = translate_text(clean_summary)
                    
                    advice = get_smart_advice(raw_title) # 建议本来就是中文，不用翻
                    
                    # 3. 发送中文消息
                    msg = (
                        f"{feed_config['name']} 更新通知\n\n"
                        f"📌 *{cn_title}*\n"
                        f"⏰ {updated}\n\n"
                        f"📝 *内容摘要:*\n"
                        f"`{cn_summary}`"
                        f"{advice}\n\n"
                        f"🔗 [阅读原文]({link})"
                    )
                    send_telegram_message(msg)
                    
                    history[feed_config['url']] = entry_id
                    save_needed = True
                else:
                    print("   无新更新")
            else:
                print(f"   请求失败: {response.status_code}")
        except Exception as e:
            print(f"   出错: {e}")

    if save_needed:
        with open(STATE_FILE, "w") as f:
            json.dump(history, f)

if __name__ == "__main__":
    check_updates()
