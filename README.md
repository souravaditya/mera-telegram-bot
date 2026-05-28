# 🤖 Mera Telegram Auto-Reply Bot

Yeh bot aapke offline rehne par logon ke messages ka automatically jawab deta hai.
Simple questions ke liye fixed reply, baaki ke liye Claude AI smart reply deta hai.

---

## 📋 Zaruri Cheezein

1. **Telegram Bot Token** — BotFather se milega
2. **Anthropic API Key** — console.anthropic.com se milega (free trial available)
3. **Railway ya Render account** — free hosting ke liye

---

## 🚀 Deploy Karne ke Steps

### Step 1: Bot Token Banayein
1. Telegram open karein
2. `@BotFather` search karein
3. `/newbot` bhejein
4. Naam dein (jaise: "Mera Assistant Bot")
5. Username dein (jaise: `mera_assistant_bot`)
6. Token copy karein — kuch aisa dikhega:
   `7123456789:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Anthropic API Key Lein
1. https://console.anthropic.com par jayen
2. Sign up karein (free)
3. API Keys section mein jayen
4. "Create Key" karein
5. Copy karein — kuch aisa: `sk-ant-api03-xxxxx`

### Step 3: bot.py Customize Karein
`bot.py` file mein yeh jagahein badlein:
- `[APNA NAAM]` → Apna naam
- `[APNA KAAM]` → Apna profession
- `+91-XXXXXXXXXX` → Apna phone number
- Fixed replies mein apne hisaab se jawab likhein

### Step 4: Railway pe Deploy Karein (FREE)

1. https://railway.app par jayen
2. GitHub se login karein
3. "New Project" → "Deploy from GitHub repo" → Yeh folder upload karein
4. Environment Variables add karein:
   ```
   TELEGRAM_TOKEN = aapka_token_yahan
   ANTHROPIC_API_KEY = aapki_api_key_yahan
   OWNER_CHAT_ID = aapka_chat_id (optional)
   ```
5. Deploy ho jayega! ✅

### OWNER_CHAT_ID Kaise Milega? (Optional)
- Telegram mein `@userinfobot` ko `/start` bhejein
- Woh aapka Chat ID bata dega

---

## ⚙️ Bot Customize Karna

### Fixed Keywords Badlein
`bot.py` mein `FIXED_REPLIES` dictionary mein:
```python
"keyword": "Aapka jawab yahan",
```

### AI Personality Badlein
`AI_SYSTEM_PROMPT` mein apne baare mein jankari update karein.

---

## 📁 Files

| File | Kaam |
|------|------|
| `bot.py` | Main bot code |
| `requirements.txt` | Python libraries |
| `Procfile` | Railway/Render ke liye |

---

## ❓ Problem Aaye Toh

- Token galat hai → BotFather se dobara check karein
- Bot reply nahi kar raha → Railway logs check karein
- AI reply nahi aa raha → Anthropic API key check karein
