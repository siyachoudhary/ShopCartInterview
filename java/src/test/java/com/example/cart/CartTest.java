package com.example.cart;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/**
 * Behavioral tests for ShopCart. These describe the *intended* behavior.
 * Fix the source in Cart.java until they all pass — do not change the tests.
 *
 * There are 6 planted bugs. None of them announce themselves with a crash or an obviously
 * absurd value — every one is a plausible-looking implementation that quietly does the wrong
 * thing. Read the method's Javadoc (it states the intended behavior), then read the code.
 * Most bugs are a mismatch between those two, but don't assume it every time: a failing test
 * does not always point at the method it is named for, and one root cause can redden more
 * than one test. The tests come in two waves:
 *
 *   - Wave 1: a careful read of the Javadoc is enough to spot the problem.
 *   - Wave 2: the bug only bites on a particular input or edge case.
 *
 * Each assertion carries a message describing the intended behavior.
 */
class CartTest {

    // -----------------------------------------------------------------------
    // Wave 1 — read the Javadoc carefully
    // -----------------------------------------------------------------------

    @Test
    void mostExpensiveComparesUnitPriceNotLineTotal() {
        // most_expensive returns the line with the highest UNIT price. A cheap item bought
        // in bulk must NOT outrank a single expensive one: gum is $1 each (x10) but steak is
        // $9 each, so steak is the most expensive item.
        Cart c = new Cart();
        c.addItem("gum", 1.00, 10);
        c.addItem("steak", 9.00, 1);
        c.addItem("bread", 3.00, 1);
        assertEquals("steak", c.mostExpensive().getName(),
                "mostExpensive() should compare unit prices (steak at 9.00 each), not line totals "
                        + "(10 units of gum is a bigger line total but gum is still the cheaper item)");
    }

    @Test
    void totalAppliesDiscountAsARate() {
        // A discount rate of 0.2 = "20% off"; pay 80% of a 10.00 subtotal. The rate is a
        // FRACTION of the subtotal, not a flat dollar amount subtracted.
        Cart c = new Cart();
        c.addItem("book", 10.00);  // quantity 1 -> subtotal 10.00
        assertEquals(8.00, c.total(0.2), 1e-9,
                "total(0.2) should charge 80% of subtotal (10.00 * (1 - 0.2) = 8.00); 0.2 is a rate, "
                        + "so it is NOT 10.00 - 0.2 = 9.80");
    }

    // -----------------------------------------------------------------------
    // Wave 2 — edge cases: fractional money, repeats, boundaries
    // -----------------------------------------------------------------------

    @Test
    void subtotalKeepsFractionalCents() {
        // subtotal sums unitPrice * quantity in EXACT dollars. Fractional cents must survive:
        // 3 @ 2.50 is exactly 7.50, plus 1 @ 1.00 is 8.50. Truncating each line to whole
        // dollars would report 8.00.
        Cart c = new Cart();
        c.addItem("pear", 2.50, 3);   // 7.50
        c.addItem("roll", 1.00, 1);   // 1.00
        assertEquals(8.50, c.subtotal(), 1e-9,
                "subtotal() should keep fractional dollars (7.50 + 1.00 = 8.50); it must not round or "
                        + "truncate line totals to whole dollars (which would give 8.00)");
    }

    @Test
    void addingSameProductAccumulatesQuantity() {
        // Adding the same product twice should ADD to the existing line's quantity, not add a
        // second line and not overwrite the quantity with the latest value. A merge that
        // *replaces* the quantity still leaves one line, so check the quantity itself.
        Cart c = new Cart();
        c.addItem("apple", 1.00, 2);
        c.addItem("apple", 1.00, 3);
        assertEquals(1, c.getItems().size(),
                "adding 'apple' twice should leave ONE line, not a duplicate");
        assertEquals(5, c.getItem("apple").getQuantity(),
                "the merged 'apple' line should carry the COMBINED quantity (2 + 3 = 5); overwriting "
                        + "it with the latest quantity (3) loses the earlier units");
    }

