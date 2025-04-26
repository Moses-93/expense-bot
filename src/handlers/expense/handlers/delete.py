import logging
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.states.expenses import DeleteExpenseStates
from src.utils.message_provider import MessageProvider
from src.services.expense import expense_service
from src.core.messages.enums import DeleteExpenseMessage


logger = logging.getLogger(__name__)


class ExpenseDeleteHandler:
    def __init__(
        self,
        mutation_service: expense_service.ExpenseMutationService,
        keyboard_builder: expense_service.ExpenseKeyboardBuilder,
        message_provider: MessageProvider[DeleteExpenseMessage],
    ):
        self.mutation_service = mutation_service
        self.keyboard_builder = keyboard_builder
        self.message_provider = message_provider

    async def handle_start(self, message: Message, state: FSMContext):
        await state.clear()

        expense_keyboard = await self.keyboard_builder.build_keyboard(
            message.from_user.id
        )
        await state.set_state(DeleteExpenseStates.EXPENSE_ID)
        await message.answer(
            self.message_provider.get(DeleteExpenseMessage.START),
            reply_markup=expense_keyboard,
        )

    async def handle_delete_expense(self, callback: CallbackQuery, state: FSMContext):

        await self.mutation_service.delete(callback.data, callback.from_user.id)

        await callback.message.answer(
            self.message_provider.get(DeleteExpenseMessage.SUCCESS),
            parse_mode="Markdown",
        )
        await state.clear()
