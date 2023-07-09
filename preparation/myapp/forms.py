from django import forms
from myapp.models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model=Vehicle
        fields='__all__'
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "number":forms.TextInput(attrs={"class":"form-control"}),
            "fueltype":forms.TextInput(attrs={"class":"form-control"}),
            "wheel":forms.TextInput(attrs={"class":"form-control"}),
            "color":forms.TextInput(attrs={"class":"form-control"})
        }