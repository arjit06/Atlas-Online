from django.shortcuts import render,redirect
from django.http import HttpResponse
from math import ceil
from .models import Items,Customer,Bills,Ledger,Category,Product,Brand
import json
from datetime import date

customer=-1
Cart=""
def index(request,flag=0):
    food= Items.objects.filter(category_name="food")
    appliances= Items.objects.filter(category_name="Appliances")
    electronics= Items.objects.filter(category_name="electronics")
    sports= Items.objects.filter(category_name="sports Equipment")
    office= Items.objects.filter(category_name="office supplies and stationary")
    medical= Items.objects.filter(category_name="medical supplies")
    products= Items.objects.all()
    params={"food":food,"appliances":appliances,"electronics":electronics,"sports":sports,"office":office,"medical":medical,"flag":flag,"customer":customer,"products":products}
    return render(request,'shop/index.html',params)

def food(request):

    products= Items.objects.filter(category_name="food")
    n=len(products)
    params={"products":products,"category":"FOOD PRODUCTS","firstRows":range(0,ceil(n/4)-1),"lastRow":range(0,n-4*(ceil(n/4)-1)),"four":range(0,4),"customer":customer}
    return render(request,'shop/food.html',params)

def health(request):
    products= Items.objects.filter(category_name="health")
    params={"products":products,"category":"HEALTH PRODUCTS","customer":customer}
    return render(request,'shop/health.html',params)

def beauty(request):
    products= Items.objects.filter(category_name="beauty")
    params={"products":products,"category":"BEAUTY PRODUCTS","customer":customer}
    return render(request,'shop/beauty.html',params)

def clothes(request):
    products= Items.objects.filter(category_name="clothes")
    params={"products":products,"category":"CLOTHES","customer":customer}
    return render(request,'shop/clothes.html',params)

def furniture(request):
    products= Items.objects.filter(category_name="furtniture")
    params={"products":products,"category":"FURNITURE","customer":customer}
    return render(request,'shop/furniture.html',params)

def daily_items(request):
    products= Items.objects.filter(category_name="Daily_Items")
    params={"products":products,"category":"DAILY ITEMS","customer":customer}
    return render(request,'shop/daily_items.html',params)

def appliances(request):
    products= Items.objects.filter(category_name="Appliances")
    params={"products":products,"category":"APPLIANCES","customer":customer}
    return render(request,'shop/appliances.html',params)

def beverages(request):
    products= Items.objects.filter(category_name="beverages")
    params={"products":products,"category":"BEVERAGES","customer":customer}
    return render(request,'shop/beverages.html',params)

def electronics(request):
    products= Items.objects.filter(category_name="electronics")
    params={"products":products,"category":"ELECTRONICS","customer":customer}
    return render(request,'shop/electronics.html',params)

def sports_equipment(request):
    products= Items.objects.filter(category_name="sports Equipment")
    params={"products":products,"category":"SPORTS EQUIPMENT","customer":customer}
    return render(request,'shop/sports_equipment.html',params)

def cleaning(request):
    products= Items.objects.filter(category_name="cleaning")
    params={"products":products,"category":"CLEANING","customer":customer}
    return render(request,'shop/cleaning.html',params)

def office(request):
    products= Items.objects.filter(category_name="office supplies and stationary")
    params={"products":products,"category":"OFFICE SUPPLIES AND STATIONERY","customer":customer}
    return render(request,'shop/office.html',params)

def medical(request):
    products= Items.objects.filter(category_name="medical supplies")
    params={"products":products,"category":"MEDICAL SUPPLIES","customer":customer}
    return render(request,'shop/medical.html',params)

def signup(request):
    if request.method=='POST':
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        address=request.POST.get('address','')
        # print(name,email,password,address)
        new_customer=Customer(cust_name=name,cust_pass=password, email=email,residence=address)
        new_customer.save()
    return redirect("/shop/")

# create logout button then set cutomer to none if clicked
def login(request):
    global customer
    if request.method=='POST':
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        temp_customer=Customer.objects.filter(email=email,cust_pass=password)
        if (len(temp_customer)==0):
            return index(request,flag=1)
        else:
            customer=temp_customer[0]
            return index(request)
        
def logout(request):
      global customer
      customer=-1
      return index(request)

def prodView(request,id):
    product= Items.objects.get(item_id=id)
    # print(id)
    params={"product":product}
    return render(request,'shop/productview.html',params)

def searchMatch(product , query):
    product_name=product.product_name.lower()
    brand_name=product.brand_name.lower()
    category_name=product.category_name.lower()
    descript=product.descript.lower()
    query=query.lower()

    if ((query in descript) or (query in product_name) or (query in brand_name) or (query in category_name)):
        return True
    else :
        return False

def search(request):
    query= request.GET.get('search')
    temp=Items.objects.all()
    products=[a for a in temp if (searchMatch(a,query)) ]
    params={'products':products}
    return render(request,'shop/search.html',params)


def cart(request):
    global Cart
    result = request.GET.get('result', None)
  

    if (result!=None):
        Cart=result
    # print(Cart)
    d=json.loads(Cart)
    
   
    Products={}
    var=0
    for a in d:
        temp_prod=Items.objects.get(item_id=a)
        Products[temp_prod]=[d[a],d[a]*temp_prod.cost_price]
        var+=d[a]*temp_prod.cost_price
    # print(Products)
    params={'products':Products,'sum':var,'customer':customer}
    return render(request,"shop/viewCart.html",params)


def checkout(request):
   print(customer)
   d=json.loads(Cart)
   if customer!=-1:
       last=Ledger.objects.all()
       max=0
       for a in last:
           if a.bill_no>max:
               max=a.bill_no
       print(max+1)
       new_ledger=Ledger(bill_no=max+1, date_of_purchase =date.today(), customer=customer)
       new_ledger.save()

   for a in d:
        temp_prod=Items.objects.get(item_id=a)
        new_bill=Bills(max+1,category=Category.objects.get(category_name=temp_prod.category_name) ,product=Product.objects.get(product_name=temp_prod.product_name),brand=Brand.objects.get(brand_name=temp_prod.brand_name),quantity=d[a],subtotal=d[a]*temp_prod.cost_price)
        new_bill.save()
   return redirect("/shop/")
         

