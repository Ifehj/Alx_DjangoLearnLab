from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, PostForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Post
from django.contrib.auth import login
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy



# Create your views here.

def home(request):
    return render(request, 'blog/home.html')

def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			Profile.objects.get_or_create(user=user)
			login(request, user)
			messages.success(request, "Registration successful. You're now logged in.")
			return redirect('home')
		else:
			messages.error(request, "Please correct the errors below.")
	else:
		form = CustomUserCreationForm()
	return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
	profile, _ = Profile.objects.get_or_create(user=request.user)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			new_email = request.POST.get('email', '').strip()
			if new_email and new_email != request.user.email:
				request.user.email = new_email
				request.user.save()
			messages.success(request, "Profile updated successfully.")
			return redirect('profile')
		else:
			messages.error(request, "Please correct the errors below.")
	else:
		form = ProfileForm(instance=profile)
	return render(request, 'blog/profile.html', {'form': form})

# POST VIEWS

class PostListView(generic.ListView):
	model = Post
	template_name = 'blog/post_list.html'
	context_object_name = 'posts'
	ordering = ['-created_at']
	paginate_by = 10

class PostDetailView(generic.DetailView):
	model = Post
	template_name = 'blog/post_detail.html'
	content_object_name = 'post'

class PostCreateView(LoginRequiredMixin, generic.CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		messages.success(self.request, "Post created successfully.")
		return super().form_valid(form)
	
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # ensure author remains unchanged
        form.instance.author = self.request.user
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts-list')

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
	
	
