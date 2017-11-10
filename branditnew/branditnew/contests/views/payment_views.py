import requests
import json

from django.shortcuts import reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect


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
    return data
    # verify_payment(request, response, item)


def verify_payment(request, response, item):
    #if the payment was made, update the db accordingly, else still update the db accordingly.

    #redirect to appropriate view with the alert that it has been successfully created. also indicate that we're awaiting validation from brandit.
    return redirect(reverse('dashboard'))



