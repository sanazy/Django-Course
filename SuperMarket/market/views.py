"""
    You can define utility functions here if needed
    For example, a function to create a JsonResponse
    with a specified status code or a message, etc.

    DO NOT FORGET to complete url patterns in market/urls.py
"""
from django.http import JsonResponse
from rest_framework.utils import json

from market.models import Product


def product_insert(request):
    # Check if Request is POST
    if request.method != 'POST':
        raise Exception('Http Method is not POST')

    # Get JSON Data from request
    json_data = json.loads(request.body)

    # Check existence of fields
    if ('code' or 'name' or 'price') not in json_data:
        return JsonResponse({"message": "some fields are not given"}, status=400)

    # Check value type of fields
    if (type(json_data['code']) != str) or (type(json_data['name']) != str) or (type(json_data['price']) != int) \
            or (len(json_data['code']) > 10) or (len(json_data['name']) > 100):
        return JsonResponse({"message": "value of fields have problem"}, status=400)

    # Check if code is unique
    if Product.objects.all().filter(code=json_data['code']).exists():
        return JsonResponse({"message": "code must be unique"}, status=400)

    # Check if price is positive
    if json_data['price'] < 0:
        return JsonResponse({"message": "price value must be greater than 0"}, status=400)

    # Create a product
    product = Product()
    product.code = json_data['code']
    product.name = json_data['name']
    product.price = json_data['price']

    # Check if inventory filed is given and is positive
    if 'inventory' not in json_data:
        product.inventory = 0
    else:
        if json_data['inventory'] < 0:
            return JsonResponse({"message": "value of inventory must be greater than 0"}, status=400)
        product.inventory = json_data['inventory']

    # Save product
    product.save()
    return JsonResponse({"id": product.id}, status=201)


def product_list(request):
    if request.method != 'GET':
        raise Exception('Http Method is not GET')

    if 'search' in request.GET:
        query = request.GET['search']
        products = Product.objects.all().filter(name__contains=query)
    else:
        products = Product.objects.all()

    response = dict({"products": []})
    for product in products:
        dic_product = dict({"id": product.id,
                            "code": product.code,
                            "name": product.name,
                            "price": product.price,
                            "inventory": product.inventory
                            })
        response["products"].append(dic_product)
    return JsonResponse(response, status=200)


def product_details(request, product_id):
    if request.method != 'GET':
        raise Exception('Http Method is not GET')

    if Product.objects.filter(id=product_id).exists():
        product = Product.objects.get(id=product_id)
        response = dict({"id": product.id,
                         "code": product.code,
                         "name": product.name,
                         "price": product.price,
                         "inventory": product.inventory
                        })
        return JsonResponse(response, status=200)
    else:
        return JsonResponse({"message": "Product Not Found."}, status=404)


def edit_inventory(request, product_id):
    # Check if Request is POST
    if request.method != 'POST':
        raise Exception('Http Method is not POST')

    # Get JSON Data from request
    json_data = json.loads(request.body)

    # Check existence of amount field
    if 'amount' not in json_data:
        return JsonResponse({"message": "amount field was not found"}, status=400)

    # Check value type of amount field
    if type(json_data['amount']) != int:
        return JsonResponse({"message": "value for amount field was not int"}, status=400)

    amount = json_data['amount']

    # Check if product with such product_id exist
    if not Product.objects.filter(id=product_id).exists():
        return JsonResponse({"message": "Product Not Found."}, status=404)

    product = Product.objects.get(id=product_id)

    # Check if there is enough Inventory
    if product.inventory + amount < 0:
        return JsonResponse({"message": "Not enough inventory."}, status=400)

    # Update product
    product. inventory = product.inventory + amount
    product.save()

    # Send Response
    response = dict({"id": product.id,
                     "code": product.code,
                     "name": product.name,
                     "price": product.price,
                     "inventory": product.inventory
                     })

    return JsonResponse(response, status=200)



