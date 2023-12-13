import logging
import pandas as pd
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, \
    ApplicationBuilder

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define states for the conversation
FIRST_NAME, LAST_NAME, PHONE_NUMBER, APPOINTMENT = range(4)

# Load existing appointments from Excel file
df = pd.read_excel('appointment_list.xlsx')


async def start(update: Update, context: CallbackContext) -> int:
    # Check if the user already provided their first name
    if 'first_name' in context.user_data:
        return await get_last_name(update, context)

    # Filter out appointments with filled Full Name cells
    available_appointments = df[df['Full Name'].isna()]['Appointment'].tolist()

    if not available_appointments:
        await update.message.reply_text("Sorry! all appointment is full, Please try later!")
        return ConversationHandler.END

    keyboard = [['/cancel']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Hi, This is a appointment Bot, Please enter your first name!",
                                    reply_markup=reply_markup)
    return FIRST_NAME


async def save_appointment(update: Update, context: CallbackContext) -> int:
    # Check if there are any appointments available
    available_appointments = df[df['Full Name'].isna()]['Appointment'].tolist()

    if not available_appointments:
        await update.message.reply_text("All appointment is full, Please try later!")
        return ConversationHandler.END

    selected_appointment = update.message.text.strip()

    if selected_appointment not in available_appointments:
        keyboard = [[app] for app in available_appointments]
        reply_markup = {'keyboard': keyboard, 'one_time_keyboard': True}
        await update.message.reply_text("This appointment is not available, Please select from list",
                                        reply_markup=reply_markup)
        return APPOINTMENT

    # Update the corresponding Full Name and Phone Number cells
    index = df.loc[df['Appointment'] == selected_appointment].index[0]
    df.at[index, 'Full Name'] = f"{context.user_data['first_name']} {context.user_data['last_name']}"
    df.at[index, 'Phone Number'] = context.user_data['phone_number']

    # Save the updated DataFrame to the Excel file
    df.to_excel('appointment_list.xlsx', index=False)

    # Send a confirmation message
    await update.message.reply_text(f"System saves your appointment \n"
                                    f"Full name: {context.user_data['first_name']} "
                                    f"{context.user_data['last_name']}\n"
                                    f"Phone number: {context.user_data['phone_number']}\n"
                                    f"Appointment: {selected_appointment}")

    # Reset the conversation
    return ConversationHandler.END


async def get_first_name(update: Update, context: CallbackContext) -> int:
    context.user_data['first_name'] = update.message.text
    keyboard = [['/back', '/cancel']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(f" Perfect, {context.user_data['first_name']} Please enter your last name! ",
                                    reply_markup=reply_markup)
    return LAST_NAME


async def get_last_name(update: Update, context: CallbackContext) -> int:
    context.user_data['last_name'] = update.message.text
    keyboard = [['/back', '/cancel']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Thanks, Please enter your phone number!", reply_markup=reply_markup)
    return PHONE_NUMBER


async def get_phone_number(update: Update, context: CallbackContext) -> int:
    context.user_data['phone_number'] = update.message.text
    user_info_message = (f"Your information:\n"
                         f"First name: {context.user_data['first_name']}\n"
                         f"Last name: {context.user_data['last_name']}\n"
                         f"Phone number: {context.user_data['phone_number']}\n\n"
                         f"Is this information correct?")

    keyboard = [['/confirm', '/back', '/cancel']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(user_info_message, reply_markup=reply_markup)
    return APPOINTMENT


async def confirm(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Confirmation received. Proceeding to the next step.")
    return await save_appointment(update, context)


async def back(update: Update, context: CallbackContext) -> int:
    # Reset the user's data
    context.user_data.clear()

    # Return to the first name receiving section
    return await start(update, context)


async def cancel(update: Update, context: CallbackContext) -> int:
    # Reset the user's data
    context.user_data.clear()

    await update.message.reply_text("Conversation canceled. Type /start to start over.")
    return ConversationHandler.END


def main():
    application = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_first_name)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_last_name)],
            PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_number)],
            APPOINTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_appointment)],
        },
        fallbacks=[
            CommandHandler('back', back),
            CommandHandler('cancel', cancel),
            CommandHandler('confirm', confirm),
        ],
    )
    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()