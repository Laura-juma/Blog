from django.urls import path
from .views import RegisterView, ProfileView, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, HomeView, CommentCreateView, CommentUpdateView, CommentDeleteView, posts_under_tag
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', ProfileView.as_view(), name='user_profile'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path("post/<int:pk>/comment/", CommentCreateView.as_view(), name="add_comment"),
    path("comment/<int:pk>/edit/", CommentUpdateView.as_view(), name="edit_comment"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="delete_comment"),
    path("tag/<str:name>/", posts_under_tag, name ='posts_under_tag'),
  

] 