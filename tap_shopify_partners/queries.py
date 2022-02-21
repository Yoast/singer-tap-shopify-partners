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
            currencyCode
          }
          grossAmount{
            amount
            currencyCode
          }
          shopifyFee{
            amount
            currencyCode
          }
          app {
            name
          }
          shop {
            myshopifyDomain
            name
            id
          }
          billingInterval
          chargeId
          processingFee{
            amount
            currencyCode
          }
          regulatoryOperatingFee{
            amount
            currencyCode
          } 
        }
      }
    }
  }
}
    """,
})

