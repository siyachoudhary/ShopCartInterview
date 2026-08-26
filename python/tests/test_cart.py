"""Behavioral tests for ShopCart.

These describe the *intended* behavior. Fix the source in cart/cart.py until they all
pass — do not change the tests.

There are 6 planted bugs: 4 are easy to spot from a single failing test, and 2 are
subtler (they only bite on an edge case). Each assertion carries a message describing the
intended behavior, so a failure tells you what the method should do — not just how two
values differ.
"""

import pytest

from cart import Cart


# ---------------------------------------------------------------------------
# The 4 easier bugs
# ---------------------------------------------------------------------------

def test_unit_count_sums_quantities():
    # unit_count should count individual UNITS, not distinct products. Two products with
    # quantities 2 and 3 means 5 units in the cart.
    c = Cart()
    c.add_item("apple", 1.00, quantity=2)
    c.add_item("banana", 0.50, quantity=3)
    assert c.unit_count() == 5, (
        "unit_count() should sum every line's quantity (2 + 3 = 5), not count the number "
        "of distinct products"
    )


def test_subtotal_multiplies_price_by_quantity():
    # Each line contributes unit_price * quantity to the subtotal.
    c = Cart()
    c.add_item("apple", 2.00, quantity=2)   # 4.00
    c.add_item("banana", 1.50, quantity=2)  # 3.00
    assert c.subtotal() == 7.00, (
        "subtotal() should add up unit_price * quantity for every line (4.00 + 3.00 = "
        "7.00), not just the unit prices"
    )


def test_most_expensive_returns_highest_priced():
    # most_expensive returns the line with the HIGHEST unit price.
    c = Cart()
    c.add_item("gum", 1.00)
    c.add_item("steak", 9.00)
    c.add_item("bread", 3.00)
    assert c.most_expensive().name == "steak", (
        "most_expensive() should return the priciest line ('steak' at 9.00), not the "
        "cheapest"
    )


def test_total_applies_discount_as_money_off():
    # A discount rate of 0.2 = "20% off", so the customer pays 80% of a 10.00 subtotal.
    c = Cart()
    c.add_item("book", 10.00)  # quantity 1 -> subtotal is 10.00
    assert c.total(0.2) == 8.00, (
        "total(0.2) should charge 80% of the subtotal (10.00 * (1 - 0.2) = 8.00); a rate "
        "of 0.2 is the amount taken OFF, not the amount paid"
    )


# ---------------------------------------------------------------------------
# The 2 harder bugs (edge cases)
# ---------------------------------------------------------------------------

def test_adding_same_product_merges_into_one_line():
    # Adding the same product twice should update the existing line's quantity, not create
    # a second line for it. (The subtotal can look correct either way, so check the line
    # itself.)
    c = Cart()
    c.add_item("apple", 1.00, quantity=2)
    c.add_item("apple", 1.00, quantity=3)
    assert len(c.items) == 1, (
        "adding 'apple' twice should leave ONE line for it, but a duplicate line was "
        f"created (found {len(c.items)} lines)"
    )
    assert c.get_item("apple").quantity == 5, (
        "the merged 'apple' line should carry the combined quantity (2 + 3 = 5)"
    )


def test_free_shipping_is_inclusive_at_the_threshold():
    # Free shipping kicks in once the subtotal REACHES the threshold. A subtotal exactly
    # equal to the threshold must qualify.
    c = Cart()
    c.add_item("widget", 50.00)  # quantity 1 -> subtotal is exactly 50.00
    assert c.free_shipping(50.00) is True, (
        "free_shipping should be inclusive: a subtotal of exactly 50.00 meets a 50.00 "
        "threshold and should qualify"
    )
    assert c.free_shipping(60.00) is False, "a 50.00 subtotal should NOT qualify for a 60.00 threshold"


# ---------------------------------------------------------------------------
# Correct behavior (kept as clean reference points)
# ---------------------------------------------------------------------------

def test_add_and_get_item():
    c = Cart()
    c.add_item("apple", 1.25)
    c.add_item("banana", 0.75)
    assert c.get_item("apple").unit_price == 1.25, "get_item should return the stored line for a product"
    assert c.get_item("cherry") is None, "get_item should return None for a product that isn't in the cart"


def test_remove_item():
    c = Cart()
    c.add_item("apple", 1.00)
    c.add_item("banana", 0.50)
    c.remove_item("apple")
    remaining = sorted(item.name for item in c.items)
    assert remaining == ["banana"], "remove_item should drop only the named product's line"
