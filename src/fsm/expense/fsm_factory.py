from . import (
    add_expense_fsm,
    get_expense_report_fsm,
    update_expense_fsm,
    delete_expense_fsm,
)
from src.services.expense import validators, expense_api_client, expense_service


class ExpenseFSMFactory:

    def __init__(
        self,
        validator: validators.ExpenseValidator,
        expense_api_client: expense_api_client.ExpenseAPIClient,
        report_service: expense_service.ExpenseReportService,
    ):
        self.validator = validator
        self.expense_api_client = expense_api_client
        self.report_service = report_service

    def create_add_fsm_service(self):
        return add_expense_fsm.AddExpenseFSMService(
            self.validator, self.expense_api_client
        )

    def create_report_fsm_service(self):
        return get_expense_report_fsm.GetReportFSMService(
            self.validator, self.report_service
        )

    def create_update_fsm_service(self):
        return update_expense_fsm.UpdateFSMService(
            self.validator, self.expense_api_client, self.report_service
        )

    def create_delete_fsm_service(self):
        return delete_expense_fsm.DeleteFSMService(
            self.validator, self.expense_api_client, self.report_service
        )
