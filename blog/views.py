from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db.models import Q
from .models import Post, Category
from django.views import View, generic

# Create your views here.


class BlogHomeView(generic.ListView):
    model = Post
    paginate_by = 6
    context_object_name = 'blog_list'
    template_name = 'blog/home.html'

    def get_queryset(self):
        qs = Post.objects.filter(active=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_post = Post.objects.filter(
            active=True).order_by('-created_at')[:3]
        category_list = Category.objects.all()
        context['title'] = 'Our Blog'
        context['recent_post'] = recent_post
        context['category_list'] = category_list
        context['blogactive'] = 'active'
        return context


class CategoryPostView(generic.ListView):
    model = Post
    paginate_by = 6
    context_object_name = 'blog_list'
    template_name = 'blog/home.html'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        qs = Post.objects.filter(active=True, category__id=category_id)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_post = Post.objects.filter(
            active=True).order_by('-created_at')[:3]
        category_list = Category.objects.all()
        context['title'] = 'Our Blog'
        context['recent_post'] = recent_post
        context['category_list'] = category_list
        return context


class SignlePostView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/single_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_post = Post.objects.filter(
            active=True).order_by('-created_at')[:3]
        category_list = Category.objects.all()
        context['recent_post'] = recent_post
        context['category_list'] = category_list
        context['title'] = self.object.title
        return context


class SearchPostView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')

        blog_list = Post.objects.filter(active=True)

        if q:
            q = q.strip()
            blog_list = blog_list.filter(Q(title__icontains=q) | Q(
                description__icontains=q) | Q(category__name__icontains=q))

        recent_post = Post.objects.filter(
            active=True).order_by('-created_at')[:3]
        category_list = Category.objects.all()

        context = {'blog_list': blog_list,
                   'recent_post': recent_post, 'category_list': category_list, 'title': 'Search Result'}
        return render(request, "blog/home.html", context)
