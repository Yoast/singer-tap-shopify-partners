"""Shopify Partners API Client."""  # noqa: WPS226
# -*- coding: utf-8 -*-

import logging
from datetime import datetime, timedelta, timezone, date
from types import MappingProxyType
from typing import Generator, Optional, Callable

import httpx
import singer
import time
import collections
from dateutil.parser import isoparse
from dateutil.rrule import DAILY, rrule

from tap_shopify_partners.cleaners import CLEANERS
from tap_shopify_partners.queries import QUERIES

API_SCHEME: str = 'https://'
API_BASE_URL: str = 'partners.shopify.com/'
API_ORG_ID: str = ':organization_id:/'
API_VERSION: str = 'api/2022-01/'
API_PATH_CALL_TYPE: str = 'graphql.json'

HEADERS: MappingProxyType = MappingProxyType({  # Frozen dictionary
    'Content-Type': 'application/graphql',
    'X-Shopify-Access-Token': ':token:',
})

class Shopify(object):  # noqa: WPS230
    """Shopify Partners API Client."""

    def __init__(
        self,
        organization_id: str,
        shopify_partners_access_token: str,
    ) -> None:
        """Initialize client.

        Arguments:
            organization_id {str} -- Shopify Partners organization id
            shopify_partners_access_token {str} -- Shopify Partners Server Token
        """
        self.organization_id: str = organization_id
        self.shopify_partners_access_token: str = shopify_partners_access_token
        self.logger: logging.Logger = singer.get_logger()
        self.client: httpx.Client = httpx.Client(http2=True)

    def flatten(
        self,
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
                items.extend(self.flatten(value, new_key, separator).items())
            elif isinstance(value, list):
                for k, v in enumerate(value):
                    items.extend(self.flatten({str(k): v}, new_key).items())
            else:
                items.append((new_key, value))
        return dict(items)

    def shopify_partners_transactions(  # noqa: WPS210, WPS213
        self,
        **kwargs: dict,
    ) -> Generator[dict, None, None]:
        """Shopify Partners transaction history.

        Raises:
            ValueError: When the parameter start_date is missing

        Yields:
            Generator[dict] -- Yields Shopify Partners transactions
        """
        self.logger.info('Stream Shopify Partners Transactions')

        # Validate the start_date value exists
        start_date_input: str = str(kwargs.get('start_date', ''))

        if not start_date_input:
            raise ValueError('The parameter start_date is required.')

        # Set start date and end date
        start_date: datetime = isoparse(start_date_input)
        end_date: datetime = datetime.now(timezone.utc).replace(microsecond=0)

        self.logger.info(
            f'Retrieving transactions from {start_date} to {end_date}',
        )
        # Extra kwargs will be converted to parameters in the API requests
        # start_date is parsed into batches, thus we remove it from the kwargs
        kwargs.pop('start_date', None)

        # Build URL
        org_id: str=API_ORG_ID.replace(':organization_id:', self.organization_id)
        url: str = (
            f'{API_SCHEME}{API_BASE_URL}{org_id}'
            f'{API_VERSION}{API_PATH_CALL_TYPE}'
        )
        self._create_headers()

        for date_day in self._start_days_till_now(start_date_input):
            query: str = QUERIES['transactions']
            # Replace dates in placeholders
            query = query.replace(':fromdate:', date_day + "T00:00:00.000000Z")
            query = query.replace(':todate:', date_day + "T23:59:59.999999Z")
            response: httpx._models.Response = self.client.post(  # noqa
                url,
                headers=self.headers,
                data=query,
                )
            time.sleep(0.3)

            # Define cleaner:
            cleaner: Callable = CLEANERS.get('clean_shopify_partners_transactions', {})

            # Raise error on 4xx and 5xxx
            response.raise_for_status()

            # Create dictionary from response
            response_data: dict = response.json()
            # transactions: List[dict] = response_data['data']['transactions']['edges']
            # transactions: List[dict] = response_data.get('edges', [])
           #  print(response_data['data']['transactions']['edges'])
            self.logger.info('~~~~~~~')
            # self.logger.info(transactions)
            self.logger.info(response_data)

            # yield cleaner(date_day, transactions)

            for transaction in response_data['data']['transactions']['edges']:
                self.logger.info('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                self.logger.info(transaction)
                temp_transaction = self.flatten(transaction)
                self.logger.info(temp_transaction)
                yield cleaner(date_day, temp_transaction)

            # for transaction in response_data:
            #     self.logger.info(transaction)
            #     yield cleaner(date_day, transaction)

            # yield from (
            #    cleaner(date_day, response_data)
                #for transaction in response_data['data']['transactions']['edges']
            #)
        

        self.logger.info('Finished: shopify_partners_transactions')

    def _create_headers(self) -> None:
        """Create authenticationn headers for requests."""
        headers: dict = dict(HEADERS)
        headers['X-Shopify-Access-Token'] = headers['X-Shopify-Access-Token'].replace(
            ':token:',
            self.shopify_partners_access_token,
        )
        self.headers = headers

    def _start_days_till_now(self, start_date: str) -> Generator:
        """Yield YYYY/MM/DD for every day until now.

        Arguments:
            start_date {str} -- Start date e.g. 2020-01-01

        Yields:
            Generator -- Every day until now.
        """
        # Parse input date
        year: int = int(start_date.split('-')[0])
        month: int = int(start_date.split('-')[1].lstrip())
        day: int = int(start_date.split('-')[2].lstrip())

        # Setup start period
        period: date = date(year, month, day)

        # Setup itterator
        dates: rrule = rrule(
            freq=DAILY,
            dtstart=period,
            until=datetime.utcnow(),
        )

        # Yield dates in YYYY-MM-DD format
        yield from (date_day.strftime('%Y-%m-%d') for date_day in dates)

