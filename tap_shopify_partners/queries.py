"""Shopify Partners Queries."""
# -*- coding: utf-8 -*-

from types import MappingProxyType

QUERIES: MappingProxyType = MappingProxyType({
    'transactions': """
query {
  transactions(types: [APP_SUBSCRIPTION_SALE], createdAtMin:":fromdate:", createdAtMax:":todate:") {
    edges {
      node {
        id
        createdAt
        ... on AppSubscriptionSale {
          netAmount {
            amount
          }
          grossAmount{
            amount
          }
          shopifyFee{
            amount
          }
          app {
            name
          }
          shop {
            myshopifyDomain
            name
          }
          billingInterval 
        }
      }
    }
  }
}
    """,
})

