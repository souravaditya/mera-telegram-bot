import os
import logging
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY", "")

FIXED_REPLIES = {
    "rate":        "Meri rate list ke liye please WhatsApp karein: +91-8521460129",
    "price":       "Meri rate list ke liye please WhatsApp karein: +91-8521460129",
    "fee":         "Meri rate list ke liye please WhatsApp karein: +91-8521460129",
    "available":   "Main abhi busy hoon, jaldi wapis aaunga. Urgent ho toh call karein.",
    "free":        "Main abhi busy hoon, jaldi wapis aaunga. Urgent ho toh call karein: +91-8521460129",
    "when":        "Main jaldi hi wapis aaunga, tab baat karenge!",
    "kab":         "Main 1-2 ghante mein wapis aaunga, tab baat karenge!",
    "hello":       "Hi, Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "hi":          "Hello, Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "hii":         "Hello, Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "hey":         "Hello, Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "sona":        "Boliye sona....",
    "kya kr rhe":  "Me abhi kuchh kam me busy hu, lekin koi baat nahi aap message kr dijiye, me online aaunga tb jwab de dunga 😊",
    "contact":     "Aap mujhe in tareekon se contact kar sakte hain:\n📞 Call: +91-8521460129\n📧 Email: souravaditya143@email.com",
    "location":    "Hamara address: Village - BINJHA, District - Deoghar, Jharkhand",
    "address":     "Hamara address: Village - BINJHA, DEOGHAR, JHARKHAND",
    "help":        "Main abhi online nahi hoon. Aap apna sawaal bta dijiye, main wapis aate hi reply karunga! 😊",
}

AI_SYSTEM_PROMPT = """Tum Sourav Aditya ke personal Telegram bot ho.

Sourav Aditya ke baare mein:
- Profession: Freelance Developer, Accountant, Data Analyst, Finance Advisor, Life Coach and all other online services.
- Speciality: AI Prompt Engineering, Data Analyst, Computer Operator.
- Contact: Phone no. +91-8521460129, Email ID - souravaditya143@email.com
- Working hours: Subah 10 baje se Shaam 7 baje tak.

Tumhara kaam:
- Log jo bhi poochhen, unhe helpful jawab dena
- Polite aur friendly rehna
- Agar kuch nahi pata, toh kehna ki "Sourav jaldi wapis aayenge aur jawab denge"
- Hindi aur English dono mein jawab de sako toh behtar hai
- Short aur clear replies do — zyada lamba mat karo

Important: Tum sirf ek auto-reply bot ho. Koi commitment mat karo fees ya deadlines ke baare mein."""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)


def check_fixed_reply(text: str):
    text_lower = text.lower()
    for keyword, reply in FIXED_REPLIES.items():
        if keyword in text_lower:
            return reply
    return None


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
        return "Abhi thodi takleef ho rahi hai. Kripya seedha message karein. 🙏"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""
    user_name = user.first_name or "Dost"
    logger.info(f"Message from {user_name}: {text}")
    reply = check_fixed_reply(text) or get_ai_reply(text, user_name)
    await update.message.reply_text(reply)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! 🙏\n\nMain abhi online nahi hoon, lekin aap apna sawaal yahan chhod sakte hain.\nMain jald se jald reply karunga! 😊"
    )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot chal raha hai... ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
    
