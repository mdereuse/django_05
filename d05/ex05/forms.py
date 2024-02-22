from django import forms


class RemoveMovieForm(forms.Form):
    title = forms.ChoiceField(required=True)

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].choices = choices
