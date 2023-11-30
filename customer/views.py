from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,DetailView,View,ListView
from account.models import Product,Cart,Order
from customer.models import Review
from django.contrib import messages
from .forms import ReviewForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"please login!!")
            return redirect('log')
    return inner

dec=[signin_required,never_cache]
# Create your views here.

# class ProductDetView(TemplateView):
#     template_name="product.html"

@method_decorator(dec,name="dispatch")
class ProductDetView(DetailView):
    template_name="product.html"
    pk_url_kwarg='id'
    queryset=Product.objects.all()
    context_object_name="data"

    def get_context_data(self, **kwargs):
        form=ReviewForm()
        context=super().get_context_data(**kwargs)
        context['form']=form
        pro=kwargs.get('object')
        reviews=Review.objects.filter(product=pro)
        context['review']=reviews
        return context

dec
def addreview(request,*args,**kwargs):
    pid=kwargs.get('id')
    form_data=ReviewForm(data=request.POST)
    if form_data.is_valid():
        review=form_data.cleaned_data.get('review')
        product=Product.objects.get(id=pid)
        user=request.user
        Review.objects.create(user=user,review=review,product=product)
        messages.success(request,"Review added!!")
        return redirect('prodet',id=pid)
    messages.error(request,"Review not added!!")
    return redirect('home')

@method_decorator(dec,name="dispatch")
class AddtoCartView(View):
    def get(self,request,**kwargs):
        pid=kwargs.get('id')
        product=Product.objects.get(id=pid)
        user=request.user
        Cart.objects.create(product=product,user=user)
        messages.success(request,"Product added to cart!!")
        return redirect('home')

@method_decorator(dec,name="dispatch")
class CartlistView(ListView):
    template_name="cart.html"
    queryset=Cart.objects.all()
    context_object_name="cart"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user,status='cart')

@method_decorator(dec,name="dispatch")
class DelCartItemView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.delete()
        messages.success(request,"Cart Item Removed!!")
        return redirect('cartlist')

@method_decorator(dec,name="dispatch")
class Checkoutview(View):
    def get(self,request,**kwargs):
        return render(request,"checkout.html")
    def post(self,request,**kwargs):
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        add=request.POST.get('address')
        ph=request.POST.get('phone')
        Order.objects.create(cart=cart,phone=ph,address=add)
        cart.status="Order Placed"
        cart.save()
        messages.success(request,"Order Placed!!")
        return redirect('home')

@method_decorator(dec,name="dispatch")
class OrderlistView(ListView):
    template_name="Order.html"
    queryset=Order.objects.all()
    context_object_name="data"

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user)

dec
def cancelorder(request,*args,**kwargs):
    oid=kwargs.get('id')
    order=Order.objects.get(id=oid)
    order.status='Cancelled'
    order.save()
    messages.success(request,"Order Cancelled!!")
    return redirect('olist')