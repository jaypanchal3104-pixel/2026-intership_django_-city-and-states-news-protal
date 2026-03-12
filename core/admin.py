from django.contrib import admin
from .models import User,State,City,Category,News,Comment,Bookmark,Advertisement

# Register your models here.
admin.site.register(User)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Category)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Advertisement)