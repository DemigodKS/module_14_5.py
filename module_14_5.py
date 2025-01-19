from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

# записываем ключ
api = "7230751067:AAF4T2f8bkFK_iFPC9FfkK8UHPRT8wySgg8"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State('1000')

#создаем клавиатуру внешнюю
kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Рассчитать"),
            KeyboardButton(text = "Информация"),
        ],
        [
            KeyboardButton(text = "Купить"),
            KeyboardButton(text = "Регистрация"),
        ]
    ], resize_keyboard=True)



#создаем клавиатуру внутреннюю
menu = InlineKeyboardMarkup()
button2 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
button3 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
menu.add(button2)
menu.add(button3)
menu2 = InlineKeyboardMarkup()
button5 = InlineKeyboardButton(text = 'Product1', callback_data="product_buying")
button6 = InlineKeyboardButton(text = 'Product2', callback_data="product_buying")
button7 = InlineKeyboardButton(text = 'Product3', callback_data="product_buying")
button8 = InlineKeyboardButton(text = 'Product4', callback_data="product_buying")
menu2.add(button5)
menu2.add(button6)
menu2.add(button7)
menu2.add(button8)


@dp.message_handler(commands = ["start"])
async def Start_message(message):
    #reply_markup=kb показываем клавиатуру
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup=kb)

@dp.message_handler(text = "Купить")
async def get_buying_list(message):

    products = get_all_products()
    for i in products:
            with open(f'files/{i[0]} бад.jpg', 'rb') as img:
                await message.answer(f"Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}")
                await message.answer_photo(img, reply_markup=kb)
    await message.answer("Выберите продукт для покупки:", reply_markup=menu2)

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    await message.answer("Выбери опцию", reply_markup=menu)

# обработка сообщений хендлеры
@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    value_data = (v for v in data.values())
    value_list = []
    for v in value_data:
        value_list.append(round(float(v),2))
    norma = 10 * value_list[2] + 6.25 * value_list[1] - 5 * value_list[0] + 5
    await message.answer(f"Ваша норма калорий {norma}")
    await state.finish()

@dp.message_handler(text = "Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'],data['email'],data['age'])
    await message.answer("Регистрация прошла успешно")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
