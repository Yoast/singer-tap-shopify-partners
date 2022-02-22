"""Shopify Partners Queries."""
# -*- coding: utf-8 -*-

from types import MappingProxyType

QUERIES: MappingProxyType = MappingProxyType({
    'app_subscription_sale': """
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
            id
            name
          }
          shop {
            myshopifyDomain
            name
            id
          }
          billingInterval
          chargeId
        }
      }
    }
  }
}
    """,
  'app_sale_adjustment': """
query {
  transactions(types: [APP_SALE_ADJUSTMENT], createdAtMin:":fromdate:", createdAtMax:":todate:") {
    edges {
      node {
        ... on AppSaleAdjustment {  
          app{
            id
            name
          }
          chargeId
          createdAt
          grossAmount {
            amount
            currencyCode
          }
          id
          netAmount{
            amount
            currencyCode
          }
          shop{
            id
            myshopifyDomain
            name
          }
          shopifyFee{
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

