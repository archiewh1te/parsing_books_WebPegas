from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsMessagePrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsCallbackPrivate(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        return call.message.chat.type == types.ChatType.PRIVATE