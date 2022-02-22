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
    'app_credit': """
{
  app(id: "gid://partners/App/4842809") {
    id
    name
    events(
      types: [CREDIT_APPLIED,
      				CREDIT_FAILED,
      				CREDIT_PENDING],
      occurredAtMin: ":fromdate:"
      occurredAtMax: ":todate:"
    ) {
      edges {
        node {
          app {
            name
            id
          }
          type
          occurredAt
          shop {
            id
            name
            myshopifyDomain
          }
          ... on CreditApplied {
            appCredit {
              amount {
              	amount
              	currencyCode
            	}
            	id 
            	name 
            	test
            }
          }
          ... on CreditFailed {
            appCredit {
              amount {
              	amount
              	currencyCode
            	}
              id
              name
              test
            }
          }
          ... on CreditPending {
            appCredit {
              amount {
              	amount
              	currencyCode
            	}
              id
              name
              test
            }
          }
        }
      }
    }
  }
}
    """,
    'app_relationship': """
{
  app(id: "gid://partners/App/4842809") {
    id
    name
    events(
      types: [RELATIONSHIP_DEACTIVATED,
      				RELATIONSHIP_INSTALLED,
      				RELATIONSHIP_REACTIVATED,
      				RELATIONSHIP_UNINSTALLED],
      occurredAtMin: ":fromdate:"
      occurredAtMax: ":todate:"
    ) {
      edges {
        node {
          app {
            name
            id
          }
          occurredAt
          shop {
            id
            name
            myshopifyDomain
          }
          type
          ... on RelationshipUninstalled {
            description
            reason
          }
        }
      }
    }
  }
}
    """,
})

