from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


class CustomUserCreationForm(UserCreationForm):
  email = forms.EmailField(required = True)
  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')

class PostCreationForm(forms.ModelForm):
  tags= forms.CharField(required=False) #not tag object yet, just text from user

  class Meta:
    model = Post
    fields = ('title', 'content')

  def save(self, commit=True): #ovverride save inorder to covert tag text to object, and process if it already existed
    post = super().save(commit=False) #creates the object with title + content field, but tag is till raw text not attached to post but does not save yet, so IT IS A CONVENTIONAL METHOD
     
    if commit: #saves the post object because for tags to be attached, you need a real post object first
      post.save()
      
    tags_input = self.cleaned_data.get('tags', '')
    tag_names =[t.strip() for t in tags_input.split(',') if t.strip()]

    for name in tag_names:
      tag, created = Tag.objects.get_or_create(name=name)
      post.tags.add(tag)

    return post
  

class CommentCreationForm(forms.ModelForm):
  def validate_content(self):
    content = self.cleaned_data.get('content')
    if not content:
      raise forms.ValidationError("Content cannot be empty.")
    return content
  
  class Meta:
    model = Comment
    fields = ['content']


