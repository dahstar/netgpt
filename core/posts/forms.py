from django import forms
from .models import Profile,Reply,Post
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']  # Add more fields as needed

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'id': 'id_content'}),
        }
