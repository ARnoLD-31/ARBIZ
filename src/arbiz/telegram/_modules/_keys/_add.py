from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from ... import _decorators
from ..._base import BOT, DS
from .... import database


_message: Message

class _Add(StatesGroup):
    key: State = State()
    product: State = State()
    activation_type: State = State()
    link: State = State()
    mak: State = State()


@DS.message(Command("add_key"))
@_decorators.security
async def add_key(message: Message, state: FSMContext) -> Message:
    global _message

    _message = await message.answer("Enter key:")
    await state.set_state(_Add.key)
    return message


@DS.message(_Add.key)
@_decorators.security
async def ak_key(message: Message, state: FSMContext) -> None:
    await BOT.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await state.update_data(key=message.text)
    await _message.edit_text("Enter product:")
    await state.set_state(_Add.product)


@DS.message(_Add.product)
@_decorators.security
async def ak_product(message: Message, state: FSMContext) -> None:
    await BOT.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await state.update_data(product=message.text)
    await _message.edit_text("Enter activation type:")
    await state.set_state(_Add.activation_type)


@DS.message(_Add.activation_type)
@_decorators.security
async def ak_activation_type(message: Message, state: FSMContext) -> None:
    await BOT.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await state.update_data(activation_type=message.text)
    await _message.edit_text("Enter link (0 - None):")
    await state.set_state(_Add.link)


@DS.message(_Add.link)
@_decorators.security
async def ak_link(message: Message, state: FSMContext) -> None:
    await BOT.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await state.update_data(link=None if message.text == 0 else message.text)
    await _message.edit_text("Enter mak (1 or 0):")
    await state.set_state(_Add.mak)

@DS.message(_Add.mak)
@_decorators.security
async def ak_mak(message: Message, state: FSMContext) -> None:
    await BOT.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await state.update_data(mak=bool(message.text))
    data: dict = await state.get_data()
    key, product, activation_type, link, mak = data.values()
    await database.keys.add(key, product, activation_type, mak, 0, link)
    await _message.edit_text(f"Key added. Data: {data}")
    await state.clear()
