from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from forms import RegisterUser, UpdateUser, GetUser, DeleteUser
from client import (
    register_user,
    get_all_users,
    get_user_by_id,
    delete_user_by_id,
    update_user_by_id
)


router = Router()

markup = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="By ID", callback_data="sort:id:asc"),
            InlineKeyboardButton(text="By Name", callback_data="sort:name:asc"),
            InlineKeyboardButton(text="By Email", callback_data="sort:email:asc"),
        ],
        [
            InlineKeyboardButton(text="ASC", callback_data="sort:current:asc"),
            InlineKeyboardButton(text="DESC", callback_data="sort:current:desc")
        ]
    ]
)

current_sort = {'order_by': 'id','direction': 'asc'}

@router.message(F.text.in_({'/start', '/add'}))
async def start(msg: Message, state: FSMContext) -> None:
    await state.set_state(RegisterUser.name)
    await msg.answer("Please enter your name:")

@router.message(RegisterUser.name)
async def get_name(msg: Message, state: FSMContext) -> None:
    await state.update_data(name=msg.text)
    await state.set_state(RegisterUser.email)
    await msg.answer("Please enter your email:")

@router.message(RegisterUser.email)
async def get_email(msg: Message, state: FSMContext) -> None:
    # await state.update_data(email=msg.text)
    data = await state.get_data()
    name = data.get('name')
    email = msg.text
    success = await register_user(name=name, email=email)
    if success:
        await msg.answer("You have been registered successfully!", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("Failed to register. Please try again.")
    await state.clear()

@router.message(F.text == '/users')
async def list_users(msg: Message):
    users = await get_all_users(order_by=current_sort['order_by'], direction=current_sort['direction'])
    if not users:
        await msg.answer("No users found.")
        return

    text="<b>Registered Users:</b>\n\n"
    for user in users:
        text += f"{user['name']} - {user['email']}\n"
    await msg.answer(text, reply_markup=markup)

@router.callback_query(F.data.startswith("sort:"))
async def sort_users(callback: CallbackQuery):
    parts = callback.data.split(":")
    field = parts[1]
    direction = parts[2]

    if field == "current":
        current_sort['direction'] = direction
    else:
        current_sort['order_by'] = field
        current_sort['direction'] = direction

    users = await get_all_users(order_by=current_sort['order_by'], direction=current_sort['direction'])
    if not users:
        await callback.message.edit_text("No users found.")
        return

    text="<b>Registered Users:</b>\n\n"
    for user in users:
        text += f"{user['name']} - {user['email']}\n"

    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.message(F.text == '/get')
async def get_user_start(msg: Message, state: FSMContext):
    await state.set_state(GetUser.id)
    await msg.answer("Please enter the user ID:")

@router.message(GetUser.id)
async def get_user_by_id_func(msg: Message, state: FSMContext):
    user = await get_user_by_id(int(msg.text))
    if user:
        await msg.answer(f"User ID: {user['id']}\nName: {user['name']}\nEmail: {user['email']}")
    else:
        await msg.answer("User not found.")
    await state.clear()

@router.message(F.text == '/update')
async def update_user_start(msg: Message, state: FSMContext):
    await state.set_state(UpdateUser.id)
    await msg.answer("Please enter the user ID to update:")

@router.message(UpdateUser.id)
async def update_user_get_id(msg: Message, state: FSMContext):
    await state.update_data(id=int(msg.text))
    await state.set_state(UpdateUser.name)
    await msg.answer("Please enter the new name:")

@router.message(UpdateUser.name)
async def update_user_get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(UpdateUser.email)
    await msg.answer("Please enter the new email:")

@router.message(UpdateUser.email)
async def update_user_get_email(msg: Message, state: FSMContext):
    data = await state.get_data()
    success = await update_user_by_id(user_id=data['id'], name=data['name'], email=msg.text)
    if success:
        await msg.answer("User updated successfully!")
    else:
        await msg.answer("Failed to update user. Please check the ID and try again.")
    await state.clear()

@router.message(F.text == '/delete')
async def delete_user_start(msg: Message, state: FSMContext):
    await state.set_state(DeleteUser.id)
    await msg.answer("Please enter the user ID to delete:")

@router.message(DeleteUser.id)
async def delete_user_get_id(msg: Message, state: FSMContext):
    success = await delete_user_by_id(int(msg.text))
    if success:
        await msg.answer("User deleted successfully!")
    else:
        await msg.answer("Failed to delete user. Please check the ID and try again.")
    await state.clear()

@router.message(F.text == '/secret_option')
async def secret_option(msg: Message):
    await msg.answer("This is a secret option! I love Bagul!\n")