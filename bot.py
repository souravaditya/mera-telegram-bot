import os
import logging
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
OWNER_CHAT_ID  = os.environ.get("OWNER_CHAT_ID", "")

# Premlata ke naam/hints
PREMLATA_HINTS = ["premlata", "premu", "prem", "baby", "jaan", "sweetheart", "love you", "i love", "miss you"]

# Sourav ko bulane wale keywords
CALL_OWNER_KEYWORDS = [
    "sourav ko bulao", "sourav ko online", "sourav online aaye",
    "sourav se baat", "owner ko bulao", "aapko bulao",
    "sourav ko bolo", "sourav ko message", "call sourav",
    "sourav kahan", "sourav nahi hai", "sourav available",
    "real person", "insaan se baat", "human se baat",
    "online aao", "online aa jao", "online aajao"
]

AI_SYSTEM_PROMPT = """Tum Sourav Aditya ke personal Telegram bot ho. Tumhara naam "Aditya Bot" hai.

Sourav Aditya ke baare mein:
- Profession: Freelance Developer, Accountant, Data Analyst, Finance Advisor, Life Coach and all other online services.
- Speciality: AI Prompt Engineering, Data Analyst, Computer Operator.
- Telegram: @aditya_sourav
- Email: souravaditya143@email.com
- Working hours: Subah 10 baje se Shaam 7 baje tak.
- Location: Village - BINJHA, District - Deoghar, Jharkhand

Tumhara behavior:
- Dost jaisa baat karo — casual, warm aur friendly
- Funny sawal pe funny jawab do, masti karo!
- Serious sawal pe helpful aur clear jawab do
- Hindi aur English dono mein baat kar sakte ho
- Short replies do — zyada lamba mat likho
- Agar kuch nahi pata to kaho "Yeh toh Sourav hi bata payenge: @aditya_sourav"

Important: Tum sirf ek auto-reply bot ho. Fees ya deadlines ke baare mein koi commitment mat karo."""

ROMANTIC_PROMPT = """Tum Sourav Aditya ke personal Telegram bot ho.

Yeh message Sourav ki girlfriend Premlata Kumari ka hai.
Unse pyaar se, romantically aur warmly baat karo.
Thoda flirty bhi ho sakte ho — jaise ek caring boyfriend ka bot ho.
Hindi mein baat karo. Short aur sweet replies do.
Unhe feel karao ki Sourav unhe bahut miss kar raha hai! 💕"""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
client = Groq(api_key=GROQ_API_KEY)


def is_premlata(user_name: str, text: str) -> bool:
    text_lower = text.lower()
    name_lower = user_name.lower()
    if "premlata" in name_lower or "premu" in name_lower:
        return True
    for hint in PREMLATA_HINTS:
        if hint in text_lower:
            return True
    return False


def should_notify_owner(text: str) -> bool:
    text_lower = text.lower()
    for keyword in CALL_OWNER_KEYWORDS:
        if keyword in text_lower:
            return True
    return False


def get_ai_reply(user_message: str, user_name: str, romantic: bool = False) -> str:
    try:
        prompt = ROMANTIC_PROMPT if romantic else AI_SYSTEM_PROMPT
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{user_name} ka message: {user_message}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return "Abhi thodi takleef ho rahi hai. Seedha message karein: @aditya_sourav 🙏"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""
    user_name = user.first_name or "Dost"
    logger.info(f"Message from {user_name}: {text}")

    # Owner ko bulane ka check — seedha code mein
    notify_now = should_notify_owner(text)

    if notify_now:
        reply = "Theek hai! Main Sourav ko abhi notify kar deta hoon! 📲\nVo jald hi aapko reply karenge 😊"
    elif is_premlata(user_name, text):
        reply = get_ai_reply(text, user_name, romantic=True)
    else:
        reply = get_ai_reply(text, user_name, romantic=False)

    await update.message.reply_text(reply)

    # Owner ko Telegram notification
    if OWNER_CHAT_ID:
        try:
            if notify_now:
                notif = (
                    f"🚨 *URGENT — {user_name} aapko online aane ko bol raha hai!*\n"
                    f"👤 {user_name} (@{user.username or 'N/A'})\n"
                    f"💬 Message: {text[:200]}\n\n"
                    f"➡️ Unhe reply karein: @{user.username or 'N/A'}"
                )
            else:
                notif = (
                    f"📩 *Naya Message*\n"
                    f"👤 {user_name} (@{user.username or 'N/A'})\n"
                    f"💬 {text[:100]}\n"
                    f"🤖 Bot reply: {reply[:100]}"
                )
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=notif,
                parse_mode="Markdown"
            )
            logger.info("Owner ko notification bhej diya ✅")
        except Exception as e:
            logger.error(f"Notification error: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! 🙏\n\nMain Sourav ka personal assistant bot hoon!\n"
        "Sourav abhi online nahi hain, lekin main hoon na 😊\n"
        "Kuch bhi puchho — serious, funny, ya kuch bhi!"
    )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot chal raha hai... ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
