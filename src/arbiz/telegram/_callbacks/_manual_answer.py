from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .._base import DS
from ... import avito

class _ManualAnswer(StatesGroup):
    chat_id: State = State()
    text: State = State()


@DS.callback_query(F.data.startswith("manual_answer"))
async def _manual_answer(callback: CallbackQuery, state: FSMContext) -> None:
    chat_id: str = callback.data.replace("manual_answer ", "")
    await state.update_data(chat_id=chat_id)
    await callback.message.answer("Enter your answer (only text supported):")
    await state.set_state(_ManualAnswer.text)
    await callback.answer()


@DS.message(_ManualAnswer.text)
async def _ma_text(message: Message, state: FSMContext) -> None:
    chat_id: str = (await state.get_data())["chat_id"]
    text: str = message.text
    await avito.api.messenger.send_message(chat_id=chat_id, text=text)
    await avito.api.messenger.mark_chat_as_read(chat_id=chat_id)
    await message.answer("Message sent")
    await state.clear()
