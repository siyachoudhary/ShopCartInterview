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
 * There are 6 planted bugs: 4 easy to spot from a single failing test, and 2 subtler ones
 * that only bite on an edge case. Each assertion carries a message describing the intended
 * behavior.
 */
class CartTest {

    // -----------------------------------------------------------------------
    // The 4 easier bugs
    // -----------------------------------------------------------------------

    @Test
    void unitCountSumsQuantities() {
        // unitCount should count individual UNITS, not distinct products: 2 + 3 = 5.
        Cart c = new Cart();
        c.addItem("apple", 1.00, 2);
        c.addItem("banana", 0.50, 3);
        assertEquals(5, c.unitCount(),
                "unitCount() should sum every line's quantity (2 + 3 = 5), not count distinct products");
    }

    @Test
    void subtotalMultipliesPriceByQuantity() {
        // Each line contributes unitPrice * quantity.
        Cart c = new Cart();
        c.addItem("apple", 2.00, 2);   // 4.00
        c.addItem("banana", 1.50, 2);  // 3.00
        assertEquals(7.00, c.subtotal(), 1e-9,
                "subtotal() should add unitPrice * quantity per line (4.00 + 3.00 = 7.00), not just prices");
    }

    @Test
    void mostExpensiveReturnsHighestPriced() {
        Cart c = new Cart();
        c.addItem("gum", 1.00);
        c.addItem("steak", 9.00);
        c.addItem("bread", 3.00);
        assertEquals("steak", c.mostExpensive().getName(),
                "mostExpensive() should return the priciest line ('steak' at 9.00), not the cheapest");
    }

    @Test
    void totalAppliesDiscountAsMoneyOff() {
        // A discount rate of 0.2 = "20% off"; pay 80% of a 10.00 subtotal.
        Cart c = new Cart();
        c.addItem("book", 10.00);  // quantity 1 -> subtotal 10.00
        assertEquals(8.00, c.total(0.2), 1e-9,
                "total(0.2) should charge 80% of subtotal (10.00 * (1 - 0.2) = 8.00); 0.2 is taken OFF");
    }

    // -----------------------------------------------------------------------
    // The 2 harder bugs (edge cases)
    // -----------------------------------------------------------------------

    @Test
    void addingSameProductMergesIntoOneLine() {
        // Adding the same product twice should update the existing line, not add a second
        // line. The subtotal can look right either way, so check the line itself.
        Cart c = new Cart();
        c.addItem("apple", 1.00, 2);
        c.addItem("apple", 1.00, 3);
        assertEquals(1, c.getItems().size(),
                "adding 'apple' twice should leave ONE line, but a duplicate line was created");
        assertEquals(5, c.getItem("apple").getQuantity(),
                "the merged 'apple' line should carry the combined quantity (2 + 3 = 5)");
    }

    @Test
    void freeShippingIsInclusiveAtThreshold() {
        // Free shipping kicks in once the subtotal REACHES the threshold; exactly equal
        // must qualify.
        Cart c = new Cart();
        c.addItem("widget", 50.00);  // quantity 1 -> subtotal exactly 50.00
        assertTrue(c.freeShipping(50.00),
                "freeShipping should be inclusive: a subtotal of exactly 50.00 meets a 50.00 threshold");
        assertFalse(c.freeShipping(60.00),
                "a 50.00 subtotal should NOT qualify for a 60.00 threshold");
    }

    // -----------------------------------------------------------------------
    // Correct behavior (kept as clean reference points)
    // -----------------------------------------------------------------------

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
