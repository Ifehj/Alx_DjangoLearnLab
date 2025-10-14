from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag
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

	tags = forms.CharField(
		required=False,
		help_text="Enter comma-separated tags (e.g. django, python)",
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'})
	)
	class Meta:
		model = Post
		fields = ('title', 'content')
		widgets = {
			'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
			'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your post here...'}),
		}
	
	def __init__(self, *args, **kwargs):
        # if instance provided, pre-populate tags field
		super().__init__(*args, **kwargs)
		if self.instance and self.instance.pk:
			tag_names = ', '.join(t.name for t in self.instance.tags.all())
			self.fields['tags'].initial = tag_names

	def clean_tags(self):
		value = self.cleaned_data.get('tags', '')
        # normalize: split by comma, strip whitespace, remove empties, lowercase optional
		tag_names = [t.strip() for t in value.split(',') if t.strip()]
        # deduplicate while preserving order
		seen = set()
		uniq = []
		for name in tag_names:
			lname = name
			if lname not in seen:
				seen.add(lname)
				uniq.append(name)
				return uniq  # return list of tag names
	
	def save(self, commit=True):
		tag_names = self.cleaned_data.pop('tags', [])
		post = super().save(commit=commit)
        # attach tags (create missing ones)
        # if commit=False we still attach after final save; here commit True by default
		post.tags.clear()
		for name in tag_names:
			tag_obj, _ = Tag.objects.get_or_create(name=name)
			post.tags.add(tag_obj)
		return post
	
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
	 
