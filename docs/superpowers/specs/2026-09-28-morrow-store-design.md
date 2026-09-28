# MORROW Store Design Spec

## Product

MORROW is a curated lifestyle store for design-conscious buyers. It sells a small,
intentional collection of audio, lighting, desk, and travel objects. The experience
should feel closer to a design journal or concept store than a marketplace.

## Goals

- Present a complete browsing-to-checkout shopping flow without a backend.
- Make the storefront visually distinctive, premium, and responsive.
- Keep the payment step deliberately non-transactional and clearly labeled.
- Persist cart and order state in the browser so the experience survives reloads.

## In Scope

- Product catalog with category filters, sorting, and text search.
- Product detail view with color selection, quantity control, and product facts.
- Cart drawer with quantity changes, removal, discount code, and totals.
- Checkout form with contact, shipping address, delivery method, and validation.
- Simulated payment method selection for card, Alipay, and WeChat Pay.
- Order confirmation state and locally persisted order history.
- Empty, loading, success, and error states.
- Keyboard support, visible focus states, reduced-motion behavior, and responsive
  layouts from 360px through desktop.

## Out of Scope

- Real payments, authentication, inventory reservation, shipping integrations, admin
  tools, server storage, analytics, and third-party tracking.

## Information Architecture

The storefront is a single-page application with four views:

1. Store: editorial hero, collection statement, category controls, product grid.
2. Product: image-led detail view with purchase controls.
3. Checkout: contact and delivery form, order summary, payment entry.
4. Confirmation: order number, payment status, delivery estimate, order summary.

The cart is a non-modal drawer available from every storefront view.

## Data Model

Each product contains:

- `id`, `name`, `series`, `category`, `price`, `compareAt`
- `description`, `materials`, `delivery`
- `colors`: `{ name, value }[]`
- `image`, `gallery`, `featured`, `stock`

Each cart item contains `productId`, `color`, and `quantity`.

Checkout state contains `name`, `email`, `phone`, `province`, `city`, `address`,
`postalCode`, `deliveryMethod`, and `paymentMethod`.

## Visual System

- Canvas: cool paper `#F4F7FB`
- Surface: mist `#E8EDF3`
- Ink: graphite `#0C1015`
- Secondary text: slate `#697386`
- Accent: cobalt `#1E4FFF`
- Success: forest `#126B4A`
- Error: brick `#B42318`

Typography uses a compact grotesk display stack and a readable system body stack.
Headlines use tight tracking and narrow width. The main visual signature is an
editorial product stage with oversized type, strong crops, and cobalt interaction
markers. Corners stay at 4px or less. Shadows are soft and blue-tinted.

## Interaction Rules

- Product images are local files and render without network access.
- Adding to cart opens the cart drawer and announces the change to assistive tech.
- Mobile navigation uses a full-width menu sheet, not a compressed desktop nav.
- Checkout errors stay inline next to the relevant field.
- The payment button never claims to charge a card. It says the order runs in demo
  mode and confirms this again on the confirmation view.

## Acceptance Criteria

- The page opens successfully from `index.html`.
- All product cards open the correct product detail.
- Search and category filters update the product grid immediately.
- Cart quantities and totals update correctly.
- Refreshing preserves the cart and completed order history.
- The checkout form blocks missing or malformed required fields.
- No real network or payment request occurs during checkout.
- The layout remains usable at 360px, 768px, 1024px, and 1440px widths.
- `prefers-reduced-motion: reduce` disables non-essential motion.

