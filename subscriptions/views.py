from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from .models import (Plan, Customer, Coupon, Setting)
# from .forms import LinkedinProfileForm, CampaignForm
import stripe
import logging
import csv
import io
import base64
from summarizerApp.utils import DgClass

logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def checkout(request, plan_id=""):
    if customerPlan(request):
        messages.success(request, ("You Have An Active Plan"))
        return redirect("dashboard")
    # coupons = Campaign.objects.filter(user=request.user)

    setting = DgClass.getSettings()
    stripe.api_key = setting.stripe_api_key
    stripe_key = stripe.api_key
    publishable_key = setting.publishable_key
    plan = ""
    if request.method == "GET" and "plan" in request.GET:
        # plan = Plan.objects.get(pk=request.GET['plan'])
        plan = get_object_or_404(Plan, pk=request.GET["plan"])
    elif plan_id:
        plan = get_object_or_404(Plan, pk=plan_id)
    else:
        plan = get_object_or_404(Plan, pk=1)

    if request.method == "POST":
        if "plan" in request.POST:
            plan = get_object_or_404(Plan, pk=request.POST["plan"])

        customer = Customer.objects.filter(user_id=request.user.id).first()
        stripe_customer = ""
        if customer:
            stripe_customer = stripe.Customer.retrieve(customer.stripeid)
        else:
            stripe_customer = stripe.Customer.create(
                email=request.user.email, source=request.POST["stripeToken"]
            )
        if "coupon" in request.POST:
            promo = Coupon.objects.filter(code=request.POST["coupon"]).first()
            if promo:
                # messages.error(request, ("Invalid coupon code2"))
                try:
                    coupon = stripe.Coupon.create(duration="once",id=request.POST["coupon"],amount_off=promo.discount)
                except:
                    pass
                subscription = stripe.Subscription.create(customer=stripe_customer.id,items=[{"plan": plan.stripe_id}],coupon=request.POST["coupon"])
            else:
                subscription = stripe.Subscription.create(customer=stripe_customer.id,items=[{"plan": plan.stripe_id}])
        else:
            subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{"plan": plan.stripe_id}])

        customer = Customer.objects.filter(user_id=request.user.id).first()
        if not customer:
            customer = Customer()

        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.current_period_end = subscription.current_period_end
        customer.plan = plan
        customer.save()

        messages.info(request, ("Subscription Successful.."))
        return redirect("dashboard")
    else:
        coupon = "none"
        price = plan.price
        og_dollar = plan.price
        coupon_dollar = 0
        final_dollar = plan.price

        if request.method == "GET" and "coupon" in request.GET:
            # print(coupons)
            promo = Coupon.objects.filter(code=request.GET["coupon"]).first()
            if not promo:
                messages.error(request, ("Invalid coupon code"))
            else:
                coupon = request.GET["coupon"]
                coupon_dollar = promo.discount
                final_dollar = plan.price - promo.discount
                price = plan.price - promo.discount

        price = price * 100  # to get the penny value

    return render(
        request,
        "subscriptions/checkout.html",
        {
            "plan": plan,
            "coupon": coupon,
            "price": price,
            "og_dollar": og_dollar,
            "coupon_dollar": coupon_dollar,
            "final_dollar": final_dollar,
            "stripe_key": stripe_key,
            "publishable_key": publishable_key,
        },
    )



def customerPlan(request):
    customer = Customer.objects.filter(user_id=request.user.id).first()
    if customer and customer.membership:
        return customer.plan
        # response = True
    return False




@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(
            customer.stripe_subscription_id)
        if(subscription.status != "active"):
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse("completed")
