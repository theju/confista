from django import forms
from django.db.models import ObjectDoesNotExist
from delegate.models import Delegate_Profile, Location

LOCATION_NOT_FOUND_MSG = """Location not found? Add one in the above input box."""
EMPTY_VALUES = (None, '')

class LocationField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.ModelChoiceField(Location.objects.all()), forms.CharField)
        kwargs['widget'].widgets[0].choices = fields[0].choices
        super(LocationField, self).__init__(fields = fields, *args, **kwargs)

    def clean(self, value):
        if (value[0] in EMPTY_VALUES and value[1] in EMPTY_VALUES) or (value[0] and value[1]):
            raise forms.ValidationError("Either location fields must be filled.")
        if value[1]:
            try:
                location = Location.objects.get(name=value[1])
            except ObjectDoesNotExist:
                location, _ = Location.objects.get_or_create(name=value[1])
        if value[0]:
            location = Location.objects.get(id=value[0])
        return location

class LocationWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
            forms.Select(attrs=attrs), 
            forms.TextInput(attrs=attrs),
            )
        super(LocationWidget, self).__init__(widgets, attrs=attrs)

    def decompress(self, value):
        if value:
            return [value, None]
        return [None, None]

class DelegateProfileForm(forms.ModelForm):
    location = LocationField(widget=LocationWidget(), help_text=LOCATION_NOT_FOUND_MSG)

    class Meta:
        model = Delegate_Profile
        exclude = ('user',)
