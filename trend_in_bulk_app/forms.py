from django import forms

from .models import Blog, Category, Product, TeamMember, Testimonial, WholesaleSeller


class WholesaleSellerForm(forms.ModelForm):
    class Meta:
        model = WholesaleSeller
        fields = ["name", "email", "phone", "address"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "image"]





class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["category", "seller", "name", "description", "price_per_unit", "unit", "stock", "image"]


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "slug", "image", "content"]


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "designation", "message", "rating", "image"]


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "designation", "image", "facebook", "instagram", "twitter", "linkedin"]
