from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import add_user, add_booking, get_bookings, delete_booking

router = Router()

days = {"date_mon": "Понедельник", "date_tue": "Вторник", "date_wed": "Среда", "date_thu": "Четверг"}


def main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Записаться", callback_data="book")
    builder.button(text="📋 Мои записи", callback_data="my_bookings")
    builder.button(text="❌ Отменить запись", callback_data="cancel_booking")
    builder.button(text="📞 Контакты", callback_data="contacts")
    builder.adjust(2)
    return builder.as_markup()


def back_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад", callback_data="back_main")
    return builder.as_markup()


@router.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    add_user(user_id=user.id, username=user.username or "", full_name=user.full_name or "")
    await message.answer(
        f"Привет, <b>{user.full_name}</b>! 🦷\nЯ помогу записаться к стоматологу.",
        reply_markup=main_menu()
    )


@router.callback_query(lambda c: c.data == "back_main")
async def back_main_handler(callback: types.CallbackQuery):
    await callback.message.edit_text("Главное меню 🦷", reply_markup=main_menu())
    await callback.answer()


@router.callback_query(lambda c: c.data == "book")
async def book_handler(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 Понедельник", callback_data="date_mon")
    builder.button(text="📅 Вторник", callback_data="date_tue")
    builder.button(text="📅 Среда", callback_data="date_wed")
    builder.button(text="📅 Четверг", callback_data="date_thu")
    builder.button(text="◀️ Назад", callback_data="back_main")
    builder.adjust(2, 2, 1)
    await callback.message.edit_text("Выберите день:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("date_"))
async def date_handler(callback: types.CallbackQuery):
    day = days.get(callback.data, "")
    builder = InlineKeyboardBuilder()
    builder.button(text="🕙 10:00", callback_data=f"time_10_{callback.data}")
    builder.button(text="🕛 12:00", callback_data=f"time_12_{callback.data}")
    builder.button(text="🕒 15:00", callback_data=f"time_15_{callback.data}")
    builder.button(text="🕔 17:00", callback_data=f"time_17_{callback.data}")
    builder.button(text="◀️ Назад", callback_data="book")
    builder.adjust(2, 2, 1)
    await callback.message.edit_text(f"День: <b>{day}</b>\nВыберите время:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("time_"))
async def time_handler(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    time = parts[1]
    date_key = "_".join(parts[2:])
    day = days.get(date_key, "")
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить", callback_data=f"confirm_{callback.data}")
    builder.button(text="◀️ Назад", callback_data=date_key)
    builder.adjust(1)
    await callback.message.edit_text(
        f"Вы выбрали:\n📅 <b>{day}</b>\n🕐 <b>{time}:00</b>\n\nПодтвердить запись?",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("confirm_"))
async def confirm_handler(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    time = parts[2]
    date_key = "_".join(parts[3:])
    day = days.get(date_key, "")
    add_booking(user_id=callback.from_user.id, day=day, time=f"{time}:00")
    await callback.message.edit_text(
        f"✅ Вы записаны!\n📅 <b>{day}</b> в <b>{time}:00</b>\n\nДо встречи 🦷",
        reply_markup=back_button()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "my_bookings")
async def my_bookings_handler(callback: types.CallbackQuery):
    bookings = get_bookings(callback.from_user.id)
    if not bookings:
        await callback.message.edit_text("📋 У вас нет активных записей.", reply_markup=back_button())
    else:
        text = "📋 <b>Ваши записи:</b>\n\n"
        for b in bookings:
            text += f"• {b['day']} в {b['time']}\n"
        await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()


@router.callback_query(lambda c: c.data == "cancel_booking")
async def cancel_booking_handler(callback: types.CallbackQuery):
    bookings = get_bookings(callback.from_user.id)
    if not bookings:
        await callback.message.edit_text("❌ Нет активных записей для отмены.", reply_markup=back_button())
    else:
        builder = InlineKeyboardBuilder()
        for b in bookings:
            builder.button(text=f"❌ {b['day']} {b['time']}", callback_data=f"del_{b['id']}")
        builder.button(text="◀️ Назад", callback_data="back_main")
        builder.adjust(1)
        await callback.message.edit_text("Выберите запись для отмены:", reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("del_"))
async def delete_booking_handler(callback: types.CallbackQuery):
    booking_id = int(callback.data.split("_")[1])
    delete_booking(booking_id)
    await callback.message.edit_text("✅ Запись отменена.", reply_markup=back_button())
    await callback.answer()


@router.callback_query(lambda c: c.data == "contacts")
async def contacts_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "📞 Телефон: +8 (342) 3513 3244 3\n📍 Адрес: ул. Пушкина 3320, Москва",
        reply_markup=back_button()
    )
    await callback.answer()