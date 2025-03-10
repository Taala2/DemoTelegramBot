from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.allapi.binanceApi as bp
import app.keyboards as kb
import app.utils as utils

import app.database.request as rq

router = Router()

class ChatAI(StatesGroup):
    prompting = State()
    wait = State()

@router.message(CommandStart())
async def start_cmd(message: Message):
    await utils.new_user(message.from_user.id)
    await message.answer(text='Welcome', reply_markup=kb.main)

@router.message(Command('q'))
async def track_cmd(message: Message):
    await message.answer('W')

@router.message(F.text == 'Get prices')
async def get_price(message: Message):
    price = await bp.track_price()
    await message.answer(price)

@router.message(F.text == 'AI assistant')
async def get_chat(message: Message, state: FSMContext):
    await message.answer(text ='Choose AI model', reply_markup=kb.close)
    await state.set_state(ChatAI.prompting)

@router.message(F.text == 'Answer mode')
async def get_chat(message: Message):
    await message.answer(text='Choose system message:', reply_markup=kb.prepromt)

@router.callback_query(F.data.startswith('system_'))
async def ai_model_set(callback: CallbackQuery):
    await callback.answer('')
    resp = callback.data.split('_')[1]
    await rq.update_system(callback.from_user.id, resp)
    await callback.message.answer(text=f'You choosed! {resp}')

@router.callback_query(F.data.startswith('assistant_'))
async def ai_model_set(callback: CallbackQuery):
    await callback.answer('')
    resp = callback.data.split('_')[1]
    await rq.update_state(callback.from_user.id, resp)
    await callback.message.answer(text=f'You choosed! {resp}', reply_markup=kb.close)


@router.message(ChatAI.prompting)
async def generate_text(message: Message, state = FSMContext):
    if (message.text == 'Exit'):
        await message.reply(text='You are in the main menu', reply_markup = kb.main)
        await state.clear()
    elif (message.text == 'Choose AI model'):
        await message.answer(text='Choose model:', reply_markup=kb.assistant)
    else:
        messages_content = await utils.prepare_promt(message.from_user.id, message.text)
        await state.set_state(ChatAI.wait)

        response = await utils.generate_ai(message.from_user.id, messages_content)

        await message.answer(response)
        await state.set_state(ChatAI.prompting)


@router.message(ChatAI.wait)
async def stop_gen(message: Message):
    await message.answer('Подождите, ваш запрос генерируется')

# @router.message(F.text == _('Выйти из AI'))
# async def stop_ai(message: Message, state: FSMContext):
#     await message.reply(text=_('Вы в глваном меню'),reply_markup= await kb.get_main_keyboard())
#     await state.clear()
