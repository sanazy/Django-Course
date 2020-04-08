from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.utils import json
from accounts.models import Customer


def customer_register(request):
    # Check if Request is POST
    if request.method != 'POST':
        raise Exception('Http Method is not POST')

    # Get JSON Data from request
    json_data = json.loads(request.body)

    # Create a customer

    user = User.objects.create_user(username=json_data['username'],
                                    password=json_data['password'],
                                    first_name=json_data['first_name'],
                                    last_name=json_data['last_name'],
                                    email=json_data['email'])
    customer = Customer.objects.create(user=user)
    customer.phone = json_data['phone']
    customer.address = json_data['address']
    customer.balance = 10000
    # Save customer
    user.save()
    customer.save()
    return JsonResponse({"id": customer.id}, status=201)


def customer_list(request):
    if request.method != 'GET':
        raise Exception('Http Method is not GET')

    if 'search' in request.GET:
        query = request.GET['search']
        customers = Customer.objects.all().filter(Q(user__first_name__contains=query) |
                                                  Q(user__last_name__contains=query) |
                                                  Q(user__username__contains=query) |
                                                  Q(address__contains=query))
    else:
        customers = Customer.objects.all()

    response = dict({"customers": []})
    for customer in customers:
        dic_product = dict({"id": customer.id,
                            "username": customer.user.username,
                            "first_name": customer.user.first_name,
                            "last_name": customer.user.last_name,
                            "email": customer.user.email,
                            "phone": customer.phone,
                            "address": customer.address,
                            "balance": customer.balance
                            })
        response["customers"].append(dic_product)
    return JsonResponse(response, status=200)


def customer_details(request, customer_id):
    if request.method != 'GET':
        raise Exception('Http Method is not GET')

    if not Customer.objects.filter(id=customer_id).exists():
        return JsonResponse({"message": "Customer Not Found."}, status=404)

    customer = Customer.objects.get(id=customer_id)
    response = dict({"id": customer.id,
                     "username": customer.user.username,
                     "first_name": customer.user.first_name,
                     "last_name": customer.user.last_name,
                     "email": customer.user.email,
                     "phone": customer.phone,
                     "address": customer.address,
                     "balance": customer.balance
                     })
    return JsonResponse(response, status=200)


def customer_login(request):
    json_data = json.loads(request.body)
    username = json_data['username']
    password = json_data['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "You are logged in successfully."}, status=200)
    else:
        return JsonResponse({"message": "Username or Password is incorrect."}, status=404)


def customer_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "You are logged out successfully."}, status=200)
    else:
        return JsonResponse({"message": "You are not logged in."}, status=403)


def customer_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "You are not logged in."}, status=403)
    else:
        user = request.user.username
        customer = Customer.objects.get(user__username__exact=user)
        response = dict({"id": customer.id,
                         "username": customer.user.username,
                         "first_name": customer.user.first_name,
                         "last_name": customer.user.last_name,
                         "email": customer.user.email,
                         "phone": customer.phone,
                         "address": customer.address,
                         "balance": customer.balance
                         })
        return JsonResponse(response, status=200)
