# MORROW Store Implementation Plan

> **For agentic workers:** Execute this plan in order. Each task must leave the
> storefront openable and testable.

**Goal:** Build a polished, backend-free e-commerce storefront with a complete
browsing, cart, checkout, and simulated-payment flow.

**Architecture:** A static single-page application using semantic HTML, CSS custom
properties, and vanilla JavaScript. Catalog, cart, checkout, and confirmation views
share one application state object persisted to `localStorage`.

**Tech Stack:** HTML5, CSS3, vanilla ES modules, Lucide icon library, local product
photography.

## Global Constraints

- No real payment request, backend, authentication, or external runtime API.
- All data attributes are lowercase kebab-case.
- Product IDs remain stable strings.
- The design uses one accent color: cobalt `#1E4FFF`.
- Interactive controls have visible focus states and minimum 44px hit targets.
- Motion must respect `prefers-reduced-motion`.
- No visible text may describe implementation details or keyboard shortcuts.

## Task 1: Foundation And Local Assets

**Files:**
- Create: `index.html`
- Create: `styles.css`
- Create: `assets/vendor/lucide.min.js`
- Create: `assets/products/*.jpg`
- Create: `README.md`

**Interfaces:**
- Produces: a document with `#app`, `#catalog-grid`, `#cart-drawer`, and
  `#toast-region`.
- Produces: local product image paths consumed by Task 2.

- [ ] Download and verify eight local product images.
- [ ] Add the Lucide browser bundle or a local-compatible equivalent.
- [ ] Build the semantic page shell and navigation.
- [ ] Define visual tokens, typography, grid, focus states, and reduced motion.
- [ ] Open `index.html` and verify the shell renders without console errors.

## Task 2: Catalog And Product Data

**Files:**
- Create: `app.js`
- Modify: `index.html`
- Modify: `styles.css`

**Interfaces:**
- Produces: `products: Product[]`
- Produces: `renderCatalog(filterState): void`
- Produces: `openProduct(productId: string): void`

- [ ] Define eight products with prices, descriptions, materials, delivery notes,
  colors, stock, and image paths.
- [ ] Render featured product cards from the data.
- [ ] Implement search, category filtering, and sorting.
- [ ] Add empty search results with a clear reset action.
- [ ] Verify every product card opens the matching detail view.

## Task 3: Cart And Persistence

**Files:**
- Modify: `app.js`
- Modify: `styles.css`

**Interfaces:**
- Produces: `cart: CartItem[]`
- Produces: `addToCart(productId: string, color: string, quantity: number): void`
- Produces: `setCartQuantity(index: number, quantity: number): void`
- Produces: `cartTotal(): { subtotal: number, shipping: number, discount: number, total: number }`

- [ ] Add product color and quantity controls.
- [ ] Build the cart drawer with item rows and quantity steppers.
- [ ] Add discount code `MORROW10`.
- [ ] Persist cart state to `localStorage`.
- [ ] Verify totals, removal, empty state, and reload persistence.

## Task 4: Checkout And Payment Entry

**Files:**
- Modify: `index.html`
- Modify: `app.js`
- Modify: `styles.css`

**Interfaces:**
- Produces: `openCheckout(): void`
- Produces: `validateCheckout(form: HTMLFormElement): CheckoutState | null`
- Produces: `completeOrder(checkout: CheckoutState): void`

- [ ] Build contact, address, delivery, and payment sections.
- [ ] Validate required fields and email format inline.
- [ ] Show a persistent demo-payment notice.
- [ ] Prevent checkout when the cart is empty.
- [ ] Verify no network request is made when placing the order.

## Task 5: Confirmation And Polish

**Files:**
- Modify: `app.js`
- Modify: `styles.css`

**Interfaces:**
- Consumes: `CheckoutState`
- Produces: persisted order records with `orderNumber`, `createdAt`, `items`, and
  `total`.

- [ ] Render a confirmation view with order number and delivery estimate.
- [ ] Clear the cart after successful completion.
- [ ] Add responsive navigation and mobile layouts.
- [ ] Add skeleton loading, toast feedback, and error states.
- [ ] Run browser checks at desktop and mobile widths.
- [ ] Validate keyboard flow, console output, and reduced-motion behavior.

