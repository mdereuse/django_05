from django import forms


class SearchPersonForm(forms.Form):
    min_movie_release_date = forms.DateField(required=True)
    max_movie_release_date = forms.DateField(required=True)
    min_planet_diameter = forms.IntegerField(required=True)
    gender = forms.ChoiceField(required=True)

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = choices
