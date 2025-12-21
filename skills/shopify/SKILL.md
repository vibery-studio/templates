---
name: shopify
description: Build Shopify applications, extensions, and themes using GraphQL/REST APIs, Shopify CLI, Polaris UI components, and Liquid templating. Use when building Shopify apps, implementing checkout customizations, developing themes, or managing store data via APIs.
license: MIT
---

# Shopify Development

Comprehensive guide for building on Shopify platform: apps, extensions, themes, and API integrations.

## Platform Overview

- **Shopify CLI**: Development workflow tool
- **GraphQL Admin API**: Primary API (recommended)
- **REST Admin API**: Legacy API
- **Polaris UI**: Design system
- **Liquid**: Template language

## Quick Start

### Create App
```bash
npm install -g @shopify/cli@latest
shopify app init
shopify app dev
```

### Create Extension
```bash
shopify app generate extension --type checkout_ui_extension
```

### Theme Development
```bash
shopify theme init
shopify theme dev
shopify theme push --development
```

## When to Build What

### App
- Integrating external services
- Functionality across multiple stores
- Merchant-facing admin tools
- Complex business logic

### Extension
- Customizing checkout flow
- Adding fields to admin pages
- POS actions for retail
- Discount/payment/shipping rules

### Theme
- Custom storefront design
- Unique shopping experiences
- Brand-specific layouts

## Essential Patterns

### GraphQL Query
```graphql
query GetProducts($first: Int!) {
  products(first: $first) {
    edges {
      node {
        id
        title
        variants(first: 5) {
          edges { node { id price } }
        }
      }
    }
  }
}
```

### Checkout Extension
```javascript
import { reactExtension, BlockStack, TextField } from '@shopify/ui-extensions-react/checkout';

export default reactExtension('purchase.checkout.block.render', () => <Extension />);
```

### Liquid Template
```liquid
{% for product in collection.products %}
  <div class="product-card">
    <img src="{{ product.featured_image | img_url: 'medium' }}">
    <h3>{{ product.title }}</h3>
    <p>{{ product.price | money }}</p>
  </div>
{% endfor %}
```

## Best Practices

- Prefer GraphQL over REST
- Request only needed fields
- Implement pagination
- Verify webhook signatures
- Use OAuth for public apps
- Request minimal access scopes

## Resources

- Shopify Docs: https://shopify.dev/docs
- GraphQL API: https://shopify.dev/docs/api/admin-graphql
- Polaris: https://polaris.shopify.com

## Credits

Source: https://github.com/mrgoonie/claudekit-skills
