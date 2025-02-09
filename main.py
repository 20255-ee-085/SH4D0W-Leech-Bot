import logging
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)
from vars import BOT_TOKEN, ADMIN_ID, MAX_CONCURRENT_DOWNLOADS
from core import (
    process_txt_file,
    download_manager,
    generate_progress_bar,
    validate_url,
    sanitize_filename
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
GET_BATCH_NAME, GET_RESOLUTION, GET_CAPTION, GET_THUMBNAIL = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
    <b>🔥 W E L C O M E   T O</b>
    <b>🖤 S H 4 D 0 W   W O R L D S</b>
    <i>U N L E A S H E D   T H E   D A R K</i>
    
    /upload ➡️ Upload .txt file
    /help ➡️ Get assistance
    """
    await update.message.reply_text(welcome_msg, parse_mode='HTML')

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 Unauthorized access!")
        return
    await update.message.reply_text("📤 Send me a .txt file to process")
    return GET_BATCH_NAME

async def handle_txt_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        file = await update.message.document.get_file()
        context.user_data['file_path'] = await file.download_to_drive()
        await update.message.reply_text("📝 Enter batch name:")
        return GET_BATCH_NAME
    except Exception as e:
        logger.error(f"File handling error: {e}")
        await update.message.reply_text("❌ Error processing file!")
        return ConversationHandler.END

async def get_batch_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['batch_name'] = sanitize_filename(update.message.text)
    keyboard = [
        [InlineKeyboardButton("144p", callback_data='144')],
        [InlineKeyboardButton("360p", callback_data='360'),
         InlineKeyboardButton("720p", callback_data='720')],
        [InlineKeyboardButton("1080p", callback_data='1080')]
    ]
    await update.message.reply_text(
        "🎚 Select video resolution:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return GET_RESOLUTION

async def get_resolution(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['resolution'] = query.data
    await query.edit_message_text(f"Selected resolution: {query.data}p")
    await query.message.reply_text("📝 Enter caption for files:")
    return GET_CAPTION

async def get_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['caption'] = update.message.text[:500]  # Limit caption length
    await update.message.reply_text("🖼 Send thumbnail (JPEG) or /skip:")
    return GET_THUMBNAIL

async def get_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo = await update.message.photo[-1].get_file()
        context.user_data['thumbnail'] = await photo.download_to_drive()
    else:
        context.user_data['thumbnail'] = None
    await start_download(update, context)
    return ConversationHandler.END

async def start_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    try:
        with open(user_data['file_path'], 'r') as f:
            links = [line.strip() for line in f if validate_url(line.strip())]
        
        progress_msg = await update.message.reply_text(
            f"🚀 Starting download...\n"
            f"📁 Batch: {user_data['batch_name']}\n"
            f"🔄 Progress: {generate_progress_bar(0)}\n"
            f"📊 Total: {len(links)} files"
        )
        
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
        results = await download_manager(
            links,
            user_data,
            progress_msg,
            semaphore
        )
        
        stats = f"""
        ✅ Download Complete!
        📥 Successful: {results['success']}
        ❌ Failed: {results['failed']}
        📄 PDFs: {results['pdfs']}
        🎥 Videos: {results['videos']}
        """
        await progress_msg.edit_text(stats)
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        await update.message.reply_text("❌ Critical download error occurred!")

# Add proper error handling
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling update:", exc_info=context.error)
    await update.message.reply_text("⚠️ An unexpected error occurred. Please try again.")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', upload)],
        states={
            GET_BATCH_NAME: [MessageHandler(filters.Document.TXT, handle_txt_file)],
            GET_RESOLUTION: [CallbackQueryHandler(get_resolution)],
            GET_CAPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_caption)],
            GET_THUMBNAIL: [
                MessageHandler(filters.PHOTO | filters.Document.IMAGE, get_thumbnail),
                CommandHandler('skip', get_thumbnail)
            ]
        },
        fallbacks=[CommandHandler('cancel', lambda u,c: ConversationHandler.END)]
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start))
    application.add_error_handler(error_handler)
    
    application.run_polling()

if __name__ == "__main__":
    main()