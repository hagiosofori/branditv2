from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, reverse

from branditnew.contests.models.templates import Template, Template_Order
from branditnew.contests.models.forms import Template_Order_Form
from branditnew.contests.views.payment_views import process_invoice




def templates_list(request):
    templates = Template.objects.all()
    context = {
        'templates': templates,
    }
    return render(request, "contests/templates.html", context)



#takes the form values, stores them in the db, stores the primary key of the db value in the session, and then redirects to verification.
# if user goes back to change the values of the template order, then value in the db is updated.
def details(request, template_id):
    template = Template.objects.get(pk=template_id)
    form = Template_Order_Form()

    if request.method == "POST": 
        form = Template_Order_Form(request.POST)
        
        if form.is_valid():
            if 'template_order' not in request.session:
                template_order = form.save(commit=False)
            else:
                template_order = Template_Order.objects.get(pk=request.session['template_order'])
            
            template_order.template = Template.objects.get(pk=template_id)
            template_order.client = request.user
            template_order.cost = template_order.template.cost
            template_order.quantity = form.cleaned_data.get('quantity')
            template_order.changes = form.cleaned_data.get('changes')
            template_order.save()
            print(template_order.template, template_order.cost, template_order.quantity, template_order.changes)
            
            request.session['template_order'] = template_order.id

            return redirect(reverse("templates:verify_order", args=(template_id)))


    context = {
        'template': template,
        'form': form,
    }
    return render(request, "contests/template_details.html", context)



#shows the user a summary of the template order. on approval, redirect to payment gateway; currently hubtel.
def verify_order(request, template_id):
    template_order = Template_Order.objects.get(pk=request.session['template_order'])
    
    if request.method == "POST":
        template_order.save()

        messages.add_message(request, messages.SUCCESS, "Successfully placed order for template", extra_tags='alert alert-success')

        data = process_invoice(request, template_order)
        del request.session['template_order']
        
        return redirect(data['response_text'], data['token'])

    context = {
        'template_order': template_order,
    }
    return render(request, "contests/verify_template_order.html", context)