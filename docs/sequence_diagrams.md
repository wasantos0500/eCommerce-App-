# Store, Buyer, and Review Sequence Diagrams

These diagrams describe the eCommerce application's own interactions. They replace the unrelated external-post sequence previously used.

## Store CRUD sequence (vendor)

```mermaid
sequenceDiagram
    actor Vendor
    participant Browser
    participant StoreView as Store views
    participant Form as StoreForm
    participant DB as MariaDB

    alt Create store
        Vendor->>Browser: Submit new store details
        Browser->>StoreView: POST /stores/create/
        StoreView->>Form: Validate name and description
        Form-->>StoreView: Valid data
        StoreView->>DB: INSERT store with current vendor as owner
        DB-->>StoreView: Created store
        StoreView-->>Browser: Redirect to dashboard
    else Read store
        Vendor->>Browser: Open owned store
        Browser->>StoreView: GET /stores/{id}/
        StoreView->>DB: SELECT store WHERE id and owner match
        DB-->>StoreView: Store and products
        StoreView-->>Browser: Render store detail
    else Update store
        Vendor->>Browser: Submit edited store details
        Browser->>StoreView: POST /stores/{id}/edit/
        StoreView->>DB: SELECT store WHERE id and owner match
        StoreView->>Form: Validate changes
        StoreView->>DB: UPDATE store
        StoreView-->>Browser: Redirect to store detail
    else Delete store
        Vendor->>Browser: Confirm deletion
        Browser->>StoreView: POST /stores/{id}/delete/
        StoreView->>DB: SELECT store WHERE id and owner match
        StoreView->>DB: DELETE store
        StoreView-->>Browser: Redirect to dashboard
    end
```

## Buyer use-case sequence

```mermaid
sequenceDiagram
    actor Buyer
    participant Browser
    participant Auth as Authentication / buyer views
    participant Cart as Session cart
    participant DB as MariaDB

    Buyer->>Browser: Register as Buyer
    Browser->>Auth: POST /register/
    Auth->>DB: CREATE user and add Buyer group
    DB-->>Auth: Buyer account created
    Auth-->>Browser: Sign in and redirect home
    Buyer->>Browser: Browse stores and products
    Browser->>Auth: GET /stores/ or /browse/
    Auth->>DB: READ available stores/products
    DB-->>Auth: Store/product data
    Auth-->>Browser: Render catalogue
    Buyer->>Browser: Add or change cart item
    Browser->>Auth: Request add/increase/decrease/remove
    Auth->>Cart: CREATE/UPDATE/DELETE session cart entry
    Cart-->>Browser: Updated cart
    Buyer->>Browser: Confirm checkout
    Browser->>Auth: POST /checkout/
    Auth->>DB: CREATE order and order items; UPDATE stock
    DB-->>Auth: Order committed
    Auth->>Cart: CLEAR cart
    Auth-->>Browser: Render order confirmation
```

## Review create and read sequence (buyer)

```mermaid
sequenceDiagram
    actor Buyer
    participant Browser
    participant ReviewView as Review / product views
    participant Form as ReviewForm
    participant DB as MariaDB

    alt Create review
        Buyer->>Browser: Submit rating and comment
        Browser->>ReviewView: POST /products/{id}/review/
        ReviewView->>Form: Validate rating and comment
        Form-->>ReviewView: Valid data
        ReviewView->>DB: READ order items to verify purchase
        DB-->>ReviewView: Purchase status
        ReviewView->>DB: CREATE review for buyer and product
        ReviewView-->>Browser: Redirect to product detail
    else Read reviews
        Buyer->>Browser: Open product detail
        Browser->>ReviewView: GET /products/{id}/view/
        ReviewView->>DB: READ product and related reviews
        DB-->>ReviewView: Product and review data
        ReviewView-->>Browser: Render reviews with product
    end
```

The current application exposes review creation and reading. Review update and delete endpoints are not implemented, so the diagram deliberately does not claim that those operations exist.
