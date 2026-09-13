from __future__ import annotations

import pyrogram
from pyrogram import raw, utils


class GetBotName:
    async def get_bot_name(
        self: pyrogram.Client,
        language_code: str = "",
        for_my_bot: int | str | None = None,
    ) -> str:
        """Get the current bot name for the given user language.

        Parameters:
            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code or an empty string.

            for_my_bot (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target bot.

        Returns:
            ``str``: The bot name.
        """
        bot_info = await self.invoke(
            raw.functions.bots.GetBotInfo(
                bot=utils.get_input_user(await self.resolve_peer(for_my_bot))
                if for_my_bot
                else None,
                lang_code=language_code,
            )
        )
        return bot_info.name
