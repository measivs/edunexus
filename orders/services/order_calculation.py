from decimal import Decimal


def calculate_final_price(base_price, discount_percentage=0, tax_percentage=0):
    discount = base_price * (Decimal(discount_percentage) / Decimal(100))
    final_price = base_price - discount
    tax_amount = final_price * (Decimal(tax_percentage) / Decimal(100))
    total_amount = final_price + tax_amount
    return final_price, tax_amount, total_amount
