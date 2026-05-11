from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BlogForm, CategoryForm, ProductForm, TeamMemberForm, TestimonialForm, WholesaleSellerForm
from .models import Blog, Category, ContactMessage, Product, TeamMember, Testimonial, WholesaleSeller


def _admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect("admin_login")
        return view_func(request, *args, **kwargs)

    return wrapper


# Frontend views

def home(request):
    return render(request, "frontend/index.html", {
        "testimonials": Testimonial.objects.all()[:6],
        "blogs": Blog.objects.all()[:4],
    })


def about(request):
    return render(request, "frontend/about.html", {
        "team": TeamMember.objects.all()[:4],
    })


def services(request):
    return render(request, "frontend/services.html", {
        "testimonials": Testimonial.objects.all(),
    })


def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")


        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, "Your message has been sent successfully! We will get back to you soon.")
        return redirect("contact")

    return render(request, "frontend/contact.html")



def testimonials(request):
    return render(request, "frontend/testimonials.html", {
        "testimonials": Testimonial.objects.all(),
    })


def pricing(request):
    return render(request, "frontend/pricing.html")


def faqs(request):
    return render(request, "frontend/faqs.html")


def products(request):
    categories = Category.objects.all()
    return render(request, "frontend/products.html", {"categories": categories})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, "frontend/category_products.html", {"category": category, "products": products})


def product_single(request):
    return render(request, "frontend/product-single.html")


def blog(request):
    return render(request, "frontend/blog.html", {
        "blogs": Blog.objects.all(),
    })


def blog_single(request, slug="default"):
    blog_obj = get_object_or_404(Blog, slug=slug)
    return render(request, "frontend/blog-single.html", {
        "blog": blog_obj,
    })


def team(request):
    return render(request, "frontend/team.html", {
        "team": TeamMember.objects.all(),
    })


def team_single(request):
    return render(request, "frontend/team-single.html")


def image_gallery(request):
    return render(request, "frontend/image-gallery.html")


def video_gallery(request):
    return render(request, "frontend/video-gallery.html")


def service_single(request):
    return render(request, "frontend/service-single.html")


# Admin auth

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        messages.error(request, "Invalid credentials or insufficient permissions.")

    return render(request, "authenticate/login.html")


@_admin_required
def admin_logout(request):
    logout(request)
    return redirect("admin_login")


@_admin_required
def admin_dashboard(request):
    now = timezone.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    stats = {
        "total_sellers": WholesaleSeller.objects.count(),
        "total_products": Product.objects.count(),
        "total_blogs": Blog.objects.count(),
        "total_testimonials": Testimonial.objects.count(),
        "sellers_this_month": WholesaleSeller.objects.filter(created_at__gte=month_start).count(),
        "products_this_month": Product.objects.filter(created_at__gte=month_start).count(),
    }
    return render(
        request,
        "admin_pages/dashboard.html",
        {
            "stats": stats,
            "recent_sellers": WholesaleSeller.objects.order_by("-created_at")[:5],
            "recent_products": Product.objects.select_related("seller").order_by("-created_at")[:5],
            "recent_blogs": Blog.objects.order_by("-created_at")[:5],
        },
    )


# Category CRUD

@_admin_required
def category_list(request):
    categories_qs = Category.objects.all().order_by("-created_at")
    paginator = Paginator(categories_qs, 10)
    page_number = request.GET.get("page")
    categories = paginator.get_page(page_number)
    return render(request, "admin_pages/category_list.html", {"categories": categories})


@_admin_required
def category_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        image = request.FILES.get("image")
        if name:
            Category.objects.create(
                name=name,
                description=description,
                image=image
            )
            messages.success(request, "Category created successfully!")
            return redirect("category_list")
    return render(request, "admin_pages/add_category.html")


@_admin_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.description = request.POST.get("description", "")
        if request.FILES.get("image"):
            category.image = request.FILES.get("image")
        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect("category_list")
    return redirect("category_list")




@_admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("category_list")
    return redirect("category_list")


# Sellers CRUD

@_admin_required
def seller_list(request):
    return render(request, "admin_pages/seller_list.html", {"sellers": WholesaleSeller.objects.all()})


@_admin_required
def seller_create(request):
    form = WholesaleSellerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Seller added successfully.")
    return redirect("seller_list")


@_admin_required
def seller_update(request, pk):
    seller = get_object_or_404(WholesaleSeller, pk=pk)
    form = WholesaleSellerForm(request.POST or None, instance=seller)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Seller updated successfully.")
    return redirect("seller_list")


@_admin_required
def seller_delete(request, pk):
    seller = get_object_or_404(WholesaleSeller, pk=pk)
    if request.method == "POST":
        seller.delete()
        messages.success(request, "Seller deleted.")
    return redirect("seller_list")


# Products CRUD

@_admin_required
def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.select_related("seller", "category").all()
    
    if category_id:
        products = products.filter(category_id=category_id)
        
    return render(
        request,
        "admin_pages/product_list.html",
        {
            "products": products,
            "sellers": WholesaleSeller.objects.all(),
            "categories": Category.objects.all(),
            "unit_choices": Product.UNIT_CHOICES,
            "selected_category": category_id,
        },
    )


@_admin_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product added successfully.")
    return redirect("product_list")


@_admin_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Product updated successfully.")
    return redirect("product_list")


@_admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
    return redirect("product_list")


# Blogs CRUD

@_admin_required
def blog_list(request):
    return render(request, "admin_pages/blog_list.html", {"blogs": Blog.objects.all()})


@_admin_required
def blog_create(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Blog created.")
    return redirect("blog_list")


@_admin_required
def blog_update(request, pk):
    blog_obj = get_object_or_404(Blog, pk=pk)
    form = BlogForm(request.POST or None, request.FILES or None, instance=blog_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Blog updated.")
    return redirect("blog_list")


@_admin_required
def blog_delete(request, pk):
    blog_obj = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog_obj.delete()
        messages.success(request, "Blog deleted.")
    return redirect("blog_list")


# Testimonials CRUD

@_admin_required
def testimonial_list(request):
    return render(request, "admin_pages/testimonial_list.html", {"testimonials": Testimonial.objects.all()})


@_admin_required
def testimonial_create(request):
    form = TestimonialForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Testimonial added.")
    return redirect("testimonial_list")


@_admin_required
def testimonial_update(request, pk):
    testimonial_obj = get_object_or_404(Testimonial, pk=pk)
    form = TestimonialForm(request.POST or None, request.FILES or None, instance=testimonial_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Testimonial updated.")
    return redirect("testimonial_list")


@_admin_required
def testimonial_delete(request, pk):
    testimonial_obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial_obj.delete()
        messages.success(request, "Testimonial deleted.")
    return redirect("testimonial_list")


# Contact Messages CRUD

@_admin_required
def contact_list(request):
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    contacts = ContactMessage.objects.all().order_by("-created_at")
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "admin_pages/contact_list.html", {"contacts": page_obj})


@_admin_required
def contact_delete(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        contact.delete()
        messages.success(request, "Message deleted.")
    return redirect("contact_list")


# Team Members CRUD

@_admin_required
def team_list(request):
    return render(request, "admin_pages/team_list.html", {"team_members": TeamMember.objects.all()})


@_admin_required
def team_create(request):
    form = TeamMemberForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Team member added successfully.")
    return redirect("team_list")


@_admin_required
def team_update(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    form = TeamMemberForm(request.POST or None, request.FILES or None, instance=member)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Team member updated successfully.")
    return redirect("team_list")


@_admin_required
def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == "POST":
        member.delete()
        messages.success(request, "Team member deleted.")
    return redirect("team_list")


def page_not_found(request, exception=None):
    return render(request, "404.html", status=404)
