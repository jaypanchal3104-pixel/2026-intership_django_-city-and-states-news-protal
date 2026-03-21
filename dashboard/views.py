from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from django.contrib import messages
from .decorators import role_required


# ─────────────────────────────────────────────
#  ADMIN DASHBOARD
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def adminDashboardView(request):
    from core.models import News, User, Category, State, City, Comment

    total_news        = News.objects.count()
    published_news    = News.objects.filter(status='published').count()
    pending_news      = News.objects.filter(status='pending').count()
    total_journalists = User.objects.filter(role='journalist').count()
    total_users       = User.objects.count()
    total_comments    = Comment.objects.count()

    pending_articles  = News.objects.filter(status='pending').order_by('-created_at')[:10]
    recent_news       = News.objects.all().order_by('-created_at')[:10]
    recent_users      = User.objects.order_by('-created_at')[:5]

    categories     = Category.objects.annotate(news_count=Count('news')).order_by('-news_count')
    states_summary = State.objects.annotate(
        city_count=Count('cities'),
        news_count=Count('cities__news')
    )
    states = State.objects.all()
    cities = City.objects.all()

    return render(request, "dashboard/admin_dashboard.html", {
        'total_news':        total_news,
        'published_news':    published_news,
        'pending_news':      pending_news,
        'total_journalists': total_journalists,
        'total_users':       total_users,
        'total_comments':    total_comments,
        'pending_articles':  pending_articles,
        'recent_news':       recent_news,
        'recent_users':      recent_users,
        'categories':        categories,
        'states_summary':    states_summary,
        'states':            states,
        'cities':            cities,
    })


# ─────────────────────────────────────────────
#  PENDING NEWS
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def pendingNewsView(request):
    from core.models import News
    pending_list = News.objects.filter(status='pending').order_by('-created_at')
    return render(request, "dashboard/pending_news.html", {
        'pending_list': pending_list,
        'pending_news': pending_list.count(),
    })


# ─────────────────────────────────────────────
#  CATEGORIES
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def categoriesView(request):
    from core.models import Category
    if request.method == 'POST':
        name = request.POST.get('category_name', '').strip()
        if name:
            Category.objects.create(category_name=name)
            messages.success(request, f'Category "{name}" created!')
        return redirect('admin_categories')

    categories = Category.objects.annotate(news_count=Count('news')).order_by('category_name')
    return render(request, "dashboard/categories.html", {
        'categories': categories,
    })


