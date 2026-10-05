import json
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "customers.json"

print(f"Loading customer data from: {DATA_PATH}")

def check_customer_history(customer_id: str) -> dict:
    """
    Retrieve customer account and support history.
    """

    with open(DATA_PATH, "r", encoding="utf-8") as file:
        customers = json.load(file)

    customer = customers.get(customer_id)
    if customer is None:
        return {
            "found": False,
            "message": f"Customer {customer_id} not found."
        }

    return {
        "found": True,
        "customer_id": customer_id,
        **customer
    }