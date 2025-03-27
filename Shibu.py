from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue
import datetime
import asyncio
import os

# Telegram Bot Token
TOKEN = "7873913951:AAFgNSYhylB6bBCgT4ZNCrhbEzeaXZnCc3g"

async def start(update: Update, context: CallbackContext):
    """Start command handler"""
    await update.message.reply_text(
        "🚀 Hey Swayanshu! Ready to grind for Google SWE? Use /remind to get daily reminders."
    )

async def send_reminder(context: CallbackContext):
    """Send daily SWE preparation reminder"""
    job = context.job
    message = (
        "🔥 *Daily SWE Preparation Reminder* 🔥\n\n"
        "📌 *DSA:* Solve 3 problems (Leetcode/Codeforces)\n"
        "📌 *CP:* Participate in a contest or upsolve 2 problems\n"
        "📌 *CS:* Revise OS, DBMS, CN topics\n"
        "📌 *Development:* Work on your Java project\n\n"
        "Keep pushing! 💪🚀"
    )
    await context.bot.send_message(chat_id=job.context, text=message, parse_mode="Markdown")

async def schedule_reminders(update: Update, context: CallbackContext):
    """Schedule daily reminders"""
    chat_id = update.message.chat_id
    remove_job_if_exists(str(chat_id), context)
    
    context.job_queue.run_daily(
        send_reminder, 
        time=datetime.time(hour=7, minute=0, second=0), 
        chat_id=chat_id, 
        name=str(chat_id),
        context=chat_id
    )

    await update.message.reply_text("✅ Daily reminders set for 7:00 AM! Use /stop to disable.")

async def stop_reminders(update: Update, context: CallbackContext):
    """Stop reminders"""
    job_removed = remove_job_if_exists(str(update.message.chat_id), context)
    if job_removed:
        await update.message.reply_text("❌ Daily reminders stopped.")
    else:
        await update.message.reply_text("❌ No active reminders found.")

def remove_job_if_exists(name: str, context: CallbackContext):
    """Remove existing job if it exists"""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def main():
    """Main function to run the bot"""
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", schedule_reminders))
    app.add_handler(CommandHandler("stop", stop_reminders))

    print("🚀 Bot is running...")
    try:
        asyncio.get_running_loop()
        app.run_polling()
    except RuntimeError:
        asyncio.run(app.run_polling())

# === Flask Server (If Hosting Requires It) ===
import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# Run the bot
main()
