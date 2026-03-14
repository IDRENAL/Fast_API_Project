from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import OperationRequest
from app.repository import wallets as wallets_reposytory


def add_income(db: Session, operation: OperationRequest):
    if not wallets_reposytory.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found")

    wallet = wallets_reposytory.add_income(db, operation.wallet_name, operation.amount)
    db.commit()
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance
    }


def add_expense(db: Session, operation: OperationRequest):
    if not wallets_reposytory.is_wallet_exist(db, operation.wallet_name):
        raise HTTPException(status_code=404, detail=f"Wallet '{operation.wallet_name}' not found")
    wallet = wallets_reposytory.get_wallet_balance_by_name(db, operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {wallet.balance}"
        )

    wallet = wallets_reposytory.add_expense(db, operation.wallet_name, operation.amount)
    db.commit()
    return {
        "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": wallet.balance
    }
