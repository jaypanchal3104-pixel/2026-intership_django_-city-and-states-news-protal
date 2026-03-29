from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from core.models import News, Category, State, City, Comment
from .forms import NewsForm
from dashboard.decorators import role_required
from django.contrib.auth.decorators import login_required


# ─────────────────────────────────────────────
#  PUBLIC — NEWS LIST
# ─────────────────────────────────────────────
def newsListView(request):
    news_list  = News.objects.filter(status='published').order_by('-publish_date', '-created_at')
    categories = Category.objects.all()
    states     = State.objects.all()
    cities     = City.objects.all()

    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        news_list = news_list.filter(category__category_id=category_id)

    # State filter
    state_id = request.GET.get('state')
    if state_id:
        news_list = news_list.filter(city__state__state_id=state_id)
        cities    = City.objects.filter(state__state_id=state_id)

    # City filter
    city_id = request.GET.get('city')
    if city_id:
        news_list = news_list.filter(city__city_id=city_id)

    # Search
    query = request.GET.get('q')
    if query:
        news_list = news_list.filter(title__icontains=query)

    return render(request, 'news/news_list.html', {
        'news_list':  news_list,
        'categories': categories,
        'states':     states,
        'cities':     cities,
        'query':      query,
    })


# ─────────────────────────────────────────────
#  PUBLIC — NEWS DETAIL
# ─────────────────────────────────────────────
def newsDetailView(request, pk):
    if request.user.is_authenticated and request.user.role in ['admin', 'journalist']:
        news = get_object_or_404(News, news_id=pk)
    else:
        news = get_object_or_404(News, news_id=pk, status='published')

    news.views += 1
    news.save(update_fields=['views'])

    related_news = News.objects.filter(
        category=news.category,
        status='published'
    ).exclude(news_id=pk)[:4]

    comments = news.comments.filter(is_active=True)

    # Bookmark check
    is_bookmarked = False
    if request.user.is_authenticated:
        from core.models import Bookmark
        is_bookmarked = Bookmark.objects.filter(
            user=request.user, news=news
        ).exists()

    return render(request, 'news/news_detail.html', {
        'news':          news,
        'related_news':  related_news,
        'comments':      comments,
        'is_bookmarked': is_bookmarked,
    })


# ─────────────────────────────────────────────
#  JOURNALIST / ADMIN — CREATE NEWS
# ─────────────────────────────────────────────
@role_required(allowed_roles=['journalist', 'admin'])
def newsCreateView(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            news            = form.save(commit=False)
            news.journalist = request.user
            if news.status == 'published':
                news.publish_date = timezone.now().date()
            news.save()
            return redirect('news_detail', pk=news.news_id)
    else:
        form = NewsForm(user=request.user)

    categories = Category.objects.all()
    states     = State.objects.all()
    cities     = City.objects.all()

    return render(request, 'news/news_form.html', {
        'form':       form,
        'title':      'Submit New Article',
        'categories': categories,
        'states':     states,
        'cities':     cities,
    })


# ─────────────────────────────────────────────
#  JOURNALIST / ADMIN — EDIT NEWS
# ─────────────────────────────────────────────
@role_required(allowed_roles=['journalist', 'admin'])
def newsEditView(request, pk):
    news = get_object_or_404(News, news_id=pk)

    if request.user.role == 'journalist' and news.journalist != request.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news, user=request.user)
        if form.is_valid():
            news = form.save(commit=False)
            if news.status == 'published' and not news.publish_date:
                news.publish_date = timezone.now().date()
            news.save()
            return redirect('news_detail', pk=news.news_id)
    else:
        form = NewsForm(instance=news, user=request.user)

    categories = Category.objects.all()
    states     = State.objects.all()
    cities     = City.objects.all()

    return render(request, 'news/news_form.html', {
        'form':       form,
        'news':       news,
        'title':      'Edit Article',
        'categories': categories,
        'states':     states,
        'cities':     cities,
    })


# ─────────────────────────────────────────────
#  JOURNALIST / ADMIN — DELETE NEWS
# ─────────────────────────────────────────────
@role_required(allowed_roles=['journalist', 'admin'])
def newsDeleteView(request, pk):
    news = get_object_or_404(News, news_id=pk)

    if request.user.role == 'journalist' and news.journalist != request.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        news.delete()
        return redirect('news_list')

    return render(request, 'news/news_delete.html', {'news': news})


# ─────────────────────────────────────────────
#  ADMIN — APPROVE NEWS
# ─────────────────────────────────────────────
@role_required(allowed_roles=['admin'])
def newsApproveView(request, pk):
    news              = get_object_or_404(News, news_id=pk)
    news.status       = 'published'
    news.publish_date = timezone.now().date()
    news.save()
    return redirect('admin_dashboard')


# ─────────────────────────────────────────────
#  ADMIN — REJECT NEWS
# ─────────────────────────────────────────────
@role_required(allowed_roles=['admin'])
def newsRejectView(request, pk):
    news        = get_object_or_404(News, news_id=pk)
    news.status = 'rejected'
    news.save()
    return redirect('admin_dashboard')


# ─────────────────────────────────────────────
#  ADD COMMENT
# ─────────────────────────────────────────────
@login_required
def addCommentView(request, pk):
    news = get_object_or_404(News, news_id=pk)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                news=news,
                user=request.user,
                content=content,
            )
    return redirect('news_detail', pk=pk)