# Technical Order Module

## Overview

The Technical Order Module is a custom Odoo module developed for a wooden tools store. It introduces an approval workflow before creating Sales Orders, allowing customer requests to be reviewed and approved before the sales process begins.

---

## Business Flow

1. A customer requests products from the store.
2. The employee creates a **Technical Order**.
3. The Technical Order is submitted for approval.
4. The manager either:

   * Approves the order.
   * Rejects the order with a rejection reason.
5. Once approved:

   * An email notification is sent to all Sales Managers.
   * The **Create SO** button becomes available.
6. One or more Sales Orders can be created from the same Technical Order.
7. The system validates that confirmed Sales Orders never exceed the requested quantities.
8. When all requested quantities have been fulfilled, the **Create SO** button is automatically hidden.

---

## Features

### Technical Order

* Automatic sequence generation (TO0001, TO0002, ...)
* Request Name
* Requested By (Current User)
* Customer selection (only customers with **is_tech_offer = True**)
* Start Date (Today's date by default)
* End Date
* Rejection Reason
* Order Lines
* Total Amount
* Status Bar

---

### Technical Order Lines

Each line contains:

* Product
* Description (Automatically filled from Product)
* Quantity
* Price (Product List Price)
* Total (Quantity × Price)

---

## Workflow

```
Draft
   │
   ▼
Submit For Approval
   │
   ▼
To Be Approved
   │
 ┌─┴─────────┐
 │           │
 ▼           ▼
Reject    Approve
 │           │
 ▼           ▼
Rejected  Approved
               │
               ▼
        Create Sale Order
```

---

## Approval Process

### Submit for Approval

Changes the state from:

```
Draft
    ↓
To Be Approved
```

---

### Approve

* Changes state to **Approved**
* Sends an email notification to all users in the Sales Manager group
* Enables the **Create SO** button

---

### Reject

Opens a Wizard where the manager enters:

* Rejection Reason

After confirmation:

* State changes to **Rejected**
* Rejection reason is stored in the Technical Order

---

## Sale Order Integration

After approval, users can create Sales Orders directly from the Technical Order.

The created Sale Order contains:

* Customer
* Products
* Remaining quantities
* Product prices

---

## Quantity Validation

Users may edit quantities inside the Sale Order before confirmation.

However, the system validates that:

```
Confirmed Quantity
        ≤
Requested Quantity
```

If the quantity exceeds the requested amount, a validation error is raised.

---

## Multiple Sale Orders

A single Technical Order can generate multiple Sales Orders.

Example:

### Technical Order

| Product   | Requested Qty |
| --------- | ------------: |
| Product A |             5 |
| Product B |             3 |

### Sale Order 1 (Confirmed)

| Product   | Qty |
| --------- | --: |
| Product A |   2 |
| Product B |   3 |

Remaining quantities:

| Product   | Remaining |
| --------- | --------: |
| Product A |         3 |
| Product B |         0 |

### Sale Order 2

Only the remaining quantity is created automatically.

| Product   | Qty |
| --------- | --: |
| Product A |   3 |

Product B is not added because its remaining quantity is zero.

---

## Remaining Quantity Logic

The module always calculates:

```
Remaining Quantity

=

Requested Quantity

-

Confirmed Sale Order Quantity
```

Only confirmed Sales Orders are considered.

Draft quotations do not affect the remaining quantity.

---

## Smart Button

A Smart Button displays:

* Number of related Sales Orders
* Opens a list of all Sales Orders linked to the Technical Order

---

## Automatic Hide of Create SO Button

The **Create SO** button is automatically hidden when:

```
Remaining Quantity = 0

for every product
```

This prevents creating unnecessary Sales Orders.

---

## Email Notification

When a Technical Order is approved:

* An email is sent automatically to every user in the **Sales Manager** group.

Example:

```
Subject:
Technical Order Approved

Body:

Technical Order TO0005 has been approved.
```

---

## QWeb Report

A printable PDF report includes:

* Technical Order Information
* Customer Details
* Request Details
* Order Lines
* Quantities
* Prices
* Totals

---

## Technologies Used

* Odoo 18
* Python
* XML
* QWeb Reports
* Mail Templates
* Wizards
* ORM
* Computed Fields
* Smart Buttons
* Server Actions
* Sale Order Integration

---

## Project Highlights

* Complete approval workflow
* Email notifications
* Wizard implementation
* QWeb PDF report
* Smart Buttons
* Sale Order integration
* Quantity validation
* Multiple Sale Orders support
* Remaining quantity calculation
* Automatic button visibility
* Business-oriented workflow
