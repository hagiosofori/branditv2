import requests
import json

from django.shortcuts import reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect

from branditnew.contests.models.transactions import Transaction, Transaction_Type, Transaction_Status


#soon to be deleted
def process_invoice(request, item):
    client_id = "cowuvotv"
    client_secret = "qpjnqjcb"
    hubtel_payment_url = "https://api.hubtel.com/v1/merchantaccount/onlinecheckout/invoice/create"
    hubtel_invoice = {
        "invoice":{
            "total_amount": item.cost,
            "description": "something random for now",
        },
        "store":{
            "name": "Brandit",
            "tagline": "Africa’s largest online graphic design marketplace ",
            "phone": "+233 549 2424 05",
            "logo_url": "https://brandit.express/images/logo.png",
            "website_url": "https://brandit.express/dashboard.php",
        },
        "actions":{ #if paid, go to a view that will indicate so in the db. else that view should indicate that it's not so. then display appropriate alert in the template.
            "cancel_url": "http://brandit.express/create_contest",
            "return_url": "http://brandit.express/dashboard"
        }
    }
    print(hubtel_invoice)
    response = requests.post(hubtel_payment_url, json=hubtel_invoice, auth=(client_id, client_secret))
    print('done posting the invoice')
    
    data = response.json()
    transaction = Transaction.create(request.user, 'enter type here', 'enter amount here')
    return data
    # verify_payment(request, response, item)







def checkout(request, transaction_type, item_name, price, quantity=1, unit_price=None):
    #create the invoice. set return url to verify_payment
    client_id = "cowuvotv"
    client_secret = "qpjnqjcb"
    hubtel_payment_url = "https://api.hubtel.com/v1/merchantaccount/onlinecheckout/invoice/create"
    
    if transaction_type == "points purchase":
        return_url = "brandit.express/payments/points_purchase/verify_payment"
    else:
        return_url = "brandit.express/payments/dashboard"

    if transaction_type == "points purchase":
        return_url = "points"
    hubtel_invoice = {
        "invoice":{
            "items":{
                "item_0":{
                   "name": item_name,
                   "quantity": quantity,
                   "unit_price": unit_price,
                   "total_price": price,
                   "description": transaction_type,
                }
            },
            "total_amount": price,
            "description": transaction_type,

        },
        "store":{
            "name": "Brandit",
            "tagline": "Africa’s largest online graphic design marketplace ",
            "phone": "+233 549 2424 05",
            "logo_url": "https://brandit.express/images/logo.png",
            "website_url": "https://brandit.express/dashboard.php",
        },
        "actions":{ 
            #if paid, go to a view that will indicate so in the db. else that view should indicate that it's not so. then display appropriate alert in the template.
            "cancel_url": "http://brandit.express/",
            "return_url": return_url
        }
    }

    #create the transaction object, and save to db.
    response = requests.post(hubtel_payment_url, json=hubtel_invoice, auth=(client_id, client_secret))
    data = response.json()

    transaction = Transaction.create(request.user, transaction_type, price, data['token'])
    transaction.save()
    request.session['transaction'] = transaction.id

    return data
    
    #redirect to checkout.




def verify_payment(request, trans=None):
    client_id = "cowuvotv"
    client_secret = "qpjnqjcb"
    #get the current transaction you're working with from the sesion
    #transform this to get_object_or_404 
    if trans:
        transaction = trans
    else:
        transaction = Transaction.objects.get(pk=request.session['transaction'])
    verify_url = "https://api.hubtel.com/v1/merchantaccount/onlinecheckout/invoice/status/"+transaction.token
    response = requests.get(verify_url, auth=(client_id, client_secret))
    data = response.json()

    #check if payment was completed from hubtel, and update status of transaction accordingly.
    if data['status'] == "completed":
        transaction.status = Transaction_Status.objects.get(name="completed")
        transaction.save()
    elif data['status'] == "cancelled":
        transaction.status = Transaction_Status.objects.get(name="cancelled")
    
    transaction.save()
    
    #redirect to appropriate view with the alert that it has been successfully created. also indicate that we're awaiting validation from brandit.
    if not trans:
        del request.session['transaction']
    
    return data['status'] == "completed"


