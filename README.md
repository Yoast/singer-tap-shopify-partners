# singer-tap-shopify-partners
This is a [Singer](https://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md#singer-specification).

This tap:

- Pulls raw data from [Shopify Partners](https://shopify.dev/api/partner)
- Extracts the following resources:
  - [Transactions](https://shopify.dev/api/partner/reference/transactions)
  - [App install/uninstall events](https://shopify.dev/api/partner/reference/apps)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state
### Step 1: Create an API client in Shopify Partners:
1. From your [Partner Dashboard](https://www.shopify.com/partners), navigate to Settings > Partner API clients, and then click Manage Partner API clients.
2. Click Create API client.
3. Enter a name to identify the API client.
4. Select the appropriate permissions. You can add or remove permissions from a Partner API client as needed.
5. Click Save, and then click Create API client.
6. In the Credentials section, next to the Access token field, click Show to show the access token, or click Copy to copy the access token to your clipboard.
### Step 2: Configure
Create a file called shopify_partners_config.json in your working directory, following config.json.example. The required parameters are the client_id and secret. 

This requires a state.json file to let the tap know from when to retrieve data. For example:
```
{
  "bookmarks": {
    "shopify-partners_app_subscription_sale": {
      "start_date": "2021-01-01T00:00:00+0000"
    }
  }
}
```
Will replicate app subscription sale data from 2021-01-01.

### Step 3: Install and Run
Create a virtual Python environment for this tap. This tap has been tested with Python 3.7, 3.8 and 3.9 and might run on future versions without problems.
```
python -m venv singer-shopify-partners
singer-shopify-partners/bin/python -m pip install --upgrade pip
singer-shopify-partners/bin/pip install git+https://github.com/Yoast/singer-tap-shopify-partners.git
```
This tap can be tested by piping the data to a local JSON target. For example:

Create a virtual Python environment with singer-json
```
python -m venv singer-json
singer-json/bin/python -m pip install --upgrade pip
singer-json/bin/pip install target-json
```
Test the tap:
```
singer-shopify-partners/bin/tap-shopify-partners --state state.json -c shopify-partners_config.json | singer-json/bin/target-json >> state_result.json
```
Copyright © 2021 Yoast
