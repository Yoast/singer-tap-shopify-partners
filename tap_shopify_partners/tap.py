"""Shopify Partners tap."""
# -*- coding: utf-8 -*-
import logging
from argparse import Namespace

import pkg_resources
from singer import get_logger, utils
from singer.catalog import Catalog

from tap_shopify_partners.shopify_partners import Shopify
from tap_shopify_partners.discover import discover
from tap_shopify_partners.sync import sync

VERSION: str = pkg_resources.get_distribution('tap-shopify-partners').version
LOGGER: logging.RootLogger = get_logger()
REQUIRED_CONFIG_KEYS: tuple = (
    'organization_id',
    'shopify_partners_server_token',
    'start_date'
)


@utils.handle_top_exception(LOGGER)
def main() -> None:
    """Run tap."""
    # Parse command line arguments
    args: Namespace = utils.parse_args(REQUIRED_CONFIG_KEYS)

    LOGGER.info(f'>>> Running tap-shopify-partners v{VERSION}')

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog: Catalog = discover()
        catalog.dump()
        return

    # Otherwise run in sync mode
    if args.catalog:
        # Load command line catalog
        catalog = args.catalog
    else:
        # Loadt the  catalog
        catalog = discover()

    # Initialize Shopify Partners client
    shopify_partners: Shopify = Shopify(
        args.config['organization_id'],
        args.config['shopify_partners_server_token'],
    )

    sync(shopify_partners, args.state, catalog, args.config['start_date'])


if __name__ == '__main__':
    main()
