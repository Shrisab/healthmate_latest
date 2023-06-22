from django.contrib.auth.models import User

from .models import Profile
from django.forms.models import ModelForm

from django.forms.widgets import FileInput
from django import forms
from healthapp import models


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'profile_img': FileInput(),
        }


class savePost(forms.ModelForm):
    user = forms.CharField(max_length=30, label="Author")
    title = forms.CharField(max_length=250, label="Title")
    short_description = forms.Textarea()
    content = forms.Textarea()
    meta_keywords = forms.Textarea()
    banner_path = forms.ImageField(label="Banner Image")
    status = forms.CharField(max_length=2)

    class Meta():
        model = models.Post
        fields = ('user','title', 'short_description',
                  'content', 'meta_keywords', 'banner_path', 'status',)

    def clean_user(self):
        userID = self.cleaned_data['user']
        try:
            user = models.User.objects.get(id=userID)
            return user
        except:
            raise forms.ValidationError('Selected User is invalid')


# class saveComment(forms.ModelForm):
#     post = forms.CharField(max_length=30, label="Post")
#     name = forms.CharField(max_length=250, label="Name")
#     email = forms.CharField(max_length=250, label="Email")
#     subject = forms.CharField(max_length=250, label="Subject")
#     message = forms.Textarea()

#     class Meta():
#         model = models.Comment
#         fields = ('post', 'name', 'email', 'subject', 'message',)

#     def clean_post(self):
#         postID = self.cleaned_data['post']
#         try:
#             post = models.Post.objects.get(id=postID)
#             return post
#         except:
#             raise forms.ValidationError('Post ID is invalid')
