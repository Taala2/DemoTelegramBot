from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)


main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Get prices')],
        [KeyboardButton(text="AI assistant")]
    ], resize_keyboard=True)

close = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Choose AI model")],
        [KeyboardButton(text="Answer mode")],
        [KeyboardButton(text="Exit")]
    ], resize_keyboard=True)

assistant = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="DeepSeek", callback_data='assistant_deepseek')],
    [InlineKeyboardButton(text="Gemini", callback_data='assistant_gemini')]
])

prepromt = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Expert", callback_data='system_expert')],
    [InlineKeyboardButton(text="Humorist", callback_data='system_humorist')]
])

# async def get_main_keyboard():
#     return ReplyKeyboardMarkup(keyboard=[
#         [KeyboardButton(text="Посмотреть цены")],
#         [KeyboardButton(text="AI помощник")]
#     ], resize_keyboard=True)

# async def get_close_keyboard():
#     return ReplyKeyboardMarkup(keyboard=[
#         [KeyboardButton(text="Выйти из AI")]
#     ], resize_keyboard=True)

# async def get_lang_keyboard():
#     return InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="English", callback_data="set_language_en")],
#         [InlineKeyboardButton(text="Русский", callback_data="set_language_ru")]
#     ])
