from fastapi import HTTPException

from app.repository.wallets import BALANCE
from app.schemas import OperationRequest
from app.repository import wallets as wallets_reposytory

def add_income(operation: OperationRequest):
    if wallets_reposytory.is_wallet_exist(operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found")

    new_balance = wallets_reposytory.add_income()
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }


def add_expense(operation: OperationRequest):
    if wallets_reposytory.is_wallet_exist(operation.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{operation.wallet_name}' not found")
    balance = wallets_reposytory.get_wallet_balance_by_name(operation.wallet_name)
    if balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {balance}"
        )

    new_balance = wallets_reposytory.add_expense(operation.wallet_name)

    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": new_balance
    }