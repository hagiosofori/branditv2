
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from branditnew.contests.models.print_orders import Item, Print_Order
from branditnew.contests.models.forms.print_order_forms import Create_Print_Order_Form
from branditnew.contests.views.payment_views import process_invoice





def new(request):
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request, "contests/print_orders_new.html", context)





@login_required
def create(request, item_id):
    form = Create_Print_Order_Form()
    
    #getting the price, for total cost calculation and display to the user on the form
    item = Item.objects.get(pk=item_id)
    cost = item.price

    if request.method == "POST":
        form = Create_Print_Order_Form(request.POST, request.FILES)

        if form.is_valid():
            print_order = form.save(commit=False)
            item = Item.objects.get(pk=item_id)
            print_order.item = item
            print_order.client = request.user
            print_order.cost = item.price * print_order.quantity
            print_order.save()

            return redirect(reverse("print_orders:print_order_verify", args=[print_order.id]))

    context = {
        'form': form,
        'cost': cost,
    }
    return render(request, "contests/print_order_create.html", context)




def verify(request, print_order_id):
    print_order = Print_Order.objects.get(pk=print_order_id)

    if request.method == "POST":
        data = process_invoice(request, print_order)
        return redirect(data['response_text'], data['token'])

    context = {
        'print_order': print_order,
    }
    return render(request, "contests/print_order_verify.html", context)






def edit(request, print_order_id):
    print_order = Print_Order.objects.get(pk=print_order_id)
    form = Create_Print_Order_Form(instance=print_order)

    if request.method == "POST":
        form = Create_Print_Order_Form(request.POST, request.FILES)
        
        if form.is_valid():
            cost = form.cleaned_data.get('')
            form.save(commit=False)
            print_order.cost = print_order.item.price * print_order.quantity
            print_order.save()

            return redirect(reverse("print_orders:print_order_verify", args=[print_order.id]))


    context = {
        'form': form,
        'print_order':print_order,
    }
    return render(request, "contests/print_order_edit.html", context)


