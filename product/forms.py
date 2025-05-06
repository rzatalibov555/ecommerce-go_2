from django import forms
from .models import Product

# https://www.youtube.com/watch?v=MBbVq_FIYDA - super().__init__()
# https://www.youtube.com/watch?v=mcAB5dBXMp4 - *args и **kwargs


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