@role_required(allowed_roles=["admin"])
def categoryDeleteView(request, pk):
    from core.models import Category
    cat = get_object_or_404(Category, category_id=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted!')
    return redirect('admin_categories')


# ─────────────────────────────────────────────
#  STATES
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def statesView(request):
    from core.models import State
    if request.method == 'POST':
        name = request.POST.get('state_name', '').strip()
        if name:
            State.objects.create(state_name=name)
            messages.success(request, f'State "{name}" created!')
        return redirect('admin_states')

    states = State.objects.annotate(
        city_count=Count('cities'),
        news_count=Count('cities__news')
    ).order_by('state_name')
    return render(request, "dashboard/states.html", {
        'states': states,
    })


@role_required(allowed_roles=["admin"])
def stateDeleteView(request, pk):
    from core.models import State
    state = get_object_or_404(State, state_id=pk)
    if request.method == 'POST':
        state.delete()
        messages.success(request, 'State deleted!')
    return redirect('admin_states')


# ─────────────────────────────────────────────
#  CITIES
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def citiesView(request):
    from core.models import City, State
    if request.method == 'POST':
        name     = request.POST.get('city_name', '').strip()
        state_id = request.POST.get('state_id', '')
        if name and state_id:
            from core.models import State as S
            state = get_object_or_404(S, state_id=state_id)
            City.objects.create(city_name=name, state=state)
            messages.success(request, f'City "{name}" created!')
        return redirect('admin_cities')

    cities = City.objects.select_related('state').order_by('city_name')
    states = State.objects.all()
    return render(request, "dashboard/cities.html", {
        'cities': cities,
        'states': states,
    })


@role_required(allowed_roles=["admin"])
def cityDeleteView(request, pk):
    from core.models import City
    city = get_object_or_404(City, city_id=pk)
    if request.method == 'POST':
        city.delete()
        messages.success(request, 'City deleted!')
    return redirect('admin_cities')


# ─────────────────────────────────────────────
#  JOURNALISTS
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def journalistsView(request):
    from core.models import User
    journalists = User.objects.filter(role='journalist').order_by('-created_at')
    return render(request, "dashboard/journalists.html", {
        'journalists': journalists,
    })


# ─────────────────────────────────────────────
#  READERS
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def readersView(request):
    from core.models import User
    readers = User.objects.filter(role='user').order_by('-created_at')
    return render(request, "dashboard/readers.html", {
        'readers': readers,
    })


# ─────────────────────────────────────────────
#  ADVERTISERS
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def advertisersView(request):
    from core.models import User
    advertisers = User.objects.filter(role='advertiser').order_by('-created_at')
    return render(request, "dashboard/advertisers.html", {
        'advertisers': advertisers,
    })


# ─────────────────────────────────────────────
#  COMMENTS
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def commentsView(request):
    from core.models import Comment
    comments = Comment.objects.select_related('user', 'news').order_by('-created_at')
    return render(request, "dashboard/comments.html", {
        'comments': comments,
    })


@role_required(allowed_roles=["admin"])
def commentDeleteView(request, pk):
    from core.models import Comment
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted!')
    return redirect('admin_comments')


# ─────────────────────────────────────────────
#  ADVERTISEMENTS
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def advertisementsView(request):
    from core.models import Advertisement
    ads = Advertisement.objects.select_related('advertiser').order_by('-created_at')
    return render(request, "dashboard/advertisements.html", {
        'ads': ads,
    })


# ─────────────────────────────────────────────
#  ANALYTICS
# ─────────────────────────────────────────────
@role_required(allowed_roles=["admin"])
def analyticsView(request):
    from core.models import News, User, Comment
    from django.db.models import Count

    total_news      = News.objects.count()
    published_news  = News.objects.filter(status='published').count()
    total_views     = News.objects.aggregate(total=Sum('views'))['total'] or 0
    total_users     = User.objects.count()
    total_comments  = Comment.objects.count()

    top_news = News.objects.filter(
        status='published'
    ).order_by('-views')[:10]

    top_journalists = User.objects.filter(
        role='journalist'
    ).annotate(article_count=Count('news_articles')).order_by('-article_count')[:5]

    return render(request, "dashboard/analytics.html", {
        'total_news':       total_news,
        'published_news':   published_news,
        'total_views':      total_views,
        'total_users':      total_users,
        'total_comments':   total_comments,
        'top_news':         top_news,
        'top_journalists':  top_journalists,
    })


# ─────────────────────────────────────────────
#  JOURNALIST DASHBOARD
# ─────────────────────────────────────────────
@role_required(allowed_roles=["journalist"])
def journalistDashboardView(request):
    from core.models import News

    my_news = News.objects.filter(journalist=request.user).order_by('-created_at')

    status = request.GET.get('status')
    if status and status != 'all':
        my_news = my_news.filter(status=status)

    all_news        = News.objects.filter(journalist=request.user)
    published_count = all_news.filter(status='published').count()
    pending_count   = all_news.filter(status='pending').count()
    draft_count     = all_news.filter(status='draft').count()
    total_views     = all_news.aggregate(total=Sum('views'))['total'] or 0

    return render(request, "dashboard/journalist_dashboard.html", {
        'my_news':         my_news,
        'published_count': published_count,
        'pending_count':   pending_count,
        'draft_count':     draft_count,
        'total_views':     total_views,
    })


# ─────────────────────────────────────────────
#  ADVERTISER DASHBOARD
# ─────────────────────────────────────────────
@role_required(allowed_roles=["advertiser"])
def advertiserDashboardView(request):
    from core.models import Advertisement

    my_ads            = Advertisement.objects.filter(advertiser=request.user).order_by('-created_at')
    active_count      = my_ads.filter(status='active').count()
    pending_count     = my_ads.filter(status='pending').count()
    total_impressions = my_ads.aggregate(total=Sum('impressions'))['total'] or 0
    total_clicks      = my_ads.aggregate(total=Sum('clicks'))['total'] or 0

    return render(request, "dashboard/advertiser_dashboard.html", {
        'my_ads':            my_ads,
        'active_count':      active_count,
        'pending_count':     pending_count,
        'total_impressions': total_impressions,
        'total_clicks':      total_clicks,
    })


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
def homeView(request):
    from core.models import News, Category, State, City

    news_qs       = News.objects.filter(status='published').order_by('-publish_date')
    breaking_news = news_qs[:6]
    featured_news = news_qs.first()

    category_id = request.GET.get('category')
    if category_id:
        news_qs = news_qs.filter(category__category_id=category_id)

    state_id = request.GET.get('state')
    if state_id:
        news_qs = news_qs.filter(city__state__state_id=state_id)

    paginator = Paginator(news_qs, 6)
    news_list = paginator.get_page(request.GET.get('page'))

    categories = Category.objects.annotate(news_count=Count('news')).order_by('-news_count')
    states     = State.objects.all()
    top_cities = City.objects.annotate(news_count=Count('news')).order_by('-news_count')[:5]

    return render(request, "core/home.html", {
        'news_list':     news_list,
        'featured_news': featured_news,
        'breaking_news': breaking_news,
        'categories':    categories,
        'states':        states,
        'top_cities':    top_cities,
    })


# ─────────────────────────────────────────────
#  CITIES API
# ─────────────────────────────────────────────
def citiesApiView(request):
    state_id = request.GET.get('state_id')
    if not state_id:
        return JsonResponse({'cities': []})
    from core.models import City
    cities = City.objects.filter(state__state_id=state_id).values('city_id', 'city_name')
    return JsonResponse({'cities': list(cities)})


# ─────────────────────────────────────────────
#  UNAUTHORIZED
# ─────────────────────────────────────────────
def unauthorizedView(request):
    return render(request, "dashboard/unauthorized.html", status=403)


# ─────────────────────────────────────────────
#  LOGOUT
# ─────────────────────────────────────────────
def logoutView(request):
    logout(request)
    return redirect("login")


# ─────────────────────────────────────────────
#  DASHBOARD REDIRECT
# ─────────────────────────────────────────────
def dashboardRedirectView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    role = request.user.role
    if role == "admin":
        return redirect("admin_dashboard")
    elif role == "journalist":
        return redirect("journalist_dashboard")
    elif role == "advertiser":
        return redirect("advertiser_dashboard")
    else:
        return redirect("home")