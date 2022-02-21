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

def clean_shopify_partners_transactions(
    date_day: str,
    response_data: dict,
) -> dict:
    """Clean shopify_partners_transactions data.

        Arguments:
            response_data {dict} -- input response_data

        Returns:
            dict -- cleaned response_data
        """
    # Get the mapping from the STREAMS
    # print('~~~~~~~~~~~~~About to go to mapping')
    mapping: Optional[dict] = STREAMS['shopify_partners_transactions'].get(
        'mapping',
    )

    # new_records: list = []
    # print(response_data)
    # for transaction in response_data["data"]["transactions"]["edges"]:
    #     transaction_flat = flatten(transaction)

        # transaction_flat = flatten(response_data['data']['transactions']['edges'])
        # Create new cleaned dict
        # print('~~~~~~~~~~~~~~about to go to dict')
    cleaned_data: dict = {
        # "id": response_data["node"].get("id"),
        # "createdAt": response_data["node"].get("createdAt"),
        # "netAmount": response_data["node"]["netAmount"].get("amount"),
        # "grossAmount": response_data["node"]["grossAmount"].get("amount"),
        # "shopifyFee": response_data["node"]["shopifyFee"].get("amount"),
        # "app": response_data["node"]["app"].get("name"),
        # "shopDomain": response_data["node"]["shop"].get("myshopifyDomain"),
        # "shopName": response_data["node"]["shop"].get("name"),
        # "billingInterval": response_data["node"].get("billingInterval"),
        "id": response_data["node.id"],
        "createdAt": response_data["node.createdAt"],
        "netAmount": float(response_data["node.netAmount.amount"]),
        "netAmountCurrencyCode": response_data["node.netAmount.currencyCode"],
        "grossAmount": float(response_data["node.grossAmount.amount"]),
        "grossAmountCurrencyCode": response_data["node.grossAmount.currencyCode"],
        "shopifyFee": float(response_data["node.shopifyFee.amount"]),
        "shopifyFeeCurrencyCode": response_data["node.shopifyFee.currencyCode"],
        "app": response_data["node.app.name"],
        "shopDomain": response_data["node.shop.myshopifyDomain"],
        "shopName": response_data["node.shop.name"],
        "shopId": response_data["node.shop.id"],
        "billingInterval": response_data["node.billingInterval"],
        "chargeId": response_data["node.chargeId"],
        "processingFee": float(response_data["node.processingFee.amount"]),
        "processingFeeCurrencyCode": response_data["node.processingFee.currencyCode"],
        "regulatoryOperatingFee": float(response_data["node.regulatoryOperatingFee"]),
        "regulatoryOperatingFeeCurrencyCode": response_data["node.regulatoryOperationgFee.currencyCode"]
    }
        # print("~~~~~~~~~~~Cleaned data (cleaners.py)")
        # print(cleaned_data)
        # new_records.append(cleaned_data)
    return clean_row(cleaned_data, mapping)
    # return[clean_row(new_record, mapping) for new_record in new_records]

# Collect all cleaners
CLEANERS: MappingProxyType = MappingProxyType({
    'shopify_partners_transactions': clean_shopify_partners_transactions,
})