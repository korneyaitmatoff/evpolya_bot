import logging

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import (
    CommandStart,
    ChatMemberUpdatedFilter,
    IS_NOT_MEMBER,
    IS_MEMBER,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    PreCheckoutQuery,
    ChatMemberUpdated
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.create_invoice_link import LabeledPrice
import telethon
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest

from config import (
    TOKEN,
    PROVIDER_TOKEN,
    API_ID,
    API_HASH,
    PHONE,
    GROUP_ID
)
from src.database import (
    add_row,
    Customers,
    Deals,
    set_success_deals,
    set_expired_date,
    get_deal_by_customer_telegram_id,
    get_active_user,
    set_chat_id
)

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=TOKEN)
client = TelegramClient(PHONE, API_ID, API_HASH)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(text=f"Привет, {message.from_user.full_name}!")

    # TODO: check subscription
    await message.answer(text="Проверяем подписку...")

    builder = InlineKeyboardBuilder()
    builder.attach(InlineKeyboardBuilder.from_markup(InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 месяц", callback_data="subcription_1"),
                InlineKeyboardButton(text="3 месяца", callback_data="subcription_3")
            ],
        ]
    )))

    if get_active_user(
            customer_telegram_id=message.from_user.id
    ) is None:
        await message.answer(
            text="У вас нет активной подписки. Для приобритения подписки выберите нужную подписку",
            reply_markup=builder.as_markup()
        )
    else:
        await message.answer(
            text="У вас уже есть активная подписка"
        )


@dp.callback_query(lambda c: c.data.startswith("subcription_"))
async def callback_1m(callback: CallbackQuery, state: FSMContext):
    month_count = callback.data.replace('subcription_', '')

    await callback.message.answer(text=f"Вы выбрали {month_count} месяц(а)")

    try:
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()

        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=f"Подписка на {month_count} месяц(а)",
            description="К оплате:",
            payload="Счет на оплату",
            currency="RUB",
            prices=[
                LabeledPrice(
                    label=f"Подписка на {month_count} месяц(а)",
                    amount=1999 * 100 if month_count == "1" else 3555 * 100,
                )
            ],
            provider_token=PROVIDER_TOKEN,
        )

        add_row(
            table=Deals,
            customer_telegram_id=callback.from_user.id,
            service_months=month_count
        )
    except Exception as e:
        logging.error(f"Ошибка при SendInvoice: {e}")


@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  # всегда отвечаем утвердительно
    except Exception as e:
        logging.error(f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")


@dp.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext):
    await message.reply(
        f"Платеж на сумму {message.successful_payment.total_amount // 100} "
        f"{message.successful_payment.currency} прошел успешно!"
    )
    logging.info(f"Получен платеж от {message.from_user.id}")
    current_state = await state.get_state()

    if current_state is not None:
        await state.clear()

    add_row(
        table=Customers,
        name=message.from_user.full_name,
        telegram_id=message.from_user.id
    )
    set_success_deals(
        customer_id=message.from_user.id
    )
    set_expired_date(
        customer_telegram_id=message.from_user.id,
        months=get_deal_by_customer_telegram_id(customer_telegram_id=message.from_user.id).service_months
    )

    user = await client.get_input_entity(message.from_user.username)
    group = await client.get_input_entity(GROUP_ID)

    await client(InviteToChannelRequest(
        channel=group,
        users=[user]
    ))


@dp.message(F.unsuccessful_payment)
async def process_unsuccessful_payment(message: Message, state: FSMContext):
    await message.reply("Не удалось выполнить платеж!")
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()


# member add handler
@dp.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def handle_add_member(event: ChatMemberUpdated):
    logging.info(
        f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
        f" добавлен в чат {event.chat.id}"
    )

    if get_active_user(
            customer_telegram_id=event.new_chat_member.user.id
    ) is None:
        logging.info(
            f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
            f" не имеет активной подписки"
        )

        # await bot.ban_chat_member(
        #     chat_id=event.chat.id,
        #     user_id=event.new_chat_member.user.id
        # )
        #
        # logging.info(
        #     f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
        #     f" заблокирован в чате {event.chat.id}"
        # )
    else:
        logging.info(
            f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
            f" имеет активную подписку"
        )

        set_chat_id(
            customer_telegram_id=event.new_chat_member.user.id,
            chat_id=event.chat.id
        )


# member remove handler
@dp.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def handler_remove_member(event: ChatMemberUpdated):
    logging.info(
        f"Пользователь {event.new_chat_member.user.full_name}, {event.new_chat_member.user.id}"
        f" покинул чат {event.chat.id}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    client.connect()

    if not client.is_user_authorized():
        try:
            client.send_code_request(phone=PHONE, force_sms=False)
            client.sign_in(
                phone=PHONE,
                code=input("Введите код: ")
            )
        except telethon.errors.rpcerrorlist.SessionPasswordNeededError:
            client.sign_in(
                password=input("Введите пароль: "),
            )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
