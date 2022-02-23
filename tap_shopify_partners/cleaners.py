"""Cleaner functions."""
# -*- coding: utf-8 -*-
from decimal import Decimal
from types import MappingProxyType
from tap_shopify_partners.streams import STREAMS
from dateutil.parser import parse as parse_d
from typing import Any, Optional
import collections

class ConvertionError(ValueError):
    """Failed to convert value."""


def to_type_or_null(
    input_value: Any,
    data_type: Optional[Any] = None,
    nullable: bool = True,
) -> Optional[Any]:
    """Convert the input_value to the data_type.

    The input_value can be anything. This function attempts to convert the
    input_value to the data_type. The data_type can be a data type such as str,
    int or Decimal or it can be a function. If nullable is True, the value is
    converted to None in cases where the input_value == None. For example:
    a '' == None, {} == None and [] == None.

    Arguments:
        input_value {Any} -- Input value

    Keyword Arguments:
        data_type {Optional[Any]} -- Data type to convert to (default: {None})
        nullable {bool} -- Whether to convert empty to None (default: {True})

    Returns:
        Optional[Any] -- The converted value
    """
    # If the input_value is not equal to None and a data_type input exists
    if input_value and data_type:
        # Convert the input value to the data_type
        try:
            return data_type(input_value)
        except ValueError as err:
            raise ConvertionError(
                f'Could not convert {input_value} to {data_type}: {err}',
            )

    # If the input_value is equal to None and Nullable is True
    elif not input_value and nullable:
        # Convert '', {}, [] to None
        return None

    # If the input_value is equal to None, but nullable is False
    # Return the original value
    return input_value

def clean_row(row: dict, mapping: dict) -> dict:
    """Clean the row according to the mapping.

    The mapping is a dictionary with optional keys:
    - map: The name of the new key/column
    - type: A data type or function to apply to the value of the key
    - nullable: Whether to convert empty values, such as '', {} or [] to None

    Arguments:
        row {dict} -- Input row
        mapping {dict} -- Input mapping

    Returns:
        dict -- Cleaned row
    """
    cleaned: dict = {}

    key: str
    key_mapping: dict

    # For every key and value in the mapping
    for key, key_mapping in mapping.items():

        # Retrieve the new mapping or use the original
        new_mapping: str = key_mapping.get('map') or key

        # Convert the value
        cleaned[new_mapping] = to_type_or_null(
            row[key],
            key_mapping.get('type'),
            key_mapping.get('null', True),
        )

    return cleaned

