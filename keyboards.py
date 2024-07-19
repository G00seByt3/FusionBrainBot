from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from parametrs import ratio_params, styles_params

back_button = [[InlineKeyboardButton(text="⬅️ Back", callback_data='back')]]
exit_keyboard = InlineKeyboardMarkup(inline_keyboard=back_button)

rkb =[[InlineKeyboardButton(text=el, callback_data=f"ratio_{i}")] for i, el in enumerate(ratio_params)]
ratio_keyboard = InlineKeyboardMarkup(inline_keyboard=rkb)

skb = [[InlineKeyboardButton(text=el, callback_data=f"style_{i}")] for i, el in enumerate(styles_params)]
styles_keyboard = InlineKeyboardMarkup(inline_keyboard=skb)

mkb = [
    [InlineKeyboardButton(text="✅ Start generation", callback_data="start_generation")],
    [InlineKeyboardButton(text="📝 Enter prompt", callback_data='prompt')],
    [InlineKeyboardButton(text="⛔️ Negative promt", callback_data="negative_prompt")],
    [InlineKeyboardButton(text='🖥 Ratio', callback_data='choose_ratio'), 
     InlineKeyboardButton(text='⭐️ Style', callback_data='choose_style')],
]
main_keyboard = InlineKeyboardMarkup(inline_keyboard=mkb)
