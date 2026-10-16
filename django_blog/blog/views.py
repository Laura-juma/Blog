from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView
from .forms import CustomUserCreationForm, PostCreationForm, CommentCreationForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Comment, Tag
from django.db.models import Q

class RegisterView(CreateView):
  form_class = CustomUserCreationForm
  success_url = reverse_lazy('login')
  template_name = 'blog/registration.html'

  def form_valid(self, form): #override form valid in order to show message
    response = super().form_valid(form)
    messages.success(self.request, "Account created successfully!")
    return response

class ProfileView(LoginRequiredMixin, View):
  def get(self, request):
    return render(request, 'blog/profile.html', {'user' : request.user})
  
  def post(self, request):
    user = self.request.user
    user.username = request.POST.get('username')
    user.email = request.POST.get('email')
    user.save()
    return redirect('user_profile')

class PostListView(ListView):
  model = Post
  template_name = 'blog/postlist.html'
  context_object_name = 'posts'  

  def get_queryset(self):
     query = self.request.GET.get('q')

     if query:
        return Post.objects.filter(
           Q(title__icontains=query)|
           Q(content__icontains=query)|
           Q(tags__name__icontains=query)

        ).distinct()
     
     return Post.objects.all()
    

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/postdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all()
        context["form"] = CommentCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = CommentCreationForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()

        return redirect(self.object.get_absolute_url())

class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  form_class = PostCreationForm
  template_name = 'blog/postcreate.html'
  success_url = reverse_lazy('post_list')

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
  model = Post
  form_class = PostCreationForm
  template_name = 'blog/postupdate.html'

  def test_func(self):
    post = self.get_object()
    return post.author == self.request.user

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)
  
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'blog/postdelete.html'
  success_url = reverse_lazy('post_list')

  def test_func(self):
    post = self.get_object()
    return post.author == self.request.user

class HomeView(TemplateView):
  template_name = 'blog/home.html'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreationForm

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs["pk"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentCreationForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()

def posts_under_tag(request, name):
   tag = get_object_or_404(Tag, name=name)
   posts = tag.posts.all()

   return render(request, 'blog/posts_under_tag.html', {
      "tag" : tag,
      "posts" : posts
   })
   


      

  