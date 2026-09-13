from __future__ import annotations

import pyrogram
from pyrogram import raw, utils


class RefundStarPayment:
    async def refund_star_payment(
        self: pyrogram.Client,
        user_id: int | str,
        telegram_payment_charge_id: str,
    ) -> bool:
        """Refunds a successful payment in Telegram Stars.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user, whose payment will be refunded.

            telegram_payment_charge_id (``str``):
                Telegram payment identifier.

        Returns:
            ``bool``: True on success
        """
        r = await self.invoke(
            raw.functions.payments.RefundStarsCharge(
                user_id=utils.get_input_user(await self.resolve_peer(user_id)),
                charge_id=telegram_payment_charge_id,
            )
        )
        return bool(r)
