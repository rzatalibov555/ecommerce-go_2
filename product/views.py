from django.http import HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import (
    F,
    FloatField,
    DecimalField,
    ExpressionWrapper,
    Count,
)
from django.db.models.functions import Coalesce, Round
from product.forms import ProductForm
from product.models import *
from urllib.parse import urlencode

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
