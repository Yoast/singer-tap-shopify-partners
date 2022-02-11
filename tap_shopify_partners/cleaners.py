"""Cleaner functions."""
# -*- coding: utf-8 -*-
from decimal import Decimal
from types import MappingProxyType
from tap_shopify_partners.streams import STREAMS
from dateutil.parser import parse as parse_d

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
    mapping: Optional[dict] = STREAMS['shopify_partners_transactions'].get(
        'mapping',
    )
    # Create new cleaned dict
    cleaned_data: dict = {
        'id': response_data['node'].get('id'),
        'createdAt': response_data['node'].get('createdAt'),
        'netAmount': response_data['node'].get('netAmount'),
        'grossAmount': response_data['node'].get('grossAmount'),
        'shopifyFee': response_data['node'].get('shopifyFee'),
        'app': response_data['node'].get('app'),
        'shop': response_data['node'].get('shop'),
        'billingInterval': response_data['node'].get('billingInterval'),
    }
    return clean_row(cleaned_data, mapping)

# Collect all cleaners
CLEANERS: MappingProxyType = MappingProxyType({
    'shopify_partners_transactions': clean_shopify_partners_transactions,
})