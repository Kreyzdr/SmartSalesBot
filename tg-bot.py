import telebot
from telebot import types
from sekret.key import TELEGRAM_TOKEN
from sekret.key import id_tg_admin

# Токен бота
BOT_TOKEN = f"{TELEGRAM_TOKEN}"
bot = telebot.TeleBot(BOT_TOKEN)

# ID чата отдела продаж (заменить на свой или попросите заказчика)
SALES_CHAT_ID = f"{id_tg_admin}"

# Хранилище данных
user_data = {}


# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}! 👋\n\n"
        "Я AI-бот компании. Помогу вам:\n"
        "- Узнать о наших услугах\n"
        "- Заполнить бриф\n"
        "- Передать заявку в отдел продаж\n\n"
        "Напишите, чем я могу помочь, или введите команду:\n"
        "/brief — заполнить бриф\n"
        "/help — помощь"
    )


# Команда /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "Вот список доступных команд:\n"
        "/start — начать общение\n"
        "/brief — заполнить бриф для вашего проекта\n"
        "/help — список доступных команд\n"
        "\nЕсли у вас есть вопросы, просто напишите их!"
    )


# Команда /brief — заполнение брифа
@bot.message_handler(commands=['brief'])
def brief_command(message):
    # Начало заполнения брифа
    user_data[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "Давайте заполним бриф для вашего проекта. Я буду задавать вам вопросы.\n\n"
        "Как называется ваша компания?"
    )
    bot.register_next_step_handler(message, get_company_name)


def get_company_name(message):
    # Сохраняем название компании
    user_data[message.chat.id]['company_name'] = message.text
    bot.send_message(message.chat.id, "Опишите вашу основную задачу или проект:")
    bot.register_next_step_handler(message, get_project_description)


def get_project_description(message):
    # Сохраняем описание проекта
    user_data[message.chat.id]['project_description'] = message.text
    bot.send_message(message.chat.id, "Укажите ваш бюджет (примерно):")
    bot.register_next_step_handler(message, get_budget)


def get_budget(message):
    # Сохраняем бюджет
    user_data[message.chat.id]['budget'] = message.text
    bot.send_message(
        message.chat.id,
        "Спасибо! Теперь укажите ваши контактные данные (имя, телефон, email):"
    )
    bot.register_next_step_handler(message, get_contact_info)


def get_contact_info(message):
    # Сохраняем контактные данные
    user_data[message.chat.id]['contact_info'] = message.text

    # Отправляем заявку в отдел продаж
    bot.send_message(
        SALES_CHAT_ID,
        f"Новая заявка от бота:\n\n"
        f"Компания: {user_data[message.chat.id].get('company_name')}\n"
        f"Описание проекта: {user_data[message.chat.id].get('project_description')}\n"
        f"Бюджет: {user_data[message.chat.id].get('budget')}\n"
        f"Контакты: {user_data[message.chat.id].get('contact_info')}\n\n"
        f"Источник: Telegram"
    )

    # Завершение общения
    bot.send_message(
        message.chat.id,
        "Спасибо! Ваша заявка отправлена в отдел продаж. Мы свяжемся с вами в ближайшее время!"
    )


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_message(
        message.chat.id,
        "Простите, я пока не знаю, как ответить на этот вопрос. Попробуйте воспользоваться командой /help."
    )


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
