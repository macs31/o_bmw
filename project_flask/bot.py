import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import ApplicationBuilder
# Добавим необходимый объект из модуля telegram.ext
from forms.user_forms import RegisterForm, LoginForm
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from data import db_session
from data.users import User

proxy_url = "socks5://user:pass@host:port"
app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).build()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
reply_keyboard = [['/start'], ['/cars', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
a = []


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'Привет {user.mention_html()}!'
        '\n'
        'Я - бот AutoInfo!\n'
        'Пользуясь моими услугами ты можешь узнать больше информации о такой марке машин, как BMW\n',
        reply_markup=markup)


async def help(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}!"
        '\n'
        'Если вдруг у тебя появились вопросы,\n'
        'то ты можешь написать в тех поддержку \n'
        'Почта: macsim31082006@gmail.com\n'
        'Telegram: @macsim3108\n')


async def cars(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'{user.mention_html()}, вы можете узнать информацию о некоторых машинах из этого списка!'
        '\n'
        '/BMW_X7 \n'
        '/BMW_X6 \n'
        '/BMW_X5 \n'
        '/BMW_M4 \n'
        '/BMW_M5_F90 \n'
        '/BMW_I8 \n'
        'Для того, чтобы получить информацию о машине, нажмите на её название в списке\n'
        , reply_markup=markup)


async def BMW_X7(update, context):
    await update.message.reply_photo('static/img/cars/bmw_x7/bmw_x7.jpg')
    await update.message.reply_html(
        'Вид топлива: бензин/дизель\n'
        'Расход топлива: 12.8–7.7 л/100 км\n'
        'Максимальная скорость(km/h): 245\n'
        'Мощность, л.с. при об/мин: 340 5500–6500\n'
        'Разгон(1-100 km/h): 6,1\n'
        'Цена: от 9.500.000 руб.\n',
        reply_markup=markup)


async def BMW_X6(update, context):
    await update.message.reply_photo('static/img/cars/bmw_x6/bmw_x6.jpg')
    await update.message.reply_text(
        'Вид топлива: бензин/дизель\n'
        'Расход топлива: 11,5/100 км\n'
        'Максимальная скорость(km/h): 245\n'
        'Мощность, л.с. при об/мин: 345 6000–6500\n'
        'Разгон(1-100 km/h), с: 4,3\n'
        'Цена: от 8 400 000 руб.\n', reply_markup=markup)


async def BMW_X5(update, context):
    await update.message.reply_photo('static/img/cars/bmw_x5/bmw_x5.jpg')
    await update.message.reply_text(
        'Вид топлива: бензин/дизель\n'
        'Расход топлива: 9,2/100 км\n'
        'Максимальная скорость(km/h): 256\n'
        'Мощность, л.с. при об/мин: 440 5000–6000\n'
        'Разгон(1-100 km/h), с: 5,5\n'
        'Цена: от 7 190 000 руб.', reply_markup=markup)


async def BMW_M4(update, context):
    await update.message.reply_photo('static/img/cars/bmw_M4/bmw_m4.jpg')
    await update.message.reply_text(
        'Вид топлива: бензин\n'
        'Расход топлива: 10,1 л/100 км\n'
        'Максимальная скорость(km/h): 307\n'
        'Мощность, кВт (л.с.) при об/мин: 551 6250\n'
        'Разгон(1-100 km/h): 3,7\n'
        'Цена: от 9.000.000 руб.\n', reply_markup=markup)


async def BMW_I8(update, context):
    await update.message.reply_photo('static/img/cars/bmw_i8/bmw_i8.jpg')
    await update.message.reply_text(
        'Вид топлива: гибрид\n'
        'Расход топлива: 1.9 л/100 км\n'
        'Максимальная скорость(km/h): 250\n'
        'Мощность, л.с. при об/мин: 231  5800\n'
        'Разгон(1-100 km/h): 4.4\n'
        'Цена: от 9.490.000 руб.\n', reply_markup=markup)


async def BMW_M5_F90(update, context):
    await update.message.reply_photo('static/img/cars/bmw_M5_F90/bmw_m5_f90.jpg')
    await update.message.reply_text(
        'Вид топлива: бензин\n'
        'Расход топлива: 10,6 л/100 км\n'
        'Максимальная скорость(km/h): 250\n'
        'Мощность, л.с. при об/мин: 625 6500–7500\n'
        'Разгон(1-100 km/h): 3,3\n'
        'Цена: от 11.450.000 руб.\n', reply_markup=markup)


def main():
    application = Application.builder().token('6286604292:AAEiaEIRDCm1AxYTfqPdBAw_QwL1vRus6hM').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("BMW_X7", BMW_X7))
    application.add_handler(CommandHandler("BMW_X6", BMW_X6))
    application.add_handler(CommandHandler("BMW_X5", BMW_X5))
    application.add_handler(CommandHandler("BMW_M4", BMW_M4))
    application.add_handler(CommandHandler("BMW_M5_F90", BMW_M5_F90))
    application.add_handler(CommandHandler("BMW_I8", BMW_I8))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("cars", cars))
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
