"""Behavioral tests for ShopCart.

These describe the *intended* behavior. Fix the source in cart/cart.py until they all
pass — do not change the tests.

There are 6 planted bugs. None of them announce themselves with a crash or an obviously
absurd value — every one is a plausible-looking implementation that quietly does the wrong
thing. Read the method's docstring (it states the intended behavior), then read the code.
Most bugs are a mismatch between those two, but don't assume it every time: a failing test
does not always point at the method it is named for, and one root cause can redden more than
one test. The tests come in two waves:

  * Wave 1 — a careful read of the docstring is enough to spot the problem.
  * Wave 2 — the bug only bites on a particular input or edge case.

Each assertion carries a message describing the intended behavior.
"""

import pytest

from cart import Cart


# ---------------------------------------------------------------------------
# Wave 1 — read the docstring carefully
# ---------------------------------------------------------------------------

def test_most_expensive_compares_unit_price_not_line_total():
    # most_expensive returns the line with the highest UNIT price. A cheap item bought in
    # bulk must NOT outrank a single expensive one: gum is $1 each (x10 = $10 of gum) but
    # steak is $9 each, so steak is the most expensive *item*.
    c = Cart()
    c.add_item("gum", 1.00, quantity=10)
    c.add_item("steak", 9.00, quantity=1)
    c.add_item("bread", 3.00, quantity=1)
    assert c.most_expensive().name == "steak", (
        "most_expensive() should compare unit prices (steak at 9.00 each wins), not line "
        "totals (10 units of gum is a bigger line total but gum is still the cheaper item)"
    )


def test_total_applies_discount_as_a_rate():
    # A discount rate of 0.2 = "20% off", so the customer pays 80% of a 10.00 subtotal.
    # The rate is a FRACTION of the subtotal, not a flat dollar amount subtracted.
    c = Cart()
    c.add_item("book", 10.00)  # quantity 1 -> subtotal is 10.00
    assert c.total(0.2) == 8.00, (
        "total(0.2) should charge 80% of the subtotal (10.00 * (1 - 0.2) = 8.00); 0.2 is a "
        "rate, so it is NOT 10.00 - 0.2 = 9.80"
    )


# ---------------------------------------------------------------------------
# Wave 2 — edge cases: fractional money, repeats, boundaries
# ---------------------------------------------------------------------------

def test_subtotal_keeps_fractional_cents():
    # subtotal sums unit_price * quantity in EXACT dollars. Fractional cents must survive:
    # 3 @ 2.50 is exactly 7.50, plus 1 @ 1.00 is 8.50. A subtotal that drops the fraction
    # (e.g. truncating each line to whole dollars) would report 8.00.
    c = Cart()
    c.add_item("pear", 2.50, quantity=3)   # 7.50
    c.add_item("roll", 1.00, quantity=1)   # 1.00
    assert c.subtotal() == 8.50, (
        "subtotal() should keep fractional dollars (7.50 + 1.00 = 8.50); it must not round "
        "or truncate line totals to whole dollars (which would give 8.00)"
    )


def test_adding_same_product_accumulates_quantity():
    # Adding the same product twice should ADD to the existing line's quantity, not create a
    # second line and not overwrite the quantity with the latest value. (A merge that
    # *replaces* the quantity still leaves one line, so check the quantity itself.)
    c = Cart()
    c.add_item("apple", 1.00, quantity=2)
    c.add_item("apple", 1.00, quantity=3)
    assert len(c.items) == 1, (
        "adding 'apple' twice should leave ONE line for it, not a duplicate "
        f"(found {len(c.items)} lines)"
    )
    assert c.get_item("apple").quantity == 5, (
        "the merged 'apple' line should carry the COMBINED quantity (2 + 3 = 5); overwriting "
        "it with the latest quantity (3) loses the earlier units"
    )


def test_remove_cheaper_than_drops_every_cheap_line():
    # Every line priced under the cutoff should go, however many there are. NOTE: the order
    # these are added in is load-bearing for this test — keep candy and gum adjacent.
    c = Cart()
    c.add_item("candy", 0.50)
    c.add_item("gum", 1.00)
    c.add_item("steak", 9.00)
    c.remove_cheaper_than(2.00)
    assert sorted(item.name for item in c.items) == ["steak"], (
        "remove_cheaper_than(2.00) should drop EVERY line under 2.00 (both candy and gum), "
        "leaving only steak"
    )


def test_subtotal_reflects_pruned_lines():
    # After pruning, the subtotal should reflect only the lines that survived. NOTE: the
    # order these are added in is load-bearing for this test — keep candy and gum adjacent.
    c = Cart()
    c.add_item("candy", 0.50)
    c.add_item("gum", 1.00)
    c.add_item("steak", 9.00)
    c.remove_cheaper_than(2.00)
    assert c.subtotal() == 9.00, (
        "after dropping every line under 2.00 only the 9.00 steak should remain, so the "
        "subtotal is 9.00"
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


def test_bogo_discount_credits_one_free_unit_per_deal():
    # "Buy 2, get one free": the customer pays for 2 and takes home a 3rd. Three units is
    # exactly one complete deal, so one unit is free.
    c = Cart()
    c.add_item("candy", 0.50, quantity=3)
    assert c.bogo_discount(2) == 0.50, (
        "3 units under a buy-2-get-one-free deal is one complete deal, so exactly one "
        "0.50 unit is free"
    )


def test_bogo_discount_needs_paid_units_for_every_free_one():
    # Each free unit has to be accompanied by `buy` PAID units, so a deal consumes 3 units
    # in total. 6 units of gum is two complete deals (2 free), not three.
    c = Cart()
    c.add_item("gum", 1.00, quantity=6)
    c.add_item("steak", 9.00, quantity=1)
    c.add_item("candy", 0.50, quantity=3)
    assert c.bogo_discount(2) == 2.50, (
        "6 gum is 2 free (not 3 — each free unit needs 2 paid ones beside it), 1 steak "
        "earns nothing, and 3 candy is 1 free: 2.00 + 0.00 + 0.50 = 2.50"
    )


# ---------------------------------------------------------------------------
# Correct behavior (these pass out of the box — clean reference points)
# ---------------------------------------------------------------------------

def test_unit_count_sums_quantities():
    # unit_count should count individual UNITS, not distinct products. Two products with
    # quantities 2 and 3 means 5 units in the cart, even though there are only 2 lines.
    c = Cart()
    c.add_item("apple", 1.00, quantity=2)
    c.add_item("banana", 0.50, quantity=3)
    assert c.unit_count() == 5, (
        "unit_count() should sum every line's quantity (2 + 3 = 5), not count the number "
        "of distinct products (which would be 2)"
    )


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
