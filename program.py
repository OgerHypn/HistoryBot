import telebot
from config import *
import os
from mg import get_map_cell


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add('Аудио 11 класс📚')
    markup.add('ЕГЭ🎓')
    markup.add('YouTube📱')
    markup.add('Перевод баллов🧮')
    markup.add('Игры🎮')
    markup.add(('Библиотека обязательной литературы📜'))
    bot.send_message(message.chat.id, "Выберите класс или нажмите кнопку YouTube:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '10 Класс «История России» Мединский')
def HR10(message):
    bot.send_message(message.chat.id, "Отправка может занять время")
    bot.send_chat_action(message.chat.id, 'upload_document')
    document = open("Uchebnik/История России 10 класс Мединский.pdf", "rb")
    bot.send_document(message.chat.id, document)
    document.close()
    bot.send_message(message.chat.id, "Для получения полной подготовки на 💯, рекомендовано ознакомится со всем учебникам")


@bot.message_handler(func=lambda message: message.text == '10 Класс «Всеобщая История» Мединский')
def HR10(message):
    bot.send_message(message.chat.id, "Отправка может занять время")
    bot.send_chat_action(message.chat.id, 'upload_document')
    document = open("Uchebnik/Всеобщая История 10 класс Мединский.pdf", "rb")
    bot.send_document(message.chat.id, document)
    document.close()
    bot.send_message(message.chat.id, "Для получения полной подготовки на 💯, рекомендовано ознакомится со всем учебникам")


@bot.message_handler(func=lambda message: message.text == '11 Класс «История России» Мединский')
def HR11(message):
    bot.send_message(message.chat.id, "Отправка может занять время")
    bot.send_chat_action(message.chat.id, 'upload_document')
    document = open("Uchebnik/История России, 11 класс, Мединский.pdf", "rb")
    bot.send_document(message.chat.id, document)
    document.close()
    bot.send_message(message.chat.id, "Для получения полной подготовки на 💯, рекомендовано ознакомится со всем учебникам")

@bot.message_handler(func=lambda message: message.text == '11 Класс «Всеобщая История» Мединский')
def VH11(message):
    bot.send_message(message.chat.id, "Отправка может занять время")
    bot.send_chat_action(message.chat.id, 'upload_document')
    document = open("Uchebnik/Всеобщая история, 11 класс, Мединский.pdf", "rb")
    bot.send_document(message.chat.id, document)
    document.close()
    bot.send_message(message.chat.id, "Для получения полной подготовки на 💯, рекомендовано ознакомится со всем учебникам")


@bot.message_handler(func=lambda m: m.text == 'Библиотека обязательной литературы📜')
def Library(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add('⏎')
    markup.add('11 Класс «История России» Мединский')
    markup.add('11 Класс «Всеобщая История» Мединский')
    markup.add('10 Класс «История России» Мединский')
    markup.add('10 Класс «Всеобщая История» Мединский')
    bot.send_message(message.chat.id, "Учебники для повторения школьной программы", reply_markup=markup)



@bot.message_handler(func=lambda m: m.text == 'Игры🎮')
def game(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add('⏎')
    markup.add('Лабиринт🧱')
    bot.send_message(message.chat.id, "Вскоре может появится ещё игры", reply_markup=markup)

cols, rows = 8, 8

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('←', callback_data='left'),
			  telebot.types.InlineKeyboardButton('↑', callback_data='up'),
			  telebot.types.InlineKeyboardButton('↓', callback_data='down'),
			  telebot.types.InlineKeyboardButton('→', callback_data='right') )

maps = {}

def get_map_str(map_cell, player):
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += "🔴"
            else:
                map_str += "⬜"
        map_str += "\n"

    return map_str

@bot.message_handler(func=lambda m: m.text == 'Лабиринт🧱')
def play_message(message):
    map_cell = get_map_cell(cols, rows)

    user_data = {
		'map': map_cell,
		'x': 0,
		'y': 0
	}

    maps[message.chat.id] = user_data

    bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
	user_data = maps[query.message.chat.id]
	new_x, new_y = user_data['x'], user_data['y']

	if query.data == 'left':
		new_x -= 1
	if query.data == 'right':
		new_x += 1
	if query.data == 'up':
		new_y -= 1
	if query.data == 'down':
		new_y += 1

	if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
		return None
	if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
		return None

	user_data['x'], user_data['y'] = new_x, new_y

	if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
		bot.edit_message_text( chat_id=query.message.chat.id,
							   message_id=query.message.id,
							   text="Вы выиграли" )
		return None

	bot.edit_message_text( chat_id=query.message.chat.id,
						   message_id=query.message.id,
						   text=get_map_str(user_data['map'], (new_x, new_y)),
						   reply_markup=keyboard )



@bot.message_handler(func=lambda m: m.text == 'Перевод баллов🧮')
def calculator(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add('⏎')
    markup.add('Математика профиль', 'Русский язык', 'Физика')
    markup.add('Обществознание', 'История', 'Биология')
    markup.add('Информатика', 'Химия', 'Англиский язык')
    markup.add('Литература', 'География', 'Китайский язык')

    bot.send_message(message.chat.id, "Выберите предмет:", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == 'Математика профиль'or m.text == 'Русский язык' or m.text == 'Физика' or m.text == 'Обществознание' or m.text == 'История' or m.text == 'Биология' or \
                      m.text == 'Информатика' or m.text == 'Химия' or m.text == 'Англиский язык' or m.text == 'Литература' or m.text == 'География' or m.text == 'Китайский язык')
def ball(message):
    Predmet = message.text
    file_path = f"ZD History/{Predmet}.jpg"

    # Отправляем фото
    with open(file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == 'ЕГЭ🎓')
def EGE(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add('⏎')
    markup.add('🎁')
    for i in range(1, 22):
        markup.add(str(i) + Task)
    bot.send_message(message.chat.id, "Выберите задание: ", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.endswith('Задание'))
def Histori_exc(message):
    task_number = message.text.split(Task)[0]  # Получаем цифру перед символом '❓'

    # Создаем путь к файлу с отделенной цифрой
    file_path = f"ZD History/{task_number}.jpg"

    # Отправляем фото
    with open(file_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


    word_file_path = f"ZD History/{task_number}.docx"
    pdf_file_path = f"ZD History/{task_number}.pdf"

    # Проверяем, существует ли файл docx
    if os.path.exists(word_file_path):
        # Отправляем файл Word
        with open(word_file_path, 'rb') as docx:
            bot.send_document(message.chat.id, docx)
    else:
        if os.path.exists(pdf_file_path):
            with open(pdf_file_path, 'rb') as pdf:
                bot.send_document(message.chat.id, pdf)
        else:
            # Если файл docx не найден, выводим сообщение об ошибке
            bot.send_message(message.chat.id, "")
            # Получаем количество баллов за задание
        points = ball_dicts.get(task_number, '0')



        # Отправляем сообщение с количеством баллов
        bot.send_message(message.chat.id, f"За это задание вы можете набрать {points} баллов. На фото представлен пример этого задания, а в файле данна информация для этого задания")


@bot.message_handler(func=lambda message: message.text == '🎁')
def Podarok(message):
    bot.send_message(message.chat.id, "Отправка 🎁 может занять время")
    bot.send_chat_action(message.chat.id, 'upload_document')
    document = open("Podarok/Артасов 2023.pdf", "rb")
    bot.send_document(message.chat.id, document)
    document.close()
    bot.send_message(message.chat.id, "Очень надеюсь, что этот подарок поможет вам, в получении 💯")


@bot.message_handler(func=lambda message: message.text == '10 класс' or message.text == 'Аудио 11 класс📚')
def select_paragraph(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add('⏎')
    for i in range(1, 38):
        markup.add(str(i))
    bot.send_message(message.chat.id, "Выберите параграф:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '⏎')
def reply_to_start(message):
    start(message)


@bot.message_handler(func=lambda message: message.text == 'YouTube📱')
def open_youtube_channel(message):
    channel_name = "HistoryAudio"
    channel_link = "https://www.youtube.com/channel/UCEVp2mDLT_n74xQGeAlF7bQ"
    channel_description = "HistoryAudio - это канал, посвященный истории. Здесь вы найдёте аудиокниги по учебнику. Подпишитесь на канал, чтобы узнавать о новых видео!"

    text = f"📺 Канал {channel_name}\n\n{channel_description}\n\nСсылка на канал: {channel_link}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: message.text.isdigit() and (int(message.text) > 0 and int(message.text) < 37))
def send_video_test(message):
        paragraph_number = message.text
        if paragraph_number in video_links:
            video_link = video_links[paragraph_number]
            bot.send_message(message.chat.id, f"Ссылка на видео: {video_link}")
        else:
            bot.send_message(message.chat.id, "Ссылка на видео не найдена.")
        if paragraph_number in test_links:
            test_link = test_links[paragraph_number]
            bot.send_message(message.chat.id, f"{test_link}")
        else:
            bot.send_message(message.chat.id, "Ссылка на тест не найдена.")





bot.polling(none_stop=False, interval=0)
