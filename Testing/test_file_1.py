import csv
from square.client import Client

# Replace with your Square Sandbox Access Token
access_token = 'EAAAlzQKFeaY3Zv20cu3t3jdty0wNvNxyUhONVjMKnXvLHVl7P6hmvUd-yMMszK9'

# Initialize Square Client (Keeping the original access_token method)
client = Client(
    access_token=access_token,
    environment="sandbox"
)

# ✅ Replace this with the actual Customer ID
customer_id = "ZM06EF241431C8PPTDX86PK2XG"

# Fetch customer details
customer_response = client.customers.retrieve_customer(customer_id)

if customer_response.is_success():
    customer = customer_response.body["customer"]
    
    # Fetch only the cards belonging to this customer
    cards_response = client.cards.list_cards(customer_id=customer_id)

    customer_cards = []
    if cards_response.is_success():
        customer_cards = cards_response.body.get("cards", [])

    # Prepare CSV file
    csv_filename = "customer_data_with_cards.csv"
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow([
            "Customer ID", "First Name", "Last Name", "Email", "Phone", "Created At",
            "Card ID", "Card Brand", "Last 4 Digits", "Expiration Month", "Expiration Year"
        ])
        
        # Write customer & card data
        if customer_cards:
            for card in customer_cards:
                writer.writerow([
                    customer.get("id", "N/A"),
                    customer.get("given_name", "N/A"),
                    customer.get("family_name", "N/A"),
                    customer.get("email_address", "N/A"),
                    customer.get("phone_number", "N/A"),
                    customer.get("created_at", "N/A"),
                    card.get("id", "N/A"),
                    card.get("card_brand", "N/A"),
                    card.get("last_4", "N/A"),
                    card.get("exp_month", "N/A"),
                    card.get("exp_year", "N/A")
                ])
        else:
            # Write customer row with no card details
            writer.writerow([
                customer.get("id", "N/A"),
                customer.get("given_name", "N/A"),
                customer.get("family_name", "N/A"),
                customer.get("email_address", "N/A"),
                customer.get("phone_number", "N/A"),
                customer.get("created_at", "N/A"),
                "No Card", "No Card", "No Card", "No Card", "No Card"
            ])
    
    print(f"✅ CSV file '{csv_filename}' created successfully with customer & card data!")
else:
    print("❌ Failed to retrieve customer. Error:", customer_response.errors)
