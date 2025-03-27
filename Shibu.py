from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue
import datetime
import asyncio
import os


TOKEN = os.getenv("7873913951:AAFgNSYhylB6bBCgT4ZNCrhbEzeaXZnCc3g")  # Replace with your bot's token

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🚀 Hey Swayanshu! Ready to grind for Google SWE? Use /remind to get daily reminders."
    )

async def send_reminder(context: CallbackContext):
    message = (
        "🔥 *Daily SWE Preparation Reminder* 🔥\n\n"
        "📌 *DSA:* Solve 3 problems (Leetcode/Codeforces)\n"
        "📌 *CP:* Participate in a contest or upsolve 2 problems\n"
        "📌 *CS:* Revise OS, DBMS, CN topics\n"
        "📌 *Development:* Work on your Java project\n\n"
        "Keep pushing! 💪🚀"
    )
    await context.bot.send_message(chat_id=context.job.chat_id, text=message, parse_mode="Markdown")

async def schedule_reminders(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_daily(send_reminder, time=datetime.time(hour=7, minute=00, second=0), chat_id=chat_id, name=str(chat_id))
    await update.message.reply_text("✅ Daily reminders set for 7:00 AM! Use /stop to disable.")

async def stop_reminders(update: Update, context: CallbackContext):
    job_removed = remove_job_if_exists(str(update.message.chat_id), context)
    if job_removed:
        await update.message.reply_text("❌ Daily reminders stopped.")
    else:
        await update.message.reply_text("❌ No active reminders found.")

def remove_job_if_exists(name: str, context: CallbackContext):
    """Remove existing job with the same name."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remind", schedule_reminders))
    app.add_handler(CommandHandler("stop", stop_reminders))

    print("🚀 Bot is running...")
    try:
        asyncio.get_running_loop()
        app.run_polling()
    except RuntimeError:
        asyncio.run(app.run_polling())

if __name__ == "__main__":
    main()
