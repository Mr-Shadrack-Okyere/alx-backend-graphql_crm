#!/usr/bin/env python3
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_FILE = "/tmp/order_reminders_log.txt"

def main():
    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    one_week_ago = (datetime.now() - timedelta(days=7)).isoformat()

    query = gql("""
        query GetRecentOrders($date: DateTime!) {
            orders(orderDate_Gte: $date) {
                id
                customer {
                    email
                }
            }
        }
    """)

    result = client.execute(query, variable_values={"date": one_week_ago})

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log:
        for order in result.get("orders", []):
            log.write(
                f"[{timestamp}] Order ID: {order['id']}, "
                f"Customer Email: {order['customer']['email']}\n"
            )

    print("Order reminders processed!")


if __name__ == "__main__":
    main()
