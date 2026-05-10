from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Customer, Restaurant, Item, Cart

import razorpay
from django.conf import settings

from .ai_utils import client, generate_recipe
from .ai_utils import client, generate_recipe


# =========================
# HOME
# =========================

def index(request):

    restaurantList = Restaurant.objects.filter(
        approved=True
    )

    username = request.session.get("username")

    role = request.session.get("role")

    if username and role == "customer":

        return render(
            request,
            "delivery/customer_home.html",
            {
                "restaurantList": restaurantList,
                "username": username
            }
        )

    return render(
        request,
        "delivery/index.html",
        {
            "restaurantList": restaurantList
        }
    )


# =========================
# AUTH
# =========================

def open_signin(request):

    return render(
        request,
        "delivery/signin.html"
    )


def open_signup(request):

    return render(
        request,
        "delivery/signup.html"
    )


def signup(request):

    if request.method == "POST":

        username = request.POST["username"]

        email = request.POST["email"]

        password = request.POST["password"]

        mobile = request.POST["mobile"]

        address = request.POST["address"]

        role = request.POST["role"]

        # ADMIN EMAIL CHECK

        if email == "shivanandshirur99@gmail.com":

            role = "admin"

        # CHECK EXISTING EMAIL

        existing_email = Customer.objects.filter(
            email=email
        ).first()

        if existing_email:

            return HttpResponse(
                "Email already registered"
            )

        # CHECK EXISTING USERNAME

        existing_username = Customer.objects.filter(
            username=username
        ).first()

        if existing_username:

            return HttpResponse(
                "Username already exists"
            )

        # CREATE USER

        Customer.objects.create(

            username=username,

            email=email,

            password=password,

            mobile=mobile,

            address=address,

            role=role

        )

        return redirect("open_signin")

    return redirect("open_signup")

def signin(request):

    username = request.POST["username"]

    password = request.POST["password"]

    customer = Customer.objects.filter(

        username=username,

        password=password

    ).first()

    if customer is None:

        return render(
            request,
            "delivery/fail.html"
        )

    request.session["username"] = customer.username

    request.session["role"] = customer.role

    request.session["email"] = customer.email

    # ADMIN LOGIN

    if customer.email == "shivanandshirur99@gmail.com":

        restaurantList = Restaurant.objects.all()

        return render(

            request,

            "delivery/admin_home.html",

            {

                "restaurantList": restaurantList,

                "username": customer.username

            }

        )

    # HOTEL MANAGER LOGIN

    elif customer.role == "manager":

        restaurants = Restaurant.objects.filter(

            owner=customer

        )

        return render(

            request,

            "delivery/manager_home.html",

            {

                "restaurants": restaurants,

                "username": customer.username

            }

        )

    # CUSTOMER LOGIN

    else:

        restaurantList = Restaurant.objects.filter(

            approved=True

        )

        return render(

            request,

            "delivery/customer_home.html",

            {

                "restaurantList": restaurantList,

                "username": customer.username

            }

        )


# =========================
# RESTAURANTS
# =========================

def open_add_restaurant(request):

    username = request.session.get("username")

    role = request.session.get("role")

    if not username:

        return redirect("open_signin")

    if role != "manager":

        return HttpResponse("Access Denied")

    return render(
        request,
        "delivery/add_restaurant.html"
    )


def add_restaurant(request):

    if request.method == "POST":

        username = request.session.get("username")

        role = request.session.get("role")

        if role != "manager":

            return HttpResponse("Access Denied")

        customer = Customer.objects.get(

            username=username

        )

        restaurant = Restaurant()

        restaurant.name = request.POST["name"]

        restaurant.picture = request.POST["picture"]

        restaurant.cuisine = request.POST["cuisine"]

        restaurant.rating = request.POST["rating"]

        restaurant.owner = customer

        restaurant.approved = False

        restaurant.save()

        restaurants = Restaurant.objects.filter(

            owner=customer

        )

        return render(

            request,

            "delivery/manager_home.html",

            {

                "restaurants": restaurants,

                "username": username

            }

        )

    return redirect("open_add_restaurant")