def flatten(
        dictionary, 
        parent_key=False, 
        separator='.'):
        """
        Turn a nested dictionary into a flattened dictionary
        :param dictionary: The dictionary to flatten
        :param parent_key: The string to prepend to dictionary's keys
        :param separator: The string used to separate flattened keys
        :return: A flattened dictionary
        """
        items = []
        for key, value in dictionary.items():
            new_key = str(parent_key) + separator + key if parent_key else key
            if isinstance(value, collections.MutableMapping):
                items.extend(flatten(value, new_key, separator).items())
            elif isinstance(value, list):
                for k, v in enumerate(value):
                    items.extend(flatten({str(k): v}, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)

def clean_shopify_partners_app_subscription_sale(
    date_day: str,
    response_data: dict,
) -> dict:
    """Clean shopify_partners_app_subscription_sale data.

        Arguments:
            response_data {dict} -- input response_data

        Returns:
            dict -- cleaned response_data
        """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['shopify_partners_app_subscription_sale'].get(
        'mapping',
    )

    cleaned_data: dict = {
        "id": response_data["node.id"],
        "createdAt": response_data["node.createdAt"],
        "netAmount": float(response_data["node.netAmount.amount"]),
        "netAmountCurrencyCode": response_data["node.netAmount.currencyCode"],
        "grossAmount": float(response_data["node.grossAmount.amount"]),
        "grossAmountCurrencyCode": response_data["node.grossAmount.currencyCode"],
        "shopifyFee": float(response_data["node.shopifyFee.amount"]),
        "shopifyFeeCurrencyCode": response_data["node.shopifyFee.currencyCode"],
        "app": response_data["node.app.name"],
        "appId": response_data["node.app.id"],
        "shopDomain": response_data["node.shop.myshopifyDomain"],
        "shopName": response_data["node.shop.name"],
        "shopId": response_data["node.shop.id"],
        "billingInterval": response_data["node.billingInterval"],
        "chargeId": response_data["node.chargeId"],
    }

    return clean_row(cleaned_data, mapping)

def clean_shopify_partners_app_sale_adjustment(
    date_day: str,
    response_data: dict,
) -> dict:
    """Clean shopify_partners_app_sale_adjustment data.

        Arguments:
            response_data {dict} -- input response_data

        Returns:
            dict -- cleaned response_data
        """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['shopify_partners_app_sale_adjustment'].get(
        'mapping',
    )

    cleaned_data: dict = {
        "app": response_data["node.app.name"],
        "appId": response_data["node.app.id"],
        "chargeId": response_data["node.chargeId"],
        "createdAt": response_data["node.createdAt"],
        "grossAmount": float(response_data["node.grossAmount.amount"]),
        "grossAmountCurrencyCode": response_data["node.grossAmount.currencyCode"],
        "id": response_data["node.id"],
        "netAmount": float(response_data["node.netAmount.amount"]),
        "netAmountCurrencyCode": response_data["node.netAmount.currencyCode"],
        "shopDomain": response_data["node.shop.myshopifyDomain"],
        "shopName": response_data["node.shop.name"],
        "shopId": response_data["node.shop.id"],
        "shopifyFee": float(response_data["node.shopifyFee.amount"]),
        "shopifyFeeCurrencyCode": response_data["node.shopifyFee.currencyCode"],
    }

    return clean_row(cleaned_data, mapping)

def clean_shopify_partners_app_credit(
    date_day: str,
    response_data: dict,
) -> dict:
    """Clean shopify_partners_app_credit data.

        Arguments:
            response_data {dict} -- input response_data

        Returns:
            dict -- cleaned response_data
        """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['shopify_partners_app_credit'].get(
        'mapping',
    )

    cleaned_data: dict = {
        "app": response_data["node.app.name"],
        "appId": response_data["node.app.id"],
        "occurredAt": response_data["node.occurredAt"],
        "shopDomain": response_data["node.shop.myshopifyDomain"],
        "shopName": response_data["node.shop.name"],
        "shopId": response_data["node.shop.id"],
        "type": response_data["node.type"],
        "appCredit": float(response_data["node.appCredit.amount"]),
        "appCreditCurrencyCode": response_data["node.appCredit.amount.currencyCode"],
        "appCreditId": response_data["node.appCredit.id"],
        "appCreditName": response_data["node.appCredit.name"],
        "appCreditTest": response_data["node.appCredit.test"],
    }

    return clean_row(cleaned_data, mapping)

def clean_shopify_partners_app_relationship(
    date_day: str,
    response_data: dict,
) -> dict:
    """Clean shopify_partners_app_relationship data.

        Arguments:
            response_data {dict} -- input response_data

        Returns:
            dict -- cleaned response_data
        """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['shopify_partners_app_relationship'].get(
        'mapping',
    )

    if response_data["node.type"] == "RELATIONSHIP_UNINSTALLED":
        cleaned_data: dict = {
            "app": response_data["node.app.name"],
            "appId": response_data["node.app.id"],
            "occurredAt": response_data["node.occurredAt"],
            "shopDomain": response_data["node.shop.myshopifyDomain"],
            "shopName": response_data["node.shop.name"],
            "shopId": response_data["node.shop.id"],
            "type": response_data["node.type"],
            "description": response_data["node.description"],
            "reason": response_data["node.reason"],
        }
    else:
        cleaned_data: dict = {
            "app": response_data["node.app.name"],
            "appId": response_data["node.app.id"],
            "occurredAt": response_data["node.occurredAt"],
            "shopDomain": response_data["node.shop.myshopifyDomain"],
            "shopName": response_data["node.shop.name"],
            "shopId": response_data["node.shop.id"],
            "type": response_data["node.type"],
            "description": None,
            "reason": None,
        }

    return clean_row(cleaned_data, mapping)

def clean_shopify_partners_app_subscription_charge(
    date_day: str,
    response_data: dict,
) -> dict:
    """Clean shopify_partners_app_subscription_charge data.

        Arguments:
            response_data {dict} -- input response_data

        Returns:
            dict -- cleaned response_data
        """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['shopify_partners_app_subscription_charge'].get(
        'mapping',
    )

    cleaned_data: dict = {
        "app": response_data["node.app.name"],
        "appId": response_data["node.app.id"],
        "subscriptionCharge": float(response_data["node.charge.amount.amount"]),
        "subscriptionChargeCurrencyCode": response_data["node.charge.amount.currencyCode"],
        "billingOn": response_data["node.charge.billingOn"],
        "id": response_data["node.charge.id"],
        "name": response_data["node.charge.name"],
        "test": response_data["node.charge.test"],
        "occurredAt": response_data["node.occurredAt"],
        "shopDomain": response_data["node.shop.myshopifyDomain"],
        "shopName": response_data["node.shop.name"],
        "shopId": response_data["node.shop.id"],
        "type": response_data["node.type"],
    }

    return clean_row(cleaned_data, mapping)

# Collect all cleaners
CLEANERS: MappingProxyType = MappingProxyType({
    'shopify_partners_app_subscription_sale': clean_shopify_partners_app_subscription_sale,
    'shopify_partners_app_sale_adjustment': clean_shopify_partners_app_sale_adjustment,
    'shopify_partners_app_credit': clean_shopify_partners_app_credit,
    'shopify_partners_app_relationship': clean_shopify_partners_app_relationship,
})