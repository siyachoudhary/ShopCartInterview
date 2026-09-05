package com.example.cart;

import java.util.ArrayList;
import java.util.List;

/**
 * ShopCart — a tiny in-memory shopping cart.
 *
 * The Javadoc on each method describes what it is *supposed* to do. The behavioral tests
 * in CartTest check that intent. Some implementations don't match their description —
 * those are the bugs you're here to find.
 */
public class Cart {

    private final List<Item> items = new ArrayList<>();

    public List<Item> getItems() {
        return items;
    }

    /**
     * Add units of a product to the cart. If the product is already in the cart, ADD the
     * new units to that line's existing quantity (accumulate) instead of creating a second
     * line or replacing the quantity.
     */
    public Item addItem(String name, double unitPrice, int quantity) {
        Item existing = getItem(name);
        if (existing != null) {
            existing.setQuantity(quantity);
            return existing;
        }
        Item item = new Item(name, unitPrice, quantity);
        items.add(item);
        return item;
    }

    public Item addItem(String name, double unitPrice) {
        return addItem(name, unitPrice, 1);
    }

    /** Return the line item for the given product name, or null if it isn't here. */
    public Item getItem(String name) {
        for (Item item : items) {
            if (item.getName().equals(name)) {
                return item;
            }
        }
        return null;
    }

    /** Remove the line for the given product (a no-op if it isn't here). */
    public void removeItem(String name) {
        items.removeIf(item -> item.getName().equals(name));
    }

    /** Total number of individual units in the cart (sum of every line's quantity). */
    public int unitCount() {
        return items.size();
    }

    /**
     * Sum of unitPrice * quantity across every line, in exact dollars. Don't round or drop
     * fractional cents: a line of 3 @ 2.50 contributes exactly 7.50.
     */
    public double subtotal() {
        double sum = 0.0;
        for (Item item : items) {
            sum += (int) (item.getUnitPrice() * item.getQuantity());
        }
        return sum;
    }

    /**
     * Return the line item with the highest UNIT price, or null if the cart is empty. This
     * compares unit prices, not line totals: a cheap item bought in bulk does not outrank a
     * single expensive one.
     */
    public Item mostExpensive() {
        if (items.isEmpty()) {
            return null;
        }
        Item best = items.get(0);
        for (Item item : items) {
            if (item.getUnitPrice() * item.getQuantity() > best.getUnitPrice() * best.getQuantity()) {
                best = item;
            }
        }
        return best;
    }

    /**
     * Subtotal after applying a discount rate in [0, 1]. A rate of 0.2 means "20% off",
     * i.e. the customer pays 80% of the subtotal.
     */
    public double total(double discountRate) {
        return subtotal() - discountRate;
    }

    /**
     * True if the subtotal qualifies for free shipping. The order ships free once the
     * subtotal reaches the threshold (at or above it).
     */
    public boolean freeShipping(double threshold) {
        return subtotal() > threshold;
    }
}
