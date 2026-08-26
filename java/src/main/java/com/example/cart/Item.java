package com.example.cart;

/** A single line in the cart: a product with a unit price and a quantity. */
public class Item {
    private final String name;
    private final double unitPrice;
    private int quantity;

    public Item(String name, double unitPrice, int quantity) {
        this.name = name;
        this.unitPrice = unitPrice;
        this.quantity = quantity;
    }

    public String getName() {
        return name;
    }

    public double getUnitPrice() {
        return unitPrice;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    @Override
    public String toString() {
        return String.format("Item(%s x%d @ %.2f)", name, quantity, unitPrice);
    }
}
