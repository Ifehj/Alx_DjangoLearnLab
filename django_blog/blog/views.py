from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q

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

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['comment_form'] = CommentForm()
		return ctx

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
	
	
class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # used if user visits create page directly

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Your comment has been posted.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()  # redirects to post detail

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        # redirect back to post detail after deletion
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

class PostByTagListView(generic.ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag_name'] = self.kwargs.get('tag_name')
        return ctx

# Search view
class PostSearchView(generic.ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if not q:
            return Post.objects.none()
        # search title, content, and tag name
        return Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx

