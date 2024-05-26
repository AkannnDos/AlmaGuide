from django import forms
from attractions.models import Attraction


class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['similar_attractions'].queryset = Attraction.objects.exclude(pk=self.instance.pk)