# =========================
# ADMIN RESTAURANT CONTROL
# =========================

def open_show_restaurant(request):

    email = request.session.get("email")

    if email != "shivanandshirur99@gmail.com":

        return HttpResponse("Only Admin Allowed")

    restaurantList = Restaurant.objects.all()

    return render(

        request,

        "delivery/show_restaurants.html",

        {

            "restaurantList": restaurantList

        }

    )


def open_update_restaurant(request, restaurant_id):

    email = request.session.get("email")

    if email != "shivanandshirur99@gmail.com":

        return HttpResponse("Only Admin Allowed")

    restaurant = Restaurant.objects.get(

        id=restaurant_id

    )

    return render(

        request,

        "delivery/update_restaurant.html",

        {

            "restaurant": restaurant

        }

    )


def update_restaurant(request, restaurant_id):

    email = request.session.get("email")

    if email != "shivanandshirur99@gmail.com":

        return HttpResponse("Only Admin Allowed")

    restaurant = Restaurant.objects.get(

        id=restaurant_id

    )

    restaurant.name = request.POST["name"]

    restaurant.picture = request.POST["picture"]

    restaurant.cuisine = request.POST["cuisine"]

    restaurant.rating = request.POST["rating"]

    restaurant.save()

    restaurantList = Restaurant.objects.all()

    return render(

        request,

        "delivery/show_restaurants.html",

        {

            "restaurantList": restaurantList

        }

    )


def delete_restaurant(request, restaurant_id):

    email = request.session.get("email")

    if email != "shivanandshirur99@gmail.com":

        return HttpResponse("Only Admin Allowed")

    restaurant = Restaurant.objects.get(

        id=restaurant_id

    )

    restaurant.delete()

    restaurantList = Restaurant.objects.all()

    return render(

        request,

        "delivery/show_restaurants.html",

        {

            "restaurantList": restaurantList

        }

    )


def approve_restaurant(request, id):

    email = request.session.get("email")

    if email != "shivanandshirur99@gmail.com":

        return HttpResponse("Only Admin Allowed")

    restaurant = Restaurant.objects.get(id=id)

    restaurant.approved = True

    restaurant.save()

    restaurantList = Restaurant.objects.all()

    return render(

        request,

        "delivery/show_restaurants.html",

        {

            "restaurantList": restaurantList

        }

    )


# =========================
# MENU
# =========================

def open_update_menu(request, restaurant_id):

    username = request.session.get("username")

    if not username:

        return redirect("open_signin")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    itemList = restaurant.items.all()

    return render(

        request,

        "delivery/update_menu.html",

        {

            "itemList": itemList,

            "restaurant": restaurant

        }

    )


def update_menu(request, restaurant_id):

    username = request.session.get("username")

    role = request.session.get("role")

    if not username:

        return redirect("open_signin")

    if role != "manager":

        return HttpResponse("Only Hotel Manager Allowed")

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    if request.method == 'POST':

        name = request.POST.get('name')

        description = request.POST.get('description')

        price = request.POST.get('price')

        vegeterian = request.POST.get(
            'vegeterian'
        ) == 'on'

        picture = request.POST.get('picture')

        Item.objects.create(

            restaurant=restaurant,

            name=name,

            description=description,

            price=price,

            vegeterian=vegeterian,

            picture=picture,

        )

    itemList = restaurant.items.all()

    return render(

        request,

        "delivery/update_menu.html",

        {

            "itemList": itemList,

            "restaurant": restaurant

        }

    )


def view_menu(request, restaurant_id, username):

    restaurant = Restaurant.objects.get(
        id=restaurant_id
    )

    itemList = restaurant.items.all()

    return render(

        request,

        "delivery/customer_menu.html",

        {

            "itemList": itemList,

            "restaurant": restaurant,

            "username": username

        }

    )


