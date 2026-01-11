from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    # GraphQL hello query
    try:
        transport = RequestsHTTPTransport(
            url=GRAPHQL_ENDPOINT,
            verify=True,
            retries=3,
        )

        client = Client(
            transport=transport,
            fetch_schema_from_transport=False,
        )

        query = gql("""
            query {
                hello
            }
        """)

        client.execute(query)
    except Exception:
        message += " (GraphQL error)"

    with open(LOG_FILE, "a") as file:
        file.write(message + "\n")

from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/low_stock_updates_log.txt"


def update_low_stock():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=False,
    )

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                products {
                    name
                    stock
                }
            }
        }
    """)

    result = client.execute(mutation)

    products = result["updateLowStockProducts"]["products"]

    with open(LOG_FILE, "a") as log:
        for product in products:
            log.write(
                f"[{timestamp}] {product['name']} new stock: {product['stock']}\n"
            )
