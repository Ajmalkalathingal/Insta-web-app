from django import forms
from .models import Post,Comments

class NewPost(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget= forms.TextInput(attrs={'class':'input','placeholder':'Caption'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'input', 'placeholder':'Type tags with spaces'}))

    class Meta:
        model = Post
        fields = ['picture','caption','tags']


# comment form
class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': 65, 'rows': 2}))

    class Meta:
        model = Comments
        fields = ['comment']
        
