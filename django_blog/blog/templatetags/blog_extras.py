from django import template
from django.db.models import Count

from ..models import Post, Tag

register = template.Library()


@register.simple_tag
def latest_posts(count=6):
  return Post.objects.select_related('author').prefetch_related('tags').order_by('-published_date')[:count]


@register.simple_tag
def post_image(post, width=800, height=533):
  # Posts have no image field yet, so each post gets a stable placeholder photo
  seed = post.pk if post else 'blog'
  return f"https://picsum.photos/seed/djblog-{seed}/{width}/{height}"


@register.inclusion_tag('blog/_sidebar.html', takes_context=True)
def blog_sidebar(context):
  return {
    'user': context.get('user'),
    'recent_posts': Post.objects.order_by('-published_date')[:4],
    'tags': Tag.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count', 'name')[:12],
  }
