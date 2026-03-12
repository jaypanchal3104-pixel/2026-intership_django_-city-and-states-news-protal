from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.models import News, Category, State, City
from .forms import NewsForm
from dashboard.decorators import role_required


# ─────────────────────────────────────────────
#  PUBLIC — NEWS LIST
#  URL: /news/
# ─────────────────────────────────────────────
def newsListView(request):
    news_list  = News.objects.filter(status='published').order_by('-publish_date')
    categories = Category.objects.all()
    states     = State.objects.all()

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        news_list = news_list.filter(category__slug=category_slug)

    # Filter by state
    state_slug = request.GET.get('state')
    if state_slug:
        news_list = news_list.filter(state__slug=state_slug)

    # Search
    query = request.GET.get('q')
    if query:
        news_list = news_list.filter(title__icontains=query)

    return render(request, 'news/news_list.html', {
        'news_list':  news_list,
        'categories': categories,
        'states':     states,
        'query':      query,
    })


# ─────────────────────────────────────────────
#  PUBLIC — NEWS DETAIL
#  URL: /news/<id>/
# ─────────────────────────────────────────────
def newsDetailView(request, pk):
    news = get_object_or_404(News, pk=pk, status='published')

    # View count
    news.views += 1
    news.save(update_fields=['views'])

    related_news = News.objects.filter(
        category=news.category,
        status='published'
    ).exclude(pk=pk)[:4]

    return render(request, 'news/news_detail.html', {
        'news':         news,
        'related_news': related_news,
    })


# ─────────────────────────────────────────────
#  JOURNALIST — CREATE NEWS
#  URL: /news/create/
# ─────────────────────────────────────────────
@role_required(allowed_roles=['journalist', 'admin'])
def newsCreateView(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            news        = form.save(commit=False)
            news.author = request.user
            if news.status == 'published':
                news.publish_date = timezone.now()
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(user=request.user)

    return render(request, 'news/news_form.html', {
        'form':  form,
        'title': 'Submit New Article',
    })


# ─────────────────────────────────────────────
#  JOURNALIST / ADMIN — EDIT NEWS
#  URL: /news/<id>/edit/
# ─────────────────────────────────────────────
@role_required(allowed_roles=['journalist', 'admin'])
def newsEditView(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Journalist fakt potani j news edit kari shake
    if request.user.role == 'journalist' and news.author != request.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news, user=request.user)
        if form.is_valid():
            news = form.save(commit=False)
            if news.status == 'published' and not news.publish_date:
                news.publish_date = timezone.now()
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news, user=request.user)

    return render(request, 'news/news_form.html', {
        'form':  form,
        'news':  news,
        'title': 'Edit Article',
    })


# ─────────────────────────────────────────────
#  JOURNALIST / ADMIN — DELETE NEWS
#  URL: /news/<id>/delete/
# ─────────────────────────────────────────────
@role_required(allowed_roles=['journalist', 'admin'])
def newsDeleteView(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Journalist fakt potani j news delete kari shake
    if request.user.role == 'journalist' and news.author != request.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        news.delete()
        return redirect('news_list')

    return render(request, 'news/news_delete.html', {'news': news})


# ─────────────────────────────────────────────
#  ADMIN — APPROVE NEWS
#  URL: /news/<id>/approve/
# ─────────────────────────────────────────────
@role_required(allowed_roles=['admin'])
def newsApproveView(request, pk):
    news              = get_object_or_404(News, pk=pk)
    news.status       = 'published'
    news.publish_date = timezone.now()
    news.save()
    return redirect('admin_dashboard')


# ─────────────────────────────────────────────
#  ADMIN — REJECT NEWS
#  URL: /news/<id>/reject/
# ─────────────────────────────────────────────
@role_required(allowed_roles=['admin'])
def newsRejectView(request, pk):
    news        = get_object_or_404(News, pk=pk)
    news.status = 'rejected'
    news.save()
    return redirect('admin_dashboard')