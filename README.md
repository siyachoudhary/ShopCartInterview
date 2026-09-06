# ShopCart — Debugging Technical Interview

Welcome! This is a **timeboxed (~60 minute)** technical interview built around a small
shopping-cart library called **ShopCart**. There are two identical implementations in the
same repo — **Python** and **Java** — so pick whichever language you're most comfortable
in.

The interview is really **one main task with an optional bonus**:

1. **Debugging (the whole interview)** — The library ships with a failing test suite. Six
   bugs have been planted. Find and fix them until the tests are green. None of them are
   one-liners that scream at you — they're the kind of plausible-looking code that quietly
   does the wrong thing, so take your time and reason carefully.
2. **Add a Feature (extra credit)** — *Only if you finish the debugging comfortably early*
   (roughly, all tests green in under 30 minutes) we'll spend the remaining time adding a
   small feature together. This is a bonus, not a requirement — a thorough, well-narrated
   debugging pass is the main thing we're evaluating.

We're not looking for perfection. We want to see how you read unfamiliar code, form
hypotheses, verify them, and communicate as you go. **Think out loud.**

---

## What is ShopCart?

A tiny in-memory shopping cart. A cart holds "line items" — one line per distinct product,
each with a `unit_price` and a `quantity`. The `Cart` class lets you add items (merging
duplicates), look them up, remove them, prune the ones under a price cutoff, count units,
compute the subtotal, find the priciest item, apply a discount, and check free-shipping
eligibility.

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
> - Python: `python -m pytest tests/test_cart.py::test_subtotal_keeps_fractional_cents -v`
> - Java: `mvn -Dtest=CartTest#subtotalKeepsFractionalCents test`

---

## Part 1 — Debugging (the main task)

1. Run the test suite. You should see multiple failures.
2. Read the failing tests to understand the *intended* behavior (each assertion has a
   message describing it).
3. Open the source (`cart/cart.py` or `src/main/java/com/example/cart/Cart.java`) — each
   method's docstring/Javadoc states what it should do — and fix the bugs.
4. Re-run until everything is green.

There are **eight** planted bugs, and **none of them are loud** — there are no crashes or
wildly-wrong values to point the way. Each is a plausible implementation that quietly does
the wrong thing: think counting the wrong thing, comparing the wrong quantity, money that
loses its cents, or a "merge" that overwrites instead of accumulating. The **docstring on
each method states what it is supposed to do**, and most bugs are a mismatch between that
description and the code — but don't assume it every time. A failing test does not always
point at the method it is named for, and one root cause can redden more than one test.

The tests come in two waves: *Wave 1* is catchable from a careful read of the docstring;
*Wave 2* only bites on a particular input or edge case. Fix the source, **not** the tests.

**As you work, tell us:** what does the failing test expect, what did you observe, what's
your hypothesis, and how did the fix confirm it?

---

## Part 2 — Add a Feature (extra credit — only if you finish early)

**This part is a bonus.** We only reach it if you've finished the debugging comfortably
early — as a rough rule of thumb, all tests green in **under 30 minutes** with time to
spare. If debugging takes the whole session, that's completely fine; a careful, well-
narrated debugging pass is what we're really evaluating. Don't rush Part 1 to get here.

If we do have time: pick **one** feature below (or propose your own) and implement it,
**including at least one test**. Reach for whatever tools and references you'd normally use
(docs, Google, StackOverflow, AI assistants such as Copilot/ChatGPT/Claude, etc.).

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
