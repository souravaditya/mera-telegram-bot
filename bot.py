import os
import logging
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")
OWNER_CHAT_ID  = os.environ.get("OWNER_CHAT_ID", "")

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
- Agar kuch nahi pata to kaho "Yeh toh Sourav hi bata payenge, unse puchho: @aditya_sourav"

IMPORTANT — Agar koi yeh kaho:
- "Sourav ko online aao bolo"
- "Sourav ko message karo"  
- "Bolo Sourav online aaye"
- "Sourav se baat karni hai"
- "Owner ko bulao"
- Ya koi bhi aisa message jisme lagta ho ki user Sourav se directly baat karna chahta hai

Toh reply mein likho: "Theek hai, main Sourav ko abhi notify kar deta hoon! 📲"
Aur saath mein [NOTIFY_OWNER] tag zaroor likho — yeh bahut zaroori hai.

Important: Tum sirf ek auto-reply bot ho. Fees ya deadlines ke baare mein koi commitment mat karo."""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)


def get_ai_reply(user_message: str, user_name: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=300,
            messages=[
                {"role": "system", "content": AI_SYSTEM_PROMPT},
                {"role": "user", "content": f"{user_name} ka message: {user_message}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return "Abhi thodi takleef ho rahi hai. Kripya seedha message karein: @aditya_sourav 🙏"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""
    user_name = user.first_name or "Dost"
    logger.info(f"Message from {user_name}: {text}")

    reply = get_ai_reply(text, user_name)

    # [NOTIFY_OWNER] tag check karo
    notify_owner = "[NOTIFY_OWNER]" in reply
    clean_reply = reply.replace("[NOTIFY_OWNER]", "").strip()

    await update.message.reply_text(clean_reply)

    # Owner ko notification bhejo
    if OWNER_CHAT_ID:
        try:
            if notify_owner:
                # Special urgent notification
                notif = (
                    f"🚨 *{user_name} aapko online aane ko bol raha hai!*\n"
                    f"👤 {user_name} (@{user.username or 'N/A'})\n"
                    f"💬 Message: {text[:200]}"
                )
            else:
                # Normal notification
                notif = (
                    f"📩 *Naya Message*\n"
                    f"👤 {user_name} (@{user.username or 'N/A'})\n"
                    f"💬 {text[:100]}\n"
                    f"🤖 Bot reply: {clean_reply[:100]}"
                )
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=notif,
                parse_mode="Markdown"
            )
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
    
