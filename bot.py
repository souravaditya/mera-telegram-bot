import os
import json
import logging
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# ─────────────────────────────────────────
#  CONFIGURATION  ←  Sirf yahan badlein
# ─────────────────────────────────────────
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OWNER_CHAT_ID    = os.environ.get("OWNER_CHAT_ID", "")   # optional: owner ko notify kare

# ─────────────────────────────────────────
#  FIXED JAWAB  ←  Apne hisaab se badlein
# ─────────────────────────────────────────
FIXED_REPLIES = {
    # Keywords (lowercase) : Jawab
    "rate":         "Meri rate list ke liye please WhatsApp karein: +91-8521460129",
    "price":        "Meri rate list ke liye please WhatsApp karein: +91-8521460129",
    "fee":          "Meri rate list ke liye please WhatsApp karein: +91-8521460129",
    "available":    "Main abhi busy hoon, jaldi wapis aaunga. Urgent ho toh call karein.",
    "free":         "Main abhi busy hoon, jaldi wapis aaunga. Urgent ho toh call karein: +91-8521460129",
    "when":         "Main jaldi hi wapis aaunga, tab baat karenge!",
    "kab":          "Main 1-2 ghante mein wapis aaunga, tab baat karenge!",
    "hello":        "Hi,  Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "hi":           "Hello, Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "hii":          "Hello, Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "hey":          "Hello, Main abhi online nahi hoon. Agar kuchh puchhna he to puchiye mere assistant jwab de denge. Ya fir jb me online aaunga tb jwab de dunga.",
    "sona":       "Boliye sona...."
    "kya kr rhe hen":      me abhi kuchh kam me busy hu, lekin koi baat nahi aap message kr dijiye, me online aaunga tb jwab de dunga 😊",
    "contact":      "Aap mujhe in tareekon se contact kar sakte hain:\n📞 Call: +91-8521460129\n📧 Email: souravaditya143@email.com",
    "location":     "Hamara address: Village - BINJHA, Dirstict - Deoghar, Jharkhand",
    "address":      "Hamara address: Village - BINJHA, DEOGHAR, JHARKHAND",
    "help":         "Main abhi online nahi hoon. Aap apna sawaal bta dijiye, main wapis aate hi reply karunga! 😊",
}

# ─────────────────────────────────────────
#  AI SYSTEM PROMPT  ←  Apna parichay likhein
# ─────────────────────────────────────────
AI_SYSTEM_PROMPT = """
Tum Sourav Aditya ke personal Telegram bot ho.

Sourav Aditya ke baare mein:
- Profession: Freelance Developer, Accountant, data analyst, finance advisor, life coach and all other online services.
- Speciality:  AI Prompt engineering, data analyst, Computer operator.
- Contact: Phone no. +91-8521460129, Email ID - souravaditya143@email.com
- Working hours: Subah 10 baje se Shaam 7 baje tak.

Tumhara kaam:
- Log jo bhi poochhen, unhe helpful jawab dena
- Polite aur friendly rehna
- Agar kuch nahi pata, toh kehna ki "Sourav jaldi wapis aayenge aur jawab denge"
- Hindi aur English dono mein jawab de sako toh behtar hai
- Short aur clear replies do — zyada lamba mat karo

Important: Tum sirf ek auto-reply bot ho. Koi commitment mat karo fees ya deadlines ke baare mein.
"""

# ─────────────────────────────────────────
#  CODE  ←  Isse mat badlein
# ─────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def check_fixed_reply(text: str) -> str | None:
    """Check karo ki koi fixed keyword match karta hai ya nahi."""
    text_lower = text.lower()
    for keyword, reply in FIXED_REPLIES.items():
        if keyword in text_lower:
            return reply
    return None


def get_ai_reply(user_message: str, user_name: str) -> str:
    """Claude se smart reply lo."""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            system=AI_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"{user_name} ka message: {user_message}"
                }
            ]
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return "Abhi mujhe jawab dene mein thodi takleef ho rahi hai. Kripya seedha message karein ya thodi der baad try karein. 🙏"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Har incoming message ko handle karo."""
    user = update.effective_user
    text = update.message.text or ""
    user_name = user.first_name or "Dost"

    logger.info(f"Message from {user_name} ({user.id}): {text}")

    # Pehle fixed reply check karo
    fixed = check_fixed_reply(text)
    if fixed:
        reply = fixed
        logger.info(f"Fixed reply diya: {reply[:50]}...")
    else:
        # AI se reply lo
        reply = get_ai_reply(text, user_name)
        logger.info(f"AI reply diya: {reply[:50]}...")

    await update.message.reply_text(reply)

    # Optional: Owner ko notify karo
    if OWNER_CHAT_ID:
        try:
            notification = (
                f"📩 *Naya Message*\n"
                f"👤 {user_name} (@{user.username or 'N/A'})\n"
                f"💬 {text[:100]}\n"
                f"🤖 Bot reply: {reply[:100]}"
            )
            await context.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text=notification,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Owner notification error: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """'/start' command ka jawab."""
    await update.message.reply_text(
        "Namaste! 🙏\n\n"
        "Main abhi online nahi hoon, lekin aap apna sawaal yahan chhod sakte hain.\n"
        "Main jald se jald reply karunga! 😊"
    )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot chal raha hai... ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
