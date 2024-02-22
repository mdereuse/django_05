from django import forms


class UpdateMovieForm(forms.Form):
    title = forms.ChoiceField(required=True)
    opening_crawl = forms.CharField(required=True)

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].choices = choices
