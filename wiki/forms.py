from django.forms import ModelForm
from wiki.models import WikiPage

class EditArticleForm(ModelForm):
    class Meta:
        model = WikiPage
        fields = ['title', 'text']
        
class AddArticleForm(ModelForm):
    class Meta:
        model = WikiPage
        fields = ['url_title', 'title', 'text']
        
class DeleteForm(ModelForm):
    class Meta:
        model = WikiPage
        fields = []