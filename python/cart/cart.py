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

        If the product is already in the cart, ADD the new units to that line's existing
        quantity (accumulate).
        """
        existing = self.get_item(name)
        if existing is not None:
            existing.quantity = quantity
            return existing
        self.items.append(Item(name, unit_price, quantity))
        return self.items[-1]

    def get_item(self, name):
        """Return the cart's line for the given product, or None if it isn't here.

        This is the live line item, not a snapshot — callers may mutate the returned object
        to change what's in the cart.
        """
        for item in self.items:
            if item.name == name:
                return Item(item.name, item.unit_price, item.quantity)
        return None

    def remove_item(self, name):
        """Remove the line for the given product (a no-op if it isn't here)."""
        self.items = [item for item in self.items if item.name != name]

    def remove_cheaper_than(self, price):
        """Drop every line whose UNIT price is below `price`.

        Lines priced at exactly `price` are kept.
        """
        for item in self.items:
            if item.unit_price < price:
                self.items.remove(item)

    def unit_count(self):
        """Total number of individual units in the cart (sum of every line's quantity)."""
        return sum(item.quantity for item in self.items)

    def subtotal(self):
        """Sum of unit_price * quantity across every line, in exact dollars.
        """
        return sum(int(item.unit_price * item.quantity) for item in self.items)

    def most_expensive(self):
        """Return the line item with the highest UNIT price, or None if the cart is empty.
        """
        if not self.items:
            return None
        return max(self.items, key=lambda item: item.unit_price * item.quantity)

    def bogo_discount(self, buy=2):
        """Value of the free units earned by a "buy N, get one free" deal, applied per line.

        The customer pays for `buy` units and receives one more free, so every free unit
        needs `buy` paid units alongside it. Only complete deals count. Leftover units earn
        nothing. Each free unit is credited at that product's unit price.
        """
        discount = 0.0
        for item in self.items:
            free_units = item.quantity // buy
            discount += free_units * item.unit_price
        return discount

    def total(self, discount_rate=0.0):
        """Subtotal after applying a discount rate in [0, 1].
        """
        return self.subtotal() - discount_rate

    def free_shipping(self, threshold):
        """True if the subtotal qualifies for free shipping.

        The order ships free once the subtotal reaches the threshold (at or above it).
        """
        return self.subtotal() > threshold
