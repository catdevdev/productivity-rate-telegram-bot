import os
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from groq import Groq

# Initialize the Groq client with the provided API key
client = Groq(
    api_key="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"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I am a simple calculator bot. Send me a mathematical expression like '2 + 2 * 4' and I'll calculate the result for you.",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me a mathematical expression, and I'll calculate the result. For example, try '3 + 4' or '5 * 6'.")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    expression = update.message.text
    print(expression)
    group_id = update.message.chat_id
    print(group_id)
    try:
        # Use Groq API to evaluate the expression
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Calculate the following expression: {expression}. Output should be only number result!!",
                }
            ],
            model="llama3-8b-8192",
        )
        
        # Get the result from the response
        result = chat_completion.choices[0].message.content
        await update.message.reply_text(f"The result is: {result}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await update.message.reply_text("Sorry, I couldn't calculate the expression.")

def main() -> None:
    application = Application.builder().token("7442271112:AAE_8XnTO2CU89zT0DmmD2lhpPIFvPAI5xo").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
