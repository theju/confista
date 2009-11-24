from django import forms
from talk.models import Talk
from django.contrib.auth.models import User

class TalkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TalkForm, self).__init__(*args, **kwargs)
        self.fields['speakers'].queryset = User.objects.exclude(id = self.user.id)
        self.fields['speakers'].label = "Co-Speakers"

    def save(self, commit = True):
        speakers = self.cleaned_data['speakers']
        if speakers:
            self.cleaned_data['speakers'] = speakers | User.objects.filter(id=self.user.id)
        else:
            self.cleaned_data['speakers'] = User.objects.none() | User.objects.filter(id=self.user.id)
        return super(TalkForm, self).save(commit = commit)

    class Meta:
        model = Talk
        exclude = ['accepted', 'scheduled']
