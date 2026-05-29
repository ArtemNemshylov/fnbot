from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

back_button = KeyboardButton(text='Оновити стату')
help_btn = KeyboardButton(text='/help')
this_season_text = KeyboardButton(text='Стата за цей сезон')
status_button = KeyboardButton(text='Статус Fortnite')
today_stat_button = KeyboardButton(text='Стата за сьогодні')


def back_button_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [back_button],
            [this_season_text, today_stat_button],
            [status_button],
            [help_btn],
        ],
        resize_keyboard=True
    )
    return keyboard