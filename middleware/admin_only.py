from aiogram import BaseMiddleware

# 7823851962
ADMINS = [123425]
class AdminOnlyMiddlware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if event.from_user.id not in ADMINS:
            await event.answer('You do not have permission')
            return

        return await handler(event, data)