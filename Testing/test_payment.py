import uuid
from square.client import Client

# 🔧 Replace these with your actual values from the sandbox
SANDBOX_ACCESS_TOKEN = 'EAAAlzQKFeaY3Zv20cu3t3jdty0wNvNxyUhONVjMKnXvLHVl7P6hmvUd-yMMszK9'
LOCATION_ID = 'LSHJCCAJRRY95'
CUSTOMER_ID = 'ZM06EF241431C8PPTDX86PK2XG'

client = Client(
    access_token=SANDBOX_ACCESS_TOKEN,
    environment='sandbox'
)

# STEP 1: Create an Order with Line Items
order_body = {
    "order": {
        "location_id": LOCATION_ID,
        "customer_id": CUSTOMER_ID,
        "line_items": [
            {
                "name": "surfboards",
                "quantity": "2",
                "base_price_money": {
                    "amount": 20000,  # = $20.00
                    "currency": "AUD"
                }
            },
            {
                "name": "wax",
                "quantity": "1",
                "base_price_money": {
                    "amount": 400,  # = $5.00
                    "currency": "AUD"
                }
            }
        ]
    },
    "idempotency_key": str(uuid.uuid4())
}

create_order_result = client.orders.create_order(body=order_body)

if create_order_result.is_success():
    order_id = create_order_result.body['order']['id']
    print(f"✅ Order created: {order_id}")
else:
    print("❌ Failed to create order")
    print(create_order_result.errors)
    exit()

# STEP 2: Create a Payment for the Order
payment_body = {
    "source_id": "cnon:card-nonce-ok",  # Square test nonce
    "idempotency_key": str(uuid.uuid4()),
    "amount_money": {
        "amount": 40400,  # must match order total exactly
        "currency": "AUD"
    },
    "order_id": order_id,
    "location_id": LOCATION_ID,
    "customer_id": CUSTOMER_ID
}

create_payment_result = client.payments.create_payment(body=payment_body)

if create_payment_result.is_success():
    payment = create_payment_result.body['payment']
    print(f"✅ Payment succeeded. Payment ID: {payment['id']}")
else:
    print("❌ Payment failed")
    print(create_payment_result.errors)


