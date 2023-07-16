import telebot
from telebot import types
from json import load, dump
import re

choose_habits = ['about habit1', 'habit2', 'habit3', 'habit4', 'habit5', 'habit5']

TOKENRob = '5859251151:AAGMtdaTKIGvV1ShfAIrZte-3-9MYNRwwsg'

bot = telebot.TeleBot(token=TOKENRob)
commands = (
    ('program', 'Получить программу'),
    ('exercises', 'Упражнения'),
    ('shower', 'Про контрастный душ')
)
# bot.delete_my_commands()
bot.set_my_commands([types.BotCommand(*i) for i in commands])

with open('data_new.json', 'r') as file:
    data = load(file)

# markup for all of habits
all_habits_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton("Расположение будильника", callback_data='about habit1')
button2 = types.InlineKeyboardButton('Количество будильников', callback_data='about habit2')
button3 = types.InlineKeyboardButton('Стакан воды', callback_data='about habit3')
button4 = types.InlineKeyboardButton('Зарядка', callback_data='about habit4')
button5 = types.InlineKeyboardButton('Контрастный душ', callback_data='about habit5')
button6 = types.InlineKeyboardButton('Утро без помех', callback_data='about habit6')
all_habits_markup.add(button1, button2, button3, button4, button5, button6, row_width=2)

# markup to back to all habits from one of them
back_to_all_habits_markup = types.InlineKeyboardMarkup()
back_to_all_habits_button = types.InlineKeyboardButton('« Назад', callback_data='back to all habits')
back_to_all_habits_markup.add(back_to_all_habits_button)

# markup for asking user what does he want to know about exercises (why do we need or what do we need)
habit4_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('Зачем делать', callback_data='why do habit4')
button2 = types.InlineKeyboardButton('Что делать', callback_data='what do habit4')
habit4_markup.add(button1, button2, back_to_all_habits_button, row_width=2)

# markup to show instruction for each points of exercise program
habit4_what_do_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('1', callback_data='habit4_1')
button2 = types.InlineKeyboardButton('2', callback_data='habit4_2')
button3 = types.InlineKeyboardButton('3', callback_data='habit4_3')
button4 = types.InlineKeyboardButton('4', callback_data='habit4_4')
button5 = types.InlineKeyboardButton('5', callback_data='habit4_5')
button6 = types.InlineKeyboardButton('6', callback_data='habit4_6')
button7 = types.InlineKeyboardButton('7', callback_data='habit4_7')
button8 = types.InlineKeyboardButton('8', callback_data='habit4_8')
button9 = types.InlineKeyboardButton('9', callback_data='habit4_9')
button10 = types.InlineKeyboardButton('10', callback_data='habit4_10')
button11 = types.InlineKeyboardButton('11', callback_data='habit4_11')
button12 = types.InlineKeyboardButton('12', callback_data='habit4_12')
button13 = types.InlineKeyboardButton('13', callback_data='habit4_13')
button14 = types.InlineKeyboardButton('14', callback_data='habit4_14')
button15 = types.InlineKeyboardButton('15', callback_data='habit4_15')
button16 = types.InlineKeyboardButton('16', callback_data='habit4_16')
button17 = types.InlineKeyboardButton('17', callback_data='habit4_17')
button18 = types.InlineKeyboardButton('18', callback_data='habit4_18')
habit4_what_do_markup.add(
    button1, button2, button3, button4, button5, button6, button7, button8, button9, button10,
    button11, button12, button13, button14, button15, button16, button17, button18
)

# markup to back from program of exercises to asking
habit4_back_from_what_do_markup = types.InlineKeyboardMarkup()
back_button = types.InlineKeyboardButton('« Назад', callback_data='back to habit4 from what')
habit4_back_from_what_do_markup.add(back_button)

# markup for asking user what does he want to know about contrast shower (why do we need or what do we need)
habit5_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('Зачем делать', callback_data='why do habit5')
button2 = types.InlineKeyboardButton('Как делать', callback_data='what do habit5')
habit5_markup.add(button1, button2, back_to_all_habits_button, row_width=2)

# markup to back from program of shower to asking
habit5_back_to_about_markup = types.InlineKeyboardMarkup()
back_to_about_habit5_button = types.InlineKeyboardButton('« Назад', callback_data='back to about habit5')
habit5_back_to_about_markup.add(back_to_about_habit5_button)


# command for short view of habits
@bot.message_handler(commands=['start'])
def get_program(message):
    text = data.get('introduction')
    message_from_user_id = message.from_user.id
    with open('json_message_id.json', 'r') as f:
        json_data = load(f)

    bot.send_message(chat_id=message_from_user_id, text=text)

    with open('json_message_id.json', 'w') as f:
        json_data[str(message_from_user_id)] = [0, 0]
        dump(json_data, f, indent=2)


# detailed message about program
@bot.message_handler(commands=['program'])
def get_more_about_program(message):
    message_from_user_id = message.from_user.id
    with open('json_message_id.json', 'r') as f:
        json_data = load(f)

    first_last_user_message_id = json_data.get(str(message_from_user_id))[0]
    if first_last_user_message_id:
        bot.delete_message(
            chat_id=message_from_user_id,
            message_id=first_last_user_message_id
        )
    second_last_user_message_id = json_data.get(str(message_from_user_id))[1]
    if second_last_user_message_id:
        bot.delete_message(
            chat_id=message_from_user_id,
            message_id=second_last_user_message_id
        )

    sent_message = bot.send_message(
        chat_id=message_from_user_id,
        text=data.get("all_habits"),
        reply_markup=all_habits_markup
    )

    with open('json_message_id.json', 'w') as f:
        json_data[str(message_from_user_id)] = [str(sent_message.message_id), 0]
        dump(json_data, f, indent=2)


# command for short view of habits
@bot.message_handler(commands=['exercises'])
def get_exercises(message):
    text = data.get('about habit4').get('what do habit4')

    message_from_user_id = message.from_user.id
    with open('json_message_id.json', 'r') as f:
        json_data = load(f)

    first_last_user_message_id = json_data.get(str(message_from_user_id))[0]
    if first_last_user_message_id:
        bot.delete_message(
            chat_id=message_from_user_id,
            message_id=first_last_user_message_id
        )
    second_last_user_message_id = json_data.get(str(message_from_user_id))[1]
    if second_last_user_message_id:
        bot.delete_message(
            chat_id=message_from_user_id,
            message_id=second_last_user_message_id
        )

    first_sent_message = bot.send_message(
        chat_id=message.from_user.id,
        text=text,
        reply_markup=habit4_back_from_what_do_markup
    )
    second_sent_message = bot.send_message(
        chat_id=message.from_user.id,
        text='Выберите пункт из списка упражнений для получения инструкции по нему',
        reply_markup=habit4_what_do_markup
    )

    with open('json_message_id.json', 'w') as f:
        json_data[str(message_from_user_id)] = [str(first_sent_message.message_id), str(second_sent_message.message_id)]
        dump(json_data, f, indent=2)


# send a message with info about shower
@bot.message_handler(commands=['shower'])
def get_shower(message):
    text = data.get('about habit5', 'None').get('what do habit5')

    message_from_user_id = message.from_user.id
    with open('json_message_id.json', 'r') as f:
        json_data = load(f)

    first_last_user_message_id = json_data.get(str(message_from_user_id))[0]
    if first_last_user_message_id:
        bot.delete_message(
            chat_id=message_from_user_id,
            message_id=first_last_user_message_id
        )
    second_last_user_message_id = json_data.get(str(message_from_user_id))[1]
    if second_last_user_message_id:
        bot.delete_message(
            chat_id=message_from_user_id,
            message_id=second_last_user_message_id
        )

    sent_message = bot.send_message(
        chat_id=message.from_user.id,
        text=text,
        reply_markup=habit5_back_to_about_markup
    )

    with open('json_message_id.json', 'w') as f:
        json_data[str(message_from_user_id)] = [str(sent_message.message_id), 0]
        dump(json_data, f, indent=2)


# edit the message before to message about choosen habit
@bot.callback_query_handler(func=lambda call: call.data in data)
def about_the_habit(call):
    text = data.get(call.data, 'None')
    if call.data in ('about habit1', 'about habit2', 'about habit3', 'about habit6'):
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=back_to_all_habits_markup
        )
    elif call.data == 'about habit4':
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='Что вы хотите узнать про зарядку',
            reply_markup=habit4_markup
        )
    else:
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='Что вы хотите узнать про контрастный душ',
            reply_markup=habit5_markup
        )


# returm to all habits from choosen habit
@bot.callback_query_handler(func=lambda call: call.data == 'back to all habits')
def back_to_habits(call):
    text = data.get('all_habits')
    bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=all_habits_markup
    )


# edit message to message about 'why do habit4' or 'what do habit4' and sens a message to know more if "whaat do habit4
@bot.callback_query_handler(func=lambda call: call.data in ('why do habit4', 'what do habit4'))
def about_habit4(call):
    if call.data == 'why do habit4':
        text = data.get('about habit4').get('why do habit4')
        markup = types.InlineKeyboardMarkup()
        back_to_habit4_from_why_button = types.InlineKeyboardButton('« Назад', callback_data='back to habit4 from why')
        markup.add(back_to_habit4_from_why_button)
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup
        )
    if call.data == 'what do habit4':
        text = data.get('about habit4').get('what do habit4')
        message_from_user_id = call.from_user.id
        bot.edit_message_text(
            chat_id=message_from_user_id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=habit4_back_from_what_do_markup
        )
        second_sent_message = bot.send_message(
            chat_id=call.from_user.id,
            text='Выберите пункт из списка упражнений для получения инструкции по нему',
            reply_markup=habit4_what_do_markup
            # entities=[types.MessageEntity({'text_link': 'https://telegra.ph/Nilou-04-14', "text": "URL"})]
        )
        with open('json_message_id.json', 'r') as f:
            json_data = load(f)

        with open('json_message_id.json', 'w') as f:
            json_data[str(message_from_user_id)][1] = str(second_sent_message.message_id)
            dump(json_data, f, indent=2)


# edit new message to message about one of 18 exercises
@bot.callback_query_handler(func=lambda call: call.data in data.get('about habit4').get('details'))
def more_about_what_to_do(call):
    got_data = data.get('about habit4').get('details').get(call.data)
    title = got_data.get('title')
    content = got_data.get('content')
    link = got_data.get('link')
    if link:
        bot.edit_message_text(
            parse_mode="MarkdownV2",
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=f"[{re.escape(title)}]({re.escape(link)})\n\n{re.escape(content)}",
            reply_markup=habit4_what_do_markup
        )
    else:
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=f"{title}\n\n{content}",
            reply_markup=habit4_what_do_markup
        )


# edit the old message to message with question and delete new message if 'back to habit4 from what'
@bot.callback_query_handler(func=lambda call: call.data in ("back to habit4 from why", 'back to habit4 from what'))
def back_to_habit4(call):
    message_from_user_id = call.from_user.id
    bot.edit_message_text(
        chat_id=message_from_user_id,
        message_id=call.message.message_id,
        text='Что вы хотите узнать про зарядку',
        reply_markup=habit4_markup
    )

    with open('json_message_id.json', 'r') as f:
        json_data = load(f)

    if call.data == 'back to habit4 from what':
        bot.delete_message(
            chat_id=message_from_user_id,
            message_id=json_data[str(message_from_user_id)][1]
        )

    with open('json_message_id.json', 'w') as f:
        json_data[str(message_from_user_id)][1] = 0
        dump(json_data, f, indent=2)


@bot.callback_query_handler(func=lambda call: call.data in ('why do habit5', 'what do habit5'))
def about_habit5(call):
    text = data.get('about habit5', 'None').get(call.data)
    bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=habit5_back_to_about_markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'back to about habit5')
def back_to_about_habit5(call):
    bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        text='Что вы хотите узнать про контрастный душ',
        reply_markup=habit5_markup
    )


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    bot.delete_webhook()
    main()
