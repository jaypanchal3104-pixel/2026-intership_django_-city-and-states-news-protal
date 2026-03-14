#from django.contrib import admin
#from .models import User,State,City,Category,News,Comment,Bookmark,Advertisement

# Register your models here.
#admin.site.register(User)
#admin.site.register(State)
#admin.site.register(City)
#admin.site.register(Category)
#admin.site.register(News)
#admin.site.register(Comment)
#admin.site.register(Bookmark)



#admin.site.register(Advertisement)
from django.contrib import admin
from .models import (
    User, State, City, Category,
    News, Comment, Bookmark, Advertisement,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display  = ['email', 'firstname', 'lastname', 'role', 'is_active', 'created_at']
    list_filter   = ['role', 'is_active']
    search_fields = ['email', 'firstname', 'lastname']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display  = ['state_id', 'state_name']   # ← ID દેખાશે
    search_fields = ['state_name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display  = ['city_id', 'city_name', 'state']   # ← ID દેખાશે
    list_filter   = ['state']
    search_fields = ['city_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['category_id', 'category_name']   # ← ID દેખાશે
    search_fields = ['category_name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display  = ['news_id', 'title', 'journalist', 'category', 'city', 'status', 'publish_date']
    list_filter   = ['status', 'category']
    search_fields = ['title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'news', 'is_active', 'created_at']
    list_filter   = ['is_active']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display  = ['user', 'news', 'created_at']


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display  = ['name', 'advertiser', 'placement', 'status', 'budget']
    list_filter   = ['status', 'placement']
    search_fields = ['name']