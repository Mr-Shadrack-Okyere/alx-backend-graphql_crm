from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from celery import shared_task

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/crm_report_log.txt"


@shared_task
def generate_crm_report():
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
            customers {
                id
            }
            orders {
                id
                totalAmount
            }
        }
    """)

    result = client.execute(query)

    total_customers = len(result.get("customers", []))
    orders = result.get("orders", [])
    total_orders = len(orders)
    total_revenue = sum(order.get("totalAmount", 0) for order in orders)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log:
        log.write(
            f"{timestamp} - Report: "
            f"{total_customers} customers, "
            f"{total_orders} orders, "
            f"{total_revenue} revenue\n"
        )
