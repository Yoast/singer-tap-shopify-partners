"""Shopify Partners Queries."""
# -*- coding: utf-8 -*-

from types import MappingProxyType

QUERIES: MappingProxyType = MappingProxyType({
    'app_subscription_sale': """
query {
  transactions(types: [APP_SUBSCRIPTION_SALE], createdAtMin:":fromdate:", createdAtMax:":todate:", first: 100, after: ":cursor:") {
    edges {
      cursor
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
    pageInfo{
        hasNextPage
    }
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
    'app_subscription_charge': """
{
  app(id: "gid://partners/App/4842809") {
    events(
      types: [SUBSCRIPTION_CHARGE_ACCEPTED, SUBSCRIPTION_CHARGE_ACTIVATED, SUBSCRIPTION_CHARGE_CANCELED, SUBSCRIPTION_CHARGE_DECLINED, SUBSCRIPTION_CHARGE_EXPIRED, SUBSCRIPTION_CHARGE_FROZEN, SUBSCRIPTION_CHARGE_UNFROZEN]
      occurredAtMin: ":fromdate:"
      occurredAtMax: ":todate:"
      first: 100
      after: ":cursor:"
    ) {
      pageInfo{
        hasNextPage
      }
      edges {
        cursor
        node {
          app {
            name
            id
          }
          ... on SubscriptionChargeAccepted {
            charge {
            	amount {
              	amount
              	currencyCode
            	}
            	billingOn
            	id
            	name
            	test
          	}
          }
          ... on SubscriptionChargeActivated {
            charge {
            	amount {
              	amount
              	currencyCode
            	}
            	billingOn
            	id
            	name
            	test
          	}
          }
          ... on SubscriptionChargeCanceled {
            charge {
            	amount {
              	amount
              	currencyCode
            	}
            	billingOn
            	id
            	name
            	test
          	}
          }
          ... on SubscriptionChargeDeclined {
            charge {
            	amount {
              	amount
              	currencyCode
            	}
            	billingOn
            	id
            	name
            	test
          	}
          }
          ... on SubscriptionChargeExpired {
            charge {
            	amount {
              	amount
              	currencyCode
            	}
            	billingOn
            	id
            	name
            	test
          	}
          }
          ... on SubscriptionChargeFrozen {
            charge {
            	amount {
              	amount
              	currencyCode
            	}
            	billingOn
            	id
            	name
            	test
          	}
          }
          ... on SubscriptionChargeUnfrozen {
            charge {
            	amount {
              	amount
              	currencyCode
            	}
            	billingOn
            	id
            	name
            	test
          	}
          }
          occurredAt
          shop {
            id
            name
            myshopifyDomain
          }
          type
        }
      }
    }
  }
}

    """,
})