    @Test
    void removeCheaperThanDropsEveryCheapLine() {
        // Every line priced under the cutoff should go, however many there are. NOTE: the
        // order these are added in is load-bearing — keep candy and gum adjacent.
        Cart c = new Cart();
        c.addItem("candy", 0.50);
        c.addItem("gum", 1.00);
        c.addItem("steak", 9.00);
        c.removeCheaperThan(2.00);
        assertEquals(1, c.getItems().size(),
                "removeCheaperThan(2.00) should drop EVERY line under 2.00 (both candy and gum), "
                        + "leaving only steak");
        assertEquals("steak", c.getItems().get(0).getName(), "the surviving line should be 'steak'");
    }

    @Test
    void subtotalReflectsPrunedLines() {
        // After pruning, the subtotal should reflect only the lines that survived. NOTE: the
        // order these are added in is load-bearing — keep candy and gum adjacent.
        Cart c = new Cart();
        c.addItem("candy", 0.50);
        c.addItem("gum", 1.00);
        c.addItem("steak", 9.00);
        c.removeCheaperThan(2.00);
        assertEquals(9.00, c.subtotal(), 1e-9,
                "after dropping every line under 2.00 only the 9.00 steak should remain, so the "
                        + "subtotal is 9.00");
    }

    @Test
    void freeShippingIsInclusiveAtThreshold() {
        // Free shipping kicks in once the subtotal REACHES the threshold; exactly equal must
        // qualify.
        Cart c = new Cart();
        c.addItem("widget", 50.00);  // quantity 1 -> subtotal exactly 50.00
        assertTrue(c.freeShipping(50.00),
                "freeShipping should be inclusive: a subtotal of exactly 50.00 meets a 50.00 threshold");
        assertFalse(c.freeShipping(60.00),
                "a 50.00 subtotal should NOT qualify for a 60.00 threshold");
    }

    @Test
    void bogoDiscountCreditsOneFreeUnitPerDeal() {
        // "Buy 2, get one free": the customer pays for 2 and takes home a 3rd. Three units
        // is exactly one complete deal, so one unit is free.
        Cart c = new Cart();
        c.addItem("candy", 0.50, 3);
        assertEquals(0.50, c.bogoDiscount(2), 1e-9,
                "3 units under a buy-2-get-one-free deal is one complete deal, so exactly one "
                        + "0.50 unit is free");
    }

    @Test
    void bogoDiscountNeedsPaidUnitsForEveryFreeOne() {
        // Each free unit has to be accompanied by `buy` PAID units, so a deal consumes 3
        // units in total. 6 units of gum is two complete deals (2 free), not three.
        Cart c = new Cart();
        c.addItem("gum", 1.00, 6);
        c.addItem("steak", 9.00, 1);
        c.addItem("candy", 0.50, 3);
        assertEquals(2.50, c.bogoDiscount(2), 1e-9,
                "6 gum is 2 free (not 3 — each free unit needs 2 paid ones beside it), 1 steak "
                        + "earns nothing, and 3 candy is 1 free: 2.00 + 0.00 + 0.50 = 2.50");
    }

    // -----------------------------------------------------------------------
    // Correct behavior (these pass out of the box — clean reference points)
    // -----------------------------------------------------------------------

    @Test
    void unitCountSumsQuantities() {
        // unitCount should count individual UNITS, not distinct products: 2 + 3 = 5, even
        // though there are only 2 lines.
        Cart c = new Cart();
        c.addItem("apple", 1.00, 2);
        c.addItem("banana", 0.50, 3);
        assertEquals(5, c.unitCount(),
                "unitCount() should sum every line's quantity (2 + 3 = 5), not count distinct products (2)");
    }

    @Test
    void addAndGetItem() {
        Cart c = new Cart();
        c.addItem("apple", 1.25);
        c.addItem("banana", 0.75);
        assertEquals(1.25, c.getItem("apple").getUnitPrice(), 1e-9,
                "getItem should return the stored line for a product");
        assertNull(c.getItem("cherry"), "getItem should return null for a product not in the cart");
    }

    @Test
    void removeItem() {
        Cart c = new Cart();
        c.addItem("apple", 1.00);
        c.addItem("banana", 0.50);
        c.removeItem("apple");
        assertEquals(1, c.getItems().size(), "remove_item should drop only the named product's line");
        assertEquals("banana", c.getItems().get(0).getName(), "the remaining line should be 'banana'");
    }
}
