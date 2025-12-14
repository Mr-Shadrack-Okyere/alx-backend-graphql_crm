import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.db import transaction
import re

# -----------------------
# Types
# -----------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")


# -----------------------
# Queries
# -----------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()


# -----------------------
# Mutations
# -----------------------

# CreateCustomer
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(root, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")
        if phone and not re.match(r"^\+?\d{1,3}?[-.\s]?\d+$", phone):
            raise Exception("Invalid phone format")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()  # explicit save
        return CreateCustomer(customer=customer, message="Customer created successfully")


# BulkCreateCustomers
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        customers = graphene.List(CustomerInput, required=True)

    customers_created = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, customers):
        created = []
        errors = []

        with transaction.atomic():
            for c in customers:
                try:
                    if Customer.objects.filter(email=c.email).exists():
                        errors.append(f"{c.email} already exists")
                        continue
                    customer = Customer(name=c.name, email=c.email, phone=c.phone)
                    customer.save()  # explicit save
                    created.append(customer)
                except Exception as e:
                    errors.append(str(e))
        return BulkCreateCustomers(customers_created=created, errors=errors)


# CreateProduct
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=False)

    product = graphene.Field(ProductType)

    def mutate(root, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product(name=name, price=price, stock=stock)
        product.save()  # explicit save
        return CreateProduct(product=product)


# CreateOrder
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    def mutate(root, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Customer not found")

        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            raise Exception("At least one valid product must be selected")

        total_amount = sum([p.price for p in products])
        order = Order(customer=customer, total_amount=total_amount)
        order.save()  # explicit save
        order.products.set(products)
        return CreateOrder(order=order)


# -----------------------
# Main Mutation Class
# -----------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
