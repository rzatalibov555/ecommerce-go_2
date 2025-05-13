
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import (F, FloatField, DecimalField, ExpressionWrapper, Count)
from django.db.models.functions import Coalesce, Round
from product.forms import LoginForm, RegisterForm, ProductForm
from product.models import *
from urllib.parse import urlencode
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from product.forms import AuthorLoginForm

# User model uzerinden Start
def login_view(request):

    if request.user.is_authenticated:
        messages.info(request,"You are logged in.")
        return redirect(reverse("product:index"))


    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            # print(user)
            login(request, user)
            return redirect('/')
            
        else:
            print(form.errors)


    context = {
        "form":form
    }    

    return render(request, "product/login.html", context)


def logout_view(request):
    logout(request)

    if not request.user.is_authenticated:
        messages.info(request,"You are successfully logout.")
        return redirect(reverse("product:index"))
    return redirect("/")


def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            
            new_user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            new_user.set_password(password)
            new_user.is_staff = True
            new_user.save()

            login(request, new_user)
            return redirect("/")
            

        else:
            print(form.errors)



    context = {
        "form" : form
    }

    return render(request, "product/register.html", context)
# User model uzerinden End



# Author model uzerinden Start
def a_login_view(request):
     
    if request.session.get("author_id"):
        messages.error(request, "Diqqət! Siz artıq login olmusuz. Əvvəlcə profildən çıxın.")
        return redirect("product:index")

    form = AuthorLoginForm(request.POST or None)
     
    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                author = Author.objects.get(username=username)
                
                if author.a_check_password(password):
                    request.session["author_id"] = author.id
                    print(request.session["author_id"])
                    return redirect('/')
                else:
                    messages.error(request, "İstifadəçi adı və ya şifrə yalnışdır.")

            except Author.DoesNotExist:
                messages.error(request, "Belə istifadəçi tapılmadı.")
                
        else:
            messages.error(request, "Xəta! Yenidən cəhd edin!")

    context = {
        "form":form
    }    

    return render(request, "product/a_login.html", context)


def a_logout_view(request):
    if "author_id" in request.session:
        del request.session["author_id"]
        messages.info(request, "Ehh! Səni yenə gözləyəcəyəm. Tez qayıt! :(")
    else:
        messages.info(request, "Xeta!")
    return redirect("/")




def a_register_view(request):
    ...

def a_change_password_view(request):
    ...

# Author model uzerinden End

def index(request):
    products_qs = Product.objects.annotate(
        tax_value=Coalesce(F("tax_price"), 0.00, output_field=DecimalField()),
        discount_value=Coalesce(
            F("discount"), 0.00, output_field=DecimalField()
        ),
    ).annotate(
        final_price=Round(
            ExpressionWrapper(
                F("price") * (1.00 - F("discount_value") / 100.00)
                + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
        total_price=Round(
            ExpressionWrapper(
                F("price") + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
    )

    categories = Category.objects.annotate(
        product_count=Count("products")
    ).order_by("-created_at")

    context = {
        "page_title": "Home",
        "products": products_qs[:12],
        "categories": categories[:12],
        "discount_products": products_qs.filter(discount_value__gt=0),
        "last_products": products_qs.order_by("-id")[:5],
    }

    return render(request, "product/index.html", context)


def home(request):
    return redirect(reverse("product:index"), permanent=True)


def product_list(request):
    products_qs = Product.objects.annotate(
        tax_value=Coalesce(F("tax_price"), 0.00, output_field=DecimalField()),
        discount_value=Coalesce(
            F("discount"), 0.00, output_field=DecimalField()
        ),
    ).annotate(
        final_price=Round(
            ExpressionWrapper(
                F("price") * (1.00 - F("discount_value") / 100.00)
                + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
        total_price=Round(
            ExpressionWrapper(
                F("price") + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
    )

    categories = Category.objects.annotate(
        product_count=Count("products")
    ).order_by("-created_at")

    context = {
        "page_title": "Products",
        "products": products_qs,
        "categories": categories[:12],
    }

    return render(request, "product/products.html", context)


def product_detail(request, product_id):
    product_qs = Product.objects.annotate(
        tax_value=Coalesce(F("tax_price"), 0.00, output_field=DecimalField()),
        discount_value=Coalesce(
            F("discount"), 0.00, output_field=DecimalField()
        ),
    ).annotate(
        final_price=Round(
            ExpressionWrapper(
                F("price") * (1.00 - F("discount_value") / 100.00)
                + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
        total_price=Round(
            ExpressionWrapper(
                F("price") + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
    )

    single_product = product_qs.get(id=product_id)

    product_tags = single_product.tags.all()

    if product_tags.exists():
        related_products = (
            product_qs.filter(tags__in=product_tags)
            .exclude(id=single_product.id)
            .order_by("-created_at")[:4]
        )
    else:
        related_products = product_qs.filter(
            category=single_product.category
        ).order_by("-created_at")[:4]

    context = {
        "page_title": "Product Detail",
        "product": single_product,
        "related_products": related_products,
    }

    return render(request, "product/product_detail.html", context)


def product_add(request):
    context = {}
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(data=request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect("product:index")
        else:
            print(form.errors)
    else:
        form = ProductForm()

    context["form"] = form
    context["page_title"] = "Product Add"

    return render(request, "product/product_add.html", context)


def category_list(request):
    categories = Category.objects.annotate(
        product_count=Count("products")
    ).order_by("-created_at")

    context = {
        "page_title": "Categories",
        "categories": categories[:12],
    }

    return render(request, "product/category.html", context)


def category_products(request, category_id):
    
    category = get_object_or_404(Category, id=category_id)
    
    # try:
    #     category = Category.objects.get(id=category_id) 
    # except:
    #     raise Http404()

    categories = Category.objects.annotate(
        product_count=Count("products")
    ).order_by("-created_at")

    products_qs = Product.objects.annotate(
        tax_value=Coalesce(F("tax_price"), 0.00, output_field=DecimalField()),
        discount_value=Coalesce(
            F("discount"), 0.00, output_field=DecimalField()
        ),
    ).annotate(
        final_price=Round(
            ExpressionWrapper(
                F("price") * (1.00 - F("discount_value") / 100.00)
                + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
        total_price=Round(
            ExpressionWrapper(
                F("price") + F("tax_value"),
                output_field=DecimalField(),
            ),
            2,
            output_field=FloatField(),
        ),
    )

    # pagination ucun start
    filtered_products = products_qs.filter(category=category_id)
    paginator = Paginator(filtered_products, 10)
    page = request.GET.get('page', 1)

    try:
        page_c = paginator.page(page)
    except PageNotAnInteger:
        page_c = paginator.page(1)
    except EmptyPage:
        page_c = paginator.page(paginator.num_pages)
    # pagination ucun end
    

    querydict = request.GET.copy()
    querydict.pop('page', None)  # 'page' varsa, sil
    base_query = querydict.urlencode()


    context = {
        "page_title": "Category Products",
        "products"  : page_c.object_list,
        "category"  : category,
        "categories": categories,
        
        # pagination ucun start
        "paginator" : paginator,
        "page_c"    : page_c,
        "base_query": base_query,
        # pagination ucun end
    }

    return render(request, "product/category_products.html", context)


def page_not_found(request, exception):
    return HttpResponseNotFound("UPSSS! Sehife tapilmadi")
