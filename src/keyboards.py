from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from configs.config_reader import cfg

back_button = [[InlineKeyboardButton(text="⬅️ Back", callback_data='back')]]
exit_keyboard = InlineKeyboardMarkup(inline_keyboard=back_button)

skb = [[InlineKeyboardButton(text=style.capitalize(), callback_data=style)] for style in cfg.styles]
styles_keyboard = InlineKeyboardMarkup(inline_keyboard=skb)

mkb = [
    [InlineKeyboardButton(text="✅ Start generation", callback_data="start_generation")],
    [InlineKeyboardButton(text="📝 Enter prompt", callback_data='prompt')],
    [InlineKeyboardButton(text="⛔️ Negative promt", callback_data="negative_prompt")],
    [InlineKeyboardButton(text='⭐️ Style', callback_data='choose_style')]
]
main_keyboard = InlineKeyboardMarkup(inline_keyboard=mkb)
