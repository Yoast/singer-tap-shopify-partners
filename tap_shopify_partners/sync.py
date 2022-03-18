"""Sync data."""
# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timezone
from typing import Callable, Optional

import singer
from singer.catalog import Catalog, CatalogEntry

from tap_shopify_partners import tools
from tap_shopify_partners.shopify_partners import Shopify
from tap_shopify_partners.streams import STREAMS

LOGGER: logging.RootLogger = singer.get_logger()


def sync(
    shopify_partners: Shopify,
    state: dict,
    catalog: Catalog,
    start_date: str,
) -> None:
    """Sync data from tap source.

    Arguments:
        shopify_partners {Shopify} -- Shopify Partners client
        state {dict} -- Tap state
        catalog {Catalog} -- Stream catalog
        start_date {str} -- Start date
    """
    # For every stream in the catalog
    LOGGER.info('Sync')
    LOGGER.debug('Current state:\n{state}')

    # Only selected streams are synced, whether a stream is selected is
    # determined by whether the key-value: "selected": true is in the schema
    # file.
    for stream in catalog.get_selected_streams(state):
        LOGGER.info(f'Syncing stream: {stream.tap_stream_id}')

        # Update the current stream as active syncing in the state
        singer.set_currently_syncing(state, stream.tap_stream_id)

        # Retrieve the state of the stream
        stream_state: dict = tools.get_stream_state(
            state,
            stream.tap_stream_id,
        )

        LOGGER.debug(f'Stream state: {stream_state}')
        LOGGER.info(f'Stream state: {stream_state}')
        # Write the schema
        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        # Every stream has a corresponding method in the Shopify object e.g.:
        # The stream: shopify_partners_app_subscription_sale will call: shopify_partners.shopify_partners_app_subscription_sale
        tap_data: Callable = getattr(shopify_partners, stream.tap_stream_id)

        # The tap_data method yields rows of data from the API
        # The state of the stream is used as kwargs for the method
        # E.g. if the state of the stream has a key 'start_date', it will be
        # used in the method as start_date='2021-01-01T00:00:00+0000'
        for row in tap_data(**stream_state):
            sync_record(stream, row, state)


def sync_record(stream: CatalogEntry, row: dict, state: dict) -> None:
    """Sync the record.

    Arguments:
        stream {CatalogEntry} -- Stream catalog
        row {dict} -- Record
        state {dict} -- State
    """
    # Retrieve the value of the bookmark
    bookmark: Optional[str] = tools.retrieve_bookmark_with_path(
        stream.replication_key,
        row,
    )

    # Create new bookmark
    # new_bookmark: str = tools.create_bookmark(stream.tap_stream_id, bookmark)

    # Write a row to the stream
    singer.write_record(
        stream.tap_stream_id,
        row,
        time_extracted=datetime.now(timezone.utc),
    )
    if bookmark:
        # Save the bookmark to the state
        # Temporary logging:
        
        # Add milisecond so data is never duplicated:
        # state = state['start_date'].replace('000000Z', '100000Z')
        LOGGER.info(f'%%%%%%%%%row: {row}')
        LOGGER.info(f'%%%%%%%state: {state}')
        temp_state = state
        tools.clear_currently_syncing(temp_state)

        for key1 in temp_state:
            for key2 in temp_state[key1]:
                temp_state[key1][key2]['start_date'] = temp_state[key1][key2]['start_date'].replace('000000Z', '100000Z')
        
        LOGGER.info(f'```````state: {state}')
        singer.write_bookmark(
            temp_state,
            stream.tap_stream_id,
            STREAMS[stream.tap_stream_id]['bookmark'],
            bookmark,
        )

        # Clear currently syncing
        tools.clear_currently_syncing(state)

        # Write the bookmark
        singer.write_state(state)
