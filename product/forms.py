# https://www.youtube.com/watch?v=MBbVq_FIYDA - super().__init__()
# https://www.youtube.com/watch?v=mcAB5dBXMp4 - *args и **kwargs

from django import forms
from .models import Author, Product
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
import re

User = get_user_model()

class LoginForm(forms.ModelForm):
    # username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, max_length=16, required=True)
    class Meta:
        model = User
        fields = ("username","password")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        # print(user)

        if not user:
            raise forms.ValidationError("Username or Password is wrong")
        
        if not user.is_active:
            raise forms.ValidationError("Your account is not active")
        
        # if user.is_superuser:
        #     ...
        # elif user.is_staff:
        #     ...
        # else:
        #     ...

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].required = True

class RegisterForm(forms.ModelForm):

    # PasswordInput formasina salmaq ucun
    password = forms.CharField(widget=forms.PasswordInput, max_length=16, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, max_length=16, required=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "password_confirm", "first_name", "last_name")


    # form-control ve s. class ve xususiyyetler vermek ucun
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            # self.fields[field].required = True


    # XSS temizlik ucun
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")


        # Validatorlar ucun 
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already exists")
        
        if len(password) < 8:
            raise forms.ValidationError("Minimum length is 8 symbols")
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords dont match")
        
        return self.cleaned_data




# ================================ CUSTOM FORM ==========================================
class AuthorLoginForm(forms.Form):

    username = forms.CharField(label="İstifadəçi adı", max_length=150)
    password = forms.CharField(label="Şifrə", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"


class AuthorRegisterForm(forms.ModelForm):
    # PasswordInput formasina salmaq ucun
    password = forms.CharField(widget=forms.PasswordInput, max_length=16, required=True, label="Şifrə")
    confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=16, required=True, label="Şifrə təkrarı")
    birthday = forms.CharField(widget=forms.DateInput, required=True)
   
   # form-control ve s. class ve xususiyyetler vermek ucun
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            # self.fields[field].required = True


    class Meta:
        model=Author
        fields = ['username', 'email', 'name', 'surname','birthday', 'gender', 'image', 'bio', 'password']


    def clean_username(self):
        username = self.cleaned_data.get("username")

        if Author.objects.filter(username=username).exists():
            raise ValidationError("This username is already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if Author.objects.filter(email=email).exists():
            raise ValidationError("This e-mail is already exists")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm  = cleaned_data.get('confirm_password')

        if password != confirm:
            raise ValidationError("Passwords dont match")
        return cleaned_data


class AuthorResetChangePassword(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["confirm_password"].widget.attrs["class"] = "form-control"

    password = forms.CharField(label="Yeni sifre", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Tekrar sifre", widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()

        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")

        if p1 != p2:
            raise ValidationError("Passwords dont match!")
        if len(p1) < 8:
            raise ValidationError("Passwords must be minimum 8 simbol!")
        return cleaned_data

# ================================ CUSTOM FORM ==========================================

class ProductForm(forms.ModelForm):
    # description = forms.CharField(widget=forms.Textarea(attrs={'cols':40, 'rows':5}))

    class Meta:
        model = Product
        # fields = ("name","price",)
        # fields = "__all__"
        exclude = ("time_create", "time_update", "status", "poster")
        widgets = {
            "description": forms.Textarea(attrs={"cols": 20, "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    # Variant 1

    # def clean_name(self):
    #     name = self.cleaned_data.get("name")
    #     if name and name.startswith("a"):
    #         raise forms.ValidationError("Ad a ile baslaya bilmez!")
    #     return name

    # def clean_price(self):
    #     price = self.cleaned_data.get("price")
    #     if price is not None and price <= 0:
    #         raise forms.ValidationError("Qiymet 1den asagi ola bilmez!")
    #     return price

    # Variant 2

    def clean(self):
        # attrs = self.cleaned_data
        attrs = super().clean()
        name = attrs.get("name")
        price = attrs.get("price")

        if name.startswith("a"):
            self.add_error("name", "Ad a ile baslaya bilmez!")

        if price is not None and price < 1:
            self.add_error("price", "Qiymet 1den asagi ola bilmez!")

        return attrs

    # def clean(self):
    #     attrs = self.cleaned_data
    #     name = attrs.get("name")
    #     price = attrs.get("price")
    #     # print(name)
    #     if name.startswith("a"):
    #         raise forms.ValidationError("Ad a ile baslaya bilmez!")

    #     if price is not None and price < 1:
    #         raise forms.ValidationError("Qiymet 1den asagi ola bilmez!")
    #     return attrs

    # def save(self, commit = True):
    #     if commit:
    #         print("We are inside")
    #         return Product.objects.create(
    #             **self.cleaned_data
    #         )
    #     else:
    #         return Product(**self.cleaned_data)


# class ProductForm(forms.Form):
#     name = forms.CharField()
#     price = forms.CharField()
#     tax_price  = forms.CharField()
