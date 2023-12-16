# appointment-telegram-bot
ربات تلگرام نوبت دهی توسط پایتون
Appointment Telegram Bot by Python

Appointment Bot using Telegram and Python
This Telegram bot allows users to schedule appointments through a conversation flow. The bot is built using the Python programming language and utilizes the Telegram API for communication.

این ربات تلگرام به کاربران اجازه می دهد تا از طریق گفتگو، نوبت های موجود را مشاهده کننده و نوبت مورد نظر را انتخاب کنند. این ربات با استفاده از زبان برنامه نویسی پایتون ساخته شده است و از API تلگرام برای ارتباط استفاده می کند.

Features
Appointment Scheduling: Users can schedule appointments by providing their first name, last name, and phone number.

کاربران می توانند با ارائه نام، نام خانوادگی و شماره تلفن خود، زمان مورد نظر خود را انتخاب کنند.


Availability Check: The bot checks for available appointment slots and informs the user if all slots are filled.

ربات نوبت های موجود را بررسی می کند و به کاربر نوبت های موجود و آزاد را نمایش می دهد 

Confirmation: Users receive a confirmation message before the appointment is saved.

Installation
Clone the repository:

git clone https://github.com/ehsan-shiasi/appointment-bot.git
Install the required dependencies:

pip install -r requirements.txt
Set up a Telegram bot and obtain the token. Insert the token in the main() function:

application = ApplicationBuilder().token('YOUR_BOT_TOKEN').build()
Usage
Run the bot:

python your_bot_script.py
Start a conversation with the bot by typing /start.

Follow the instructions provided by the bot to schedule an appointment.

Conversation Flow
Start: /start initiates the conversation and prompts the user to enter their first name.

First Name: User enters their first name.

Last Name: User enters their last name.

Phone Number: User enters their phone number.

Appointment Selection: User selects an available appointment slot.

Confirmation: User confirms the provided information.

Completion: The bot saves the appointment and provides a confirmation message.

Commands
/start: Start the appointment scheduling process.

/back: Go back to the previous step in the conversation.

/cancel: Cancel the appointment scheduling process.

/confirm: Confirm the provided information and proceed to save the appointment.

Excel Integration
The bot loads existing appointments from an Excel file (appointment_list.xlsx) and updates it after each successful appointment scheduling. Ensure the file exists and is in the correct format.

