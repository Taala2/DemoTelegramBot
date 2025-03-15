from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Get prices")],
        [KeyboardButton(text="AI assistant")],
    ],
    resize_keyboard=True,
)

close = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Choose AI model")],
        [KeyboardButton(text="Answer mode")],
        [KeyboardButton(text="Exit")],
    ],
    resize_keyboard=True,
)

assistant = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="DeepSeek", callback_data="assistant_deepseek")],
        [InlineKeyboardButton(text="Gemini", callback_data="assistant_gemini")],
    ]
)

prepromt = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Expert", callback_data="system_expert")],
        [InlineKeyboardButton(text="Humorist", callback_data="system_humorist")],
    ]
)

switch = "👉"


async def switch_smile(s: str):
    if s == "deepseek":
        return InlineKeyboardMarkup(
            key=[
                [
                    InlineKeyboardButton(
                        text=f"{switch} DeepSeek", callback_data="assistant_deepseek"
                    )
                ],
                [InlineKeyboardButton(text="Gemini", callback_data="assistant_gemini")],
            ],
            resize_keyboard=True,
        )
    else:
        return InlineKeyboardMarkup(
            key=[
                [
                    InlineKeyboardButton(
                        text="DeepSeek", callback_data="assistant_deepseek"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=f"{switch} Gemini", callback_data="assistant_gemini"
                    )
                ],
            ],
            resize_keyboard=True,
        )
