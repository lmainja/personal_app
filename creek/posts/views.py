from django.shortcuts import render, redirect
from .models import Post, Comment
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'posts/home1.html', context)

def about(request):
    return render(request, 'posts/about1.html', {'title': 'About'})


def coming_soon(request):
    return render(request, 'posts/coming_soon.html')

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'posts/detail.html'

class PostListView(ListView):
    model = Post
    template_name = 'posts/home1.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'posts/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def add_comment(request, pk):
    if request.method == "POST":
            form = CommentForm(request.POST)
            post = get_object_or_404(Post, pk=pk)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('posts:detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/comments.html', {'form': form})

