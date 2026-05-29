from aiogram import Router, F
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from keyboards.order_keyboard import *
from api.fn_api import get_fn_user_info, get_fn_user_daily_info, get_fn_user_stats_raw, today_kyiv
from api.fn_downdetector import get_fortnite_statuses_ua
from database.db_manipulations import UsersDB

db = UsersDB()
from handlers import Order_status

router = Router()
storage = MemoryStorage()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Fn nickname:')
    await state.set_state(Order_status.save_username)


@router.message(StateFilter("*"), F.text == 'Оновити стату')
async def update_start_bot(message: Message, state: FSMContext):
    username = db.get_user_order_number(message.from_user.id)
    if username is None:
        await message.answer(text='Спочатку введи свій Fn нікнейм:')
        await state.set_state(Order_status.save_username)
        return
    ans = get_fn_user_info(username)
    await message.answer(text=ans, reply_markup=back_button_keyboard())
    await state.clear()


@router.message(Command(commands='new'))
async def update_nickname(message: Message, state: FSMContext):
    await message.answer(text='Fn nickname:')
    await state.set_state(Order_status.save_username)


@router.message(StateFilter(Order_status.save_username))
async def ping_fn(message: Message, state: FSMContext):
    db.process_user(message.from_user.id, message.text)
    await message.answer(text="Нікнейм збережено", reply_markup=back_button_keyboard())
    username = db.get_user_order_number(message.from_user.id)
    ans = get_fn_user_info(username)
    await message.answer(text=ans, reply_markup=back_button_keyboard())
    await state.clear()


@router.message(StateFilter("*"), F.text == 'Стата за цей сезон')
async def last_season_stat(message: Message, state: FSMContext):
    username = db.get_user_order_number(message.from_user.id)
    if username is None:
        await message.answer(text='Спочатку введи свій Fn нікнейм:')
        await state.set_state(Order_status.save_username)
        return
    ans = get_fn_user_info(username, "season")
    await message.answer(text=ans, reply_markup=back_button_keyboard())


STATUS_EMOJI = {
    "Працює": "🟢",
    "Технічне обслуговування": "🔧",
    "Погіршена робота": "🟡",
    "Частковий збій": "🟠",
    "Масовий збій": "🔴",
}


@router.message(StateFilter("*"), F.text == 'Статус Fortnite')
async def Status(message: Message, state: FSMContext):
    try:
        statuses = get_fortnite_statuses_ua()

        def fmt(key):
            val = statuses.get(key, 'Невідомо')
            return f"{STATUS_EMOJI.get(val, '⚪')} {val}"

        ans = (
            "<b>🎮 Статус Fortnite</b>\n\n"
            f"👥 Друзі, групи та повідомлення\n{fmt('Друзі, групи та повідомлення')}\n\n"
            f"🎙 Голосовий чат\n{fmt('Голосовий чат')}\n\n"
            f"🔍 Пошук матчу\n{fmt('Пошук матчу')}"
        )

        await message.answer(text=ans, parse_mode="HTML", reply_markup=back_button_keyboard())
    except Exception as e:
        await message.answer(
            text=f"Не вдалося отримати статус Fortnite: {e}",
            reply_markup=back_button_keyboard()
        )


@router.message(StateFilter("*"), F.text == 'Стата за сьогодні')
async def today_stat(message: Message, state: FSMContext):
    username = db.get_user_order_number(message.from_user.id)
    if username is None:
        await message.answer(text='Спочатку введи свій Fn нікнейм:')
        await state.set_state(Order_status.save_username)
        return
    ans = get_fn_user_daily_info(username, message.from_user.id, db)
    await message.answer(text=ans, parse_mode="HTML", reply_markup=back_button_keyboard())


@router.message(Command(commands='reset_daily'))
async def reset_daily_snapshot(message: Message):
    username = db.get_user_order_number(message.from_user.id)
    if username is None:
        await message.answer(text='Спочатку введи свій Fn нікнейм.')
        return
    today = today_kyiv()
    db.delete_daily_snapshot(message.from_user.id, today)
    result = get_fn_user_stats_raw(username)
    if result is None:
        await message.answer(text='Не вдалося отримати статистику для нового снепшоту.')
        return
    stats, account_type = result
    db.save_daily_snapshot(message.from_user.id, today, stats['kills'], stats['deaths'],
                           stats['wins'], stats['matches'], stats['minutes'], account_type)
    await message.answer(text='✅ Снепшот скинуто і перезнято прямо зараз.',
                         reply_markup=back_button_keyboard())


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='/new - змінити нікнейм\n/reset_daily - скинути денний снепшот\n')