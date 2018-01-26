from django.shortcuts import render

from branditnew.contests.models.payment_requests import Payment_Request


def payment_requests(request):
    new_payment_requests = Payment_Request.objects.filter(is_touched=False)
    old_payment_requests = Payment_Request.objects.filter(is_touched=True)

    context = {
        'new_payment_requests': new_payment_requests,
        'old_payment_requests': old_payment_requests,
    }

    return render(request, 'contests/custom_admin_payment_requests.html', context)