# =========================
# CART
# =========================
def add_to_cart(request, item_id, username):

    if "username" not in request.session:

        return redirect("open_signin")

    customer = Customer.objects.get(
        username=username
    )

    item = Item.objects.get(
        id=item_id
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    cart.items.add(item)

    return redirect(
        "show_cart",
        username=username
    )
    
def show_cart(request, username):

    if "username" not in request.session:

        return redirect("open_signin")

    customer = Customer.objects.get(
        username=username
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    itemList = cart.items.all()

    total_price = 0

    for item in itemList:

        total_price += item.price

    return render(

        request,

        "delivery/cart.html",

        {

            "cart": cart,

            "itemList": itemList,

            "total_price": total_price,

            "username": username

        }

    )
    
# =========================
# CHECKOUT
# =========================

def checkout(request, username):

    if "username" not in request.session:

        return redirect("open_signin")

    customer = Customer.objects.get(
        username=username
    )

    cart = Cart.objects.get(
        customer=customer
    )

    cart_items = cart.items.all()

    total_price = cart.total_price()

    grand_total = total_price + 40

    amount = int(grand_total * 100)

    client = razorpay.Client(

        auth=(

            settings.RAZORPAY_KEY_ID,

            settings.RAZORPAY_KEY_SECRET

        )

    )

    payment = client.order.create({

        "amount": amount,

        "currency": "INR",

        "payment_capture": "1"

    })

    return render(

        request,

        "delivery/checkout.html",

        {

            "cart": cart,

            "cart_items": cart_items,

            "total_price": total_price,

            "customer": customer,

            "payment": payment,

            "username": username,

            "razorpay_key_id": settings.RAZORPAY_KEY_ID,

            "order_id": payment["id"]

        }

    )


def orders(request, username):

    customer = get_object_or_404(

        Customer,

        username=username

    )

    cart = Cart.objects.filter(

        customer=customer

    ).first()

    cart_items = []

    total_price = 0

    if cart:

        cart_items = cart.items.all()

        total_price = cart.total_price()

    return render(

        request,

        "delivery/orders.html",

        {

            "username": username,

            "customer": customer,

            "cart_items": cart_items,

            "total_price": total_price,

        }

    )


# =========================
# AI FOOD RECOMMENDER
# =========================
def ai_recommend(request):

    if request.method == "POST":

        food = request.POST.get("food")

        taste = request.POST.get("taste")

        budget = request.POST.get("budget")

        location = request.POST.get("location") or "Current Location"

        latitude = request.POST.get("latitude")

        longitude = request.POST.get("longitude")

        prompt = f"""

You are an advanced AI Restaurant Recommendation System.

USER LIVE LOCATION:
{location}

USER PREFERENCES:
- Food craving: {food}
- Taste preference: {taste}
- Budget: ₹{budget}

Recommend the BEST nearby restaurants around the user's current live location.

STRICT FORMAT:

🍽 TOP RESTAURANTS

1. Restaurant Name
• Famous Dish
• Approx Cost
• Rating
• Distance from current location
• Estimated travel time
• Crowd level
• Best visiting time
• Ambience

2. Restaurant Name
(same format)

3. Restaurant Name
(same format)

🍴 BEST DISHES TO TRY

- dish 1
- dish 2
- dish 3

🍰 DESSERT RECOMMENDATIONS

- dessert 1
- dessert 2

🥤 DRINK PAIRINGS

- drink 1
- drink 2

💡 DINING TIPS

- tip 1
- tip 2

IMPORTANT:
- Use REALISTIC nearby restaurants based on the location.
- Keep response professional and visually beautiful.
- Do NOT mention AI limitations.
- Do NOT explain reasoning.
"""

        try:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

            )

            result = response.choices[0].message.content

        except Exception as e:

            result = f"Error: {str(e)}"

        return render(

            request,

            "delivery/ai_result.html",

            {

                "result": result,

                "location": location

            }

        )

    return render(

        request,

        "delivery/ai_form.html"

    )
    
def ai_chef(request):

    if request.method == "POST":

        dish = request.POST.get("dish")

        result = generate_recipe(dish)

        return render(

            request,

            "delivery/chef_result.html",

            {

                "result": result

            }

        )

    return render(

        request,

        "delivery/chef_form.html"

    )


# =========================
# LOGOUT
# =========================

def logout_view(request):

    request.session.flush()

    return redirect("/")