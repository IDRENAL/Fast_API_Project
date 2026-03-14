from fastapi import HTTPException

from app.database import SessionLocal
from app.schemas import CreateWalletRequest
from app.repository import wallets as wallets_reposytory


def get_wallet(wallet_name: str | None = None):
    db = SessionLocal()
    try:
        if wallet_name is None:
            wallets = wallets_reposytory.get_all_wallets(db)
            return {"total_balance": sum([w.amount for w in wallets])}

        if not wallets_reposytory.is_wallet_exist(db, wallet_name):
            raise HTTPException(status_code=404, detail=f"Wallet '{wallet_name}' not found")
        wallet = wallets_reposytory.get_wallet_balance_by_name(db, wallet_name)
        return {"wallet": wallet.name, "balance": wallet.balance}
    finally:
        db.close()

def create_wallets(wallet: CreateWalletRequest):
    db = SessionLocal()
    try:
        if wallets_reposytory.is_wallet_exist(db, wallet.name):
            raise HTTPException(status_code=400, detail=f"Wallet '{wallet.name}' already exists")


        wallet = wallets_reposytory.create_wallet(db, wallet.name, wallet.initial_balance)
        db.commit()
        return {
            "message": f"Wallet '{wallet.name}' created",
            "wallet": wallet.name,
            "balance": wallet.balance
        }
    finally:
        db.close()