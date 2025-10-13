from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from django.urls import reverse_lazy
from django.contrib import messages


class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

		def save(self, commit=True):
			user = super().save(commit=False)
			user.email = self.cleaned_data['email']
			if commit:
				user.save()
			return user

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio', 'website', 'location')

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'content')
		widgets = {
			'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
			'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post here...'}),
		}

class CommentForm(forms.ModelForm):
	content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        max_length=2000,
        label=''
    )

	class Meta:
		model = Comment
		fields = ('content',)
	
		def clean_content(self):
			content = self.cleaned_data.get('content', '').strip()
			if not content:
				raise forms.ValidationError("Comment cannot be empty.")
			return content
	 
