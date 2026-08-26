# ShopCart — Debugging Technical Interview

Welcome! This is a **timeboxed (~60 minute)** technical interview built around a small
shopping-cart library called **ShopCart**. There are two identical implementations in the
same repo — **Python** and **Java** — so pick whichever language you're most comfortable
in.

The interview has two parts:

1. **Debugging (~35 min)** — The library ships with a failing test suite. Six bugs have
   been planted (four easy, two subtle). Find and fix them until the tests are green.
2. **Feature (~20 min)** — Once tests pass, add a new feature. This part is open-ended:
   use any external resources you like (docs, Google, StackOverflow, AI assistants such
   as Copilot/ChatGPT/Claude, etc.). We care about how you approach the problem.

We're not looking for perfection. We want to see how you read unfamiliar code, form
hypotheses, verify them, and communicate as you go. **Think out loud.**

---

## What is ShopCart?

A tiny in-memory shopping cart. A cart holds "line items" — one line per distinct product,
each with a `unit_price` and a `quantity`. The `Cart` class lets you add items (merging
duplicates), look them up, remove them, count units, compute the subtotal, find the
priciest item, apply a discount, and check free-shipping eligibility.

The two implementations behave identically — same classes, same methods, same bugs.

---

## Setup

### Prerequisites

| Language | Needs |
|----------|-------|
| Python   | Python 3.9+ and `pytest` (`pip install pytest`) |
| Java     | JDK 17+ and Maven 3.8+ |

### Python

```bash
cd python
python -m pip install pytest        # once
python -m pytest -v                 # run the tests
```

### Java

```bash
cd java
mvn test                            # compiles and runs the tests
```

> Tip: run a single test while iterating.
> - Python: `python -m pytest tests/test_cart.py::test_subtotal_multiplies_price_by_quantity -v`
> - Java: `mvn -Dtest=CartTest#subtotalMultipliesPriceByQuantity test`

---

## Part 1 — Debugging (~35 min)

1. Run the test suite. You should see multiple failures.
2. Read the failing tests to understand the *intended* behavior (each assertion has a
   message describing it).
3. Open the source (`cart/cart.py` or `src/main/java/com/example/cart/Cart.java`) — each
   method's docstring/Javadoc states what it should do — and fix the bugs.
4. Re-run until everything is green.

There are **six** planted bugs: **four are easy to spot** from a single failing test, and
**two are subtler** — they only surface on an edge case, so the failing test won't point
straight at the buggy line. Fix the source, **not** the tests.

**As you work, tell us:** what does the failing test expect, what did you observe, what's
your hypothesis, and how did the fix confirm it?

---

## Part 2 — Add a Feature (~20 min)

Once the suite is green, pick **one** feature below (or propose your own) and implement it,
**including at least one test**.

- **Coupon codes.** Add `apply_coupon(code)` that maps known codes (e.g. `"SAVE10"`) to a
  discount rate and applies it in `total()`; unknown codes do nothing.
- **Quantity cap / update.** Add `set_quantity(name, qty)` that sets a line's quantity
  exactly (removing the line if `qty` is 0).
- **Tax.** Add `total_with_tax(discount_rate, tax_rate)` applying discount then tax.
- **Cheapest / sorting.** Add `sorted_by_price()` returning lines cheapest-first.

Walk us through your design choices, edge cases, and how you'd extend it further.

---

## What we're evaluating

- **Debugging method** — reading code, isolating faults, verifying fixes.
- **Communication** — narrating your reasoning and trade-offs.
- **Code quality** — clean, readable changes that match the surrounding style.
- **Feature judgment** — sensible design, edge-case awareness, and a test that proves it.

Good luck — and remember to think out loud!
