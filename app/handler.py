import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.allapi.binanceApi as bp
import app.keyboards as kb
import app.utils as utils
import app.database.request as rq
from app.constants import Messages

router = Router()


class ChatAI(StatesGroup):
    prompting = State()
    wait = State()


@router.message(CommandStart())
async def start_cmd(message: Message):
    """
    Start command handler
    adds new user to the database
    """

    try:
        await utils.new_user(message.from_user.id)
        await message.answer(text=Messages.WELCOME, reply_markup=kb.main)
        logging.info(f"New user started bot: {message.from_user.id}")
    except Exception as e:
        logging.error(f"Error in start_cmd: {e}")
        await message.answer(Messages.ERROR_DATABASE)


@router.message(Command("q"))
async def track_cmd(message: Message):
    await message.answer("W")


@router.message(F.text == "Get prices")
async def get_price(message: Message):
    """Get prices command handler"""
    try:
        price = await bp.track_price()
        await message.answer(price)
        logging.info(f"User {message.from_user.id} requested prices")
    except Exception as e:
        logging.error(f"Error getting prices: {e}")
        await message.answer("Error getting prices. Please try again later.")


@router.message(F.text == "AI assistant")
async def get_chat(message: Message, state: FSMContext):
    """AI assistant command handler"""
    try:
        await message.answer(text=Messages.CHOOSE_MODEL, reply_markup=kb.close)
        await state.set_state(ChatAI.prompting)
        logging.info(f"User {message.from_user.id} started AI chat")
    except Exception as e:
        logging.error(f"Error in get_chat: {e}")
        await message.answer(Messages.ERROR_DATABASE)


@router.message(F.text == "Answer mode")
async def set_answer_mode(message: Message):
    """Get answer mode command handler"""
    await message.answer(text=Messages.CHOOSE_SYSTEM, reply_markup=kb.prepromt)


@router.callback_query(F.data.startswith("system_"))
async def system_message_set(callback: CallbackQuery):
    """Set communication model callback handler"""
    try:
        await callback.answer("")
        resp = callback.data.split("_")[1]
        await rq.update_system(callback.from_user.id, resp)
        await callback.message.answer(text=Messages.MODEL_CHOSEN.format(resp))
        logging.info(f"User {callback.from_user.id} set system message: {resp}")
    except Exception as e:
        logging.error(f"Error setting system message: {e}")
        await callback.message.answer(Messages.ERROR_DATABASE)


@router.callback_query(F.data.startswith("assistant_"))
async def ai_model_set(callback: CallbackQuery):
    """Set AI model callback handler"""
    try:
        await callback.answer("")
        resp = callback.data.split("_")[1]
        await rq.update_state(callback.from_user.id, resp)
        await callback.message.answer(
            text=Messages.MODEL_CHOSEN.format(resp), reply_markup=kb.close
        )
        logging.info(f"User {callback.from_user.id} set AI model: {resp}")
    except Exception as e:
        logging.error(f"Error setting AI model: {e}")
        await callback.message.answer(Messages.ERROR_DATABASE)


@router.message(ChatAI.prompting)
async def generate_text(message: Message, state: FSMContext):
    """
    Generate response to user message
    and send it back to the user
    """

    try:
        if message.text == "Exit":
            await message.reply(text=Messages.MAIN_MENU, reply_markup=kb.main)
            await state.clear()
            logging.info(f"User {message.from_user.id} exited AI chat")
        elif message.text == "Choose AI model":
            await message.answer(text=Messages.CHOOSE_MODEL, reply_markup=kb.assistant)
        else:
            messages_content = await utils.prepare_promt(
                message.from_user.id, message.text
            )
            await state.set_state(ChatAI.wait)

            response = await utils.generate_ai(message.from_user.id, messages_content)
            logging.info(f"Generated response for user {message.from_user.id}")

            await message.answer(response)
            await state.set_state(ChatAI.prompting)
    except Exception as e:
        logging.error(f"Error in generate_text: {e}")
        await message.answer(Messages.ERROR_GENERATION)
        await state.set_state(ChatAI.prompting)


@router.message(ChatAI.wait)
async def stop_gen(message: Message):
    await message.answer(Messages.WAIT_GENERATION)
