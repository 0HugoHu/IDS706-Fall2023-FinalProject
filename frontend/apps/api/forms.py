from wtforms import Form
from wtforms_alchemy import model_form_factory


from apps.models import *


ModelForm = model_form_factory(Form)


class BookForm(ModelForm):
    class Meta:
        model = Book

