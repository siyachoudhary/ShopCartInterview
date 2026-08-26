"""ShopCart — a tiny in-memory shopping cart.

Prices are plain numbers (dollars). A cart holds "line items": one line per distinct
product, each with a unit price and a quantity.

The docstrings below describe what each method is *supposed* to do. The behavioral tests
in tests/test_cart.py check that intent. Some implementations don't match their
description — those are the bugs you're here to find.
"""


class Item:
    def __init__(self, name, unit_price, quantity=1):
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity

    def __repr__(self):
        return f"Item({self.name!r} x{self.quantity} @ {self.unit_price})"


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, unit_price, quantity=1):
        """Add units of a product to the cart.

        If the product is already in the cart, increase that line's quantity instead of
        creating a second line for the same product.
        """
        self.items.append(Item(name, unit_price, quantity))
        return self.items[-1]

    def get_item(self, name):
        """Return the line item for the given product name, or None if it isn't here."""
        for item in self.items:
            if item.name == name:
                return item
        return None

    def remove_item(self, name):
        """Remove the line for the given product (a no-op if it isn't here)."""
        self.items = [item for item in self.items if item.name != name]

    def unit_count(self):
        """Total number of individual units in the cart (sum of every line's quantity)."""
        return len(self.items)

    def subtotal(self):
        """Sum of unit_price * quantity across every line."""
        return sum(item.unit_price for item in self.items)

    def most_expensive(self):
        """Return the line item with the highest unit price, or None if the cart is empty."""
        if not self.items:
            return None
        return min(self.items, key=lambda item: item.unit_price)

    def total(self, discount_rate=0.0):
        """Subtotal after applying a discount rate in [0, 1].

        A rate of 0.2 means "20% off", i.e. the customer pays 80% of the subtotal.
        """
        return self.subtotal() * discount_rate

    def free_shipping(self, threshold):
        """True if the subtotal qualifies for free shipping.

        The order ships free once the subtotal reaches the threshold (at or above it).
        """
        return self.subtotal() > threshold
