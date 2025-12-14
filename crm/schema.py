import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order

# -----------------------
# Customer Type
# -----------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


# -----------------------
# Query Class
# -----------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()
