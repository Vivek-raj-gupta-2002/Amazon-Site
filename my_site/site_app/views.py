from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Link, Collected_data, Catogery
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import forms
from django.views import View
from .Amazon import Amazon
import csv

# Create your views here.

# the Login and Logout View
@require_http_methods(['GET', 'POST'])
def login_view(request):
    
    # if the user is authenticated the redirect the user to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    message = ''
    if request.method == 'POST':# check if the request typr if POST or not

        # get the data from the form
        check_form = forms.form_login(request.POST)

        if check_form.is_valid():# check the validity of form
            message = 'Invalid Username or Password'
            # check the validity of user
            user = authenticate(username = check_form['username'].value(), password = check_form['password'].value())
            if user:
                # if the authentication is sussesfull Log the use in
                login(request, user)
                return redirect('dashboard')
    
    # sending the form for getting the username and password
    form = forms.form_login()

    # send the responce
    return render(request, 'a-login.html', {'form': form, 'action': '/login', 'message': message, 'title': 'Login'})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    # ----------------------> redirect
    return redirect('login')

# -------------------------------------------------------

# signup page
@require_http_methods(['GET', 'POST'])
def add_user_view(request):
    message = ''
    
    # if the user is authenticated the redirect the user to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form_filled = forms.sign_up_form(request.POST)
        if form_filled.is_valid():
            form_filled.save()
            return redirect('/login')
        message = 'Invalid Information'
    
    curr_form = forms.sign_up_form()
    return render(request, 'signup.html', {'form': curr_form, 'action': '/signup', 'message': message, 'title': 'Sign-Up'})

# ---------------------------------------------------------------------------------------|

# all catogeries for dashboard
@require_GET
@login_required(login_url='/login')
def show_all_cat(request):

    # get data of the user
    user_data = Catogery.objects.all().filter(user=request.user)
    data_to_render = []
    for my_data in user_data:
        number = len(Link.objects.all().filter(name=my_data))

        data_to_render.append({'name': my_data.name, 'number': str(number), 'id': my_data.id})
    
    data = {
        'data': data_to_render
    }
    return render(request, 'category-list.html', data)


# add category view 'Login  required and allowed requests get and post'
@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
def add_category_view(request):
    message = ''
    if request.method == 'POST':
        current_user = request.user
        add_form = forms.AddCategoryForm(request.POST)

        try:
            if add_form.is_valid():
                category = add_form.save(commit=False)
                category.user = current_user
                category.save()
                return redirect('dashboard')
        except:
            message = 'Invalid form data'

    form = forms.AddCategoryForm()

    return render(request, 'add-category.html', {'form': form, 'action': '/add_category', 'message': message})


# removing the catogery
@require_GET
@login_required(login_url='/login')
def remove_category_view(request, id):
    # here id is for catogery id
    try:
        entry = Catogery.objects.get(id=id, user=request.user).delete()
        return redirect('dashboard')
    except:
        return redirect('dashboard')


# -------------------------------------------------------------------------------------|

# Links

# show all the links
@require_GET
@login_required(login_url='/login')
def show_all_link(request, id):
    
    catogery_data = get_object_or_404(Catogery, id=id, user=request.user)

    get_data = Link.objects.all().filter(name=catogery_data)
    send_data = []
    for data in get_data:
        new_data = Collected_data.objects.all().filter(name=data).latest('created')
        
        send_data.append({
            'product': data,
            'now': new_data,
        })
        

    preview_data = {
        'name': catogery_data,
        'data': send_data,
    }
    
    return render(request, 'product-link.html', preview_data)


# delete a Link
@require_GET
@login_required(login_url='/login')
def del_link(request, id, cat_id):
    cat_id = str(cat_id)
    try:
        data = Link.objects.get(id=id, created_by=request.user)
        new_id = data.name.id
        data.delete()
        return redirect('/link/'+cat_id)
    
    except:
        return redirect('/link/'+cat_id)


# add new Link in the catogery
@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'])
def add_link_view(request, id):# id of catogery
    message = ''

    cat = get_object_or_404(Catogery, id=id, user=request.user)

    if request.method == 'POST':
        form_data = forms.AddLinkForm(request.POST)

        if form_data.is_valid():

            if 1:
                server = Amazon()

                soup = server.send_request(request.POST['product_link'])

                form_data = form_data.save(commit=False)
                form_data.name = cat
                form_data.created_by = request.user
                form_data.save()

                data = server.product_details(soup)

                db = Collected_data(
                    name = form_data,
                    title = data['title'],
                    rating = data['rating'],
                    review = data['review'],
                    isAvaliable = data['isAvaliable'],
                    price = data['price'],
                    mrp = data['mrp'],
                    seller = data['seller'],
                    ASIN = data['ASIN'],
                    First_date = data['First_date'],
                )

                db.save()

                
                return redirect('/link/{}'.format(id))

            else:
                message = 'Invalid Link'
            
            
    form = forms.AddLinkForm()

    return render(request, 'add-product.html', {'form': form, 'action': '/add_link/{}'.format(id), 'message': message})


@require_GET
@login_required(login_url='/login')
def alter_collection(request, link_id):
    link = get_object_or_404(Link, id=link_id, created_by=request.user)

    if link.collection:
        link.collection = 0
    else:
        link.collection = 1
    
    link.save()

    return redirect('/link/{}'.format(link.name.id))


# ----------------------------------------------------------------------|

#Collected data
@require_GET
@login_required(login_url='/login')
def collected_data_view(request, link_id):

    our_link = get_object_or_404(Link, id=link_id, created_by=request.user)
    data = Collected_data.objects.all().filter(name=our_link)

    cat_name = our_link.name

    res_data = {
        'cat_id': our_link.name.id,
        'link_id': our_link.id,
        'cat_name': cat_name,
        'data': data
    }


    return render(request, 'data.html', res_data)

@require_GET
@login_required(login_url='/login')
def del_data_view(request, id):

    data = get_object_or_404(Collected_data, id=id, created=request.user)
    
    redirect_id = data.name.id

    data.delete()
    return redirect('/data/{}'.format(redirect_id))


@require_GET
@login_required(login_url='/login')
def download_view(request, id):
    our_id = get_object_or_404(Link, id=id, created_by=request.user)
    data = Collected_data.objects.all().filter(name=our_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Rating', 'Review', 'isAvaliable', 'Price', 'MRP', 'Seller', 'ASIN', 'FirstDate'])

    for i in data:
        writer.writerow([i.title, i.rating, i.review, i.isAvaliable, i.price, i.mrp, i.seller, i.ASIN, i.First_date])

    return response
