from django import forms
from datetime import time
from talk.models import Talk
from schedule.models import Slot
from django.utils.translation import gettext_lazy as _

class SplitTimeWidget(forms.MultiWidget):
    """
    Widget written to split widget into hours and minutes.
    """
    def __init__(self, attrs=None):
        widgets = (forms.Select(attrs=attrs, choices=([(hour,hour) for hour in range(0,24)])),
                   forms.Select(attrs=attrs, choices=([(minute, str(minute).zfill(2)) for \
                                                           minute in [0,15,30,45]])))
        super(SplitTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.hour, value.minute]
        return [None, None]

class SplitTimeField(forms.MultiValueField):
    """
    Field written to accept two fields Hour Field and Time Field
    and combine them into TimeField.
    """
    default_error_messages = {
        'invalid_time': _(u'Enter a valid time.'),
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            forms.CharField(error_messages={'invalid': errors['invalid_time']}),
            forms.CharField(error_messages={'invalid': errors['invalid_time']}),
        )
        super(SplitTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeField has required=False).
            if data_list[0] in (None, '') or data_list[1] in (None, ''):
                raise forms.ValidationError(self.error_messages['invalid_time'])
            return time(int(data_list[0]),int(data_list[1]))
        return None


class SlotForm(forms.ModelForm):
    talk       = forms.ModelChoiceField(queryset=Talk.objects.filter(scheduled=False))
    start_time = SplitTimeField(widget=SplitTimeWidget)
    end_time   = SplitTimeField(widget=SplitTimeWidget)

    class Meta:
        model = Slot

    def clean_start_time(self):
        try:
            if self.cleaned_data['start_time'] < self.cleaned_data['day'].start_time \
                or self.cleaned_data['start_time'] > self.cleaned_data['day'].end_time:
                raise forms.ValidationError(_("Talk Time is out of bound of Conference timings."))
            return self.cleaned_data['start_time']
        except KeyError:
            raise forms.ValidationError(_("Conference day has not been set."))

    def clean_end_time(self):
        try:
            if self.cleaned_data['end_time'] <= self.cleaned_data['start_time']:
                raise forms.ValidationError(_("Talk End Time cannot be the same or lower than Talk Start Time"))
            if self.cleaned_data['end_time'] > self.cleaned_data['day'].end_time:
                raise forms.ValidationError(_("Talk End Time cannot exceed scheduled day's time."))
            return self.cleaned_data['end_time']
        except KeyError:
            return self.cleaned_data['end_time']

    def clean_hall(self):
        # ToDo: See that a speaker does not fall in two adjacent slots.
        try:
            slots = Slot.objects.all()
            for slot in slots:
                if self.cleaned_data['day'].date == slot.day.date and \
                   self.cleaned_data['hall'].name == slot.hall.name:
                    if (self.cleaned_data['start_time'] >= slot.talk_start_time and \
                        self.cleaned_data['start_time'] < slot.talk_end_time) or \
                       (self.cleaned_data['end_time'] > slot.talk_start_time and \
                        self.cleaned_data['end_time'] <= slot.talk_end_time) or \
                       (self.cleaned_data['start_time'] <= slot.talk_start_time and \
                        self.cleaned_data['end_time'] >= slot.talk_end_time):
                            raise forms.ValidationError(_("Hall already occupied."))
            return self.cleaned_data['hall']
        except KeyError:
            return self.cleaned_data['hall']

    def clean_talk(self):
        # Assumption that a talk cannot be placed more than once in
        # more than one slot. Other cases are also possible.
        try:
            slots = Slot.objects.all()
            for slot in slots:
                if self.cleaned_data['talk'].id == slot.talk.id:
                    raise forms.ValidationError(_("Talk has already been scheduled."))
            return self.cleaned_data['talk']
        except KeyError:
            return self.cleaned_data['talk']

