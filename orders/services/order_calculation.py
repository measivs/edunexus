from decimal import Decimal


def calculate_final_price(base_price, discount_percentage=0, tax_percentage=0):
    """
        Calculates the final price, tax, and total amount for a course.

        Args:
            - `base_price` (Decimal): Original price of the course.
            - `discount_percentage` (int, optional): Discount applied to the course (default is 0).
            - `tax_percentage` (int, optional): Tax rate applied to the course (default is 0).

        Returns:
            - `final_price` (Decimal): Price after applying the discount.
            - `tax_amount` (Decimal): Amount of tax calculated on the discounted price.
            - `total_amount` (Decimal): Total price including tax.
    """
    discount = base_price * (Decimal(discount_percentage) / Decimal(100))
    final_price = base_price - discount
    tax_amount = final_price * (Decimal(tax_percentage) / Decimal(100))
    total_amount = final_price + tax_amount
    return final_price, tax_amount, total_amount
