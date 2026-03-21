from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Sum
from .forms import ProfileEditForm, CustomPasswordChangeForm


# ─────────────────────────────────────────────
#  PROFILE VIEW
# ─────────────────────────────────────────────
@login_required
def profileView(request):
    from core.models import News, Comment, Bookmark

    user    = request.user
    context = {}

    if user.role == 'journalist':
        total_articles  = News.objects.filter(journalist=user).count()
        published       = News.objects.filter(journalist=user, status='published').count()
        pending         = News.objects.filter(journalist=user, status='pending').count()
        total_views     = News.objects.filter(journalist=user).aggregate(
                            total=Sum('views'))['total'] or 0
        recent_articles = News.objects.filter(journalist=user).order_by('-created_at')[:5]
        context = {
            'total_articles':  total_articles,
            'published':       published,
            'pending':         pending,
            'total_views':     total_views,
            'recent_articles': recent_articles,
        }

    elif user.role == 'user':
        total_comments  = Comment.objects.filter(user=user).count()
        total_bookmarks = Bookmark.objects.filter(user=user).count()
        context = {
            'total_comments':  total_comments,
            'total_bookmarks': total_bookmarks,
        }

    elif user.role == 'advertiser':
        from core.models import Advertisement
        total_campaigns   = Advertisement.objects.filter(advertiser=user).count()
        active_campaigns  = Advertisement.objects.filter(advertiser=user, status='active').count()
        total_impressions = Advertisement.objects.filter(advertiser=user).aggregate(
                              total=Sum('impressions'))['total'] or 0
        context = {
            'total_campaigns':   total_campaigns,
            'active_campaigns':  active_campaigns,
            'total_impressions': total_impressions,
        }

    # admin → context = {} (no extra stats)

    return render(request, 'accounts/profile.html', context)


# ─────────────────────────────────────────────
#  PROFILE EDIT VIEW
# ─────────────────────────────────────────────
@login_required
def profileEditView(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'accounts/edit.html', {'form': form})


# ─────────────────────────────────────────────
#  CHANGE PASSWORD VIEW
# ─────────────────────────────────────────────
@login_required
def changePasswordView(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


# ─────────────────────────────────────────────
#  BOOKMARKS VIEW
# ─────────────────────────────────────────────
@login_required
def bookmarksView(request):
    from core.models import Bookmark
    bookmarks = Bookmark.objects.filter(
        user=request.user
    ).select_related('news', 'news__category', 'news__city').order_by('-created_at')

    return render(request, 'accounts/bookmarks.html', {
        'bookmarks': bookmarks,
    })


# ─────────────────────────────────────────────
#  BOOKMARK TOGGLE
# ─────────────────────────────────────────────
@login_required
def bookmarkToggleView(request, news_id):
    from core.models import Bookmark, News
    news     = get_object_or_404(News, news_id=news_id)
    bookmark = Bookmark.objects.filter(user=request.user, news=news).first()

    if bookmark:
        bookmark.delete()
        messages.success(request, 'Bookmark removed.')
    else:
        Bookmark.objects.create(user=request.user, news=news)
        messages.success(request, 'Article bookmarked!')

    return redirect('news_detail', pk=news_id)


# ─────────────────────────────────────────────
#  MY COMMENTS VIEW
# ─────────────────────────────────────────────
@login_required
def myCommentsView(request):
    from core.models import Comment
    comments = Comment.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('news').order_by('-created_at')

    return render(request, 'accounts/my_comments.html', {
        'comments': comments,
    })