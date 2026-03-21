from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):

    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('journalist', 'Journalist'),   # 'reporter' → 'journalist',
        ('advertiser', 'Advertiser'),   # new
        ('user', 'User'),              # reader = user
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # ✅ New Fields (Signup change na thay etle blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=(
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ),
        blank=True,
        null=True
    )
    mobile = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return self.email
    


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.state_name

    class Meta:
        ordering = ['state_name']


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=50)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.city_name}, {self.state.state_name}"

    class Meta:
        ordering = ['city_name']
        verbose_name_plural = 'Cities'
        unique_together = ('city_name', 'state')


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
        verbose_name_plural = 'Categories'


class News(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    )

    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='news/images/', blank=True, null=True)
    publish_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)

    journalist = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news_articles',
        limit_choices_to={'role': 'journalist'}
    )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='news')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='news')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date', '-created_at']
        verbose_name_plural = 'News'


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.user.email} on '{self.news.title}'"

    class Meta:
        ordering = ['-created_at']


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} → {self.news.title}"

    class Meta:
        unique_together = ('user', 'news')
        ordering = ['-created_at']


class Advertisement(models.Model):
    PLACEMENT_CHOICES = (
        ('homepage', 'Homepage Banner'),
        ('article', 'Article Page'),
        ('sidebar', 'Side Banner'),
        ('footer', 'Footer Banner'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('rejected', 'Rejected'),
    )

    advertiser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='campaigns',
        limit_choices_to={'role': 'advertiser'}
    )
    name = models.CharField(max_length=200)
    ad_image = models.ImageField(upload_to='ads/images/', blank=True, null=True)
    ad_url = models.URLField(blank=True, null=True)
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES, default='sidebar')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.advertiser.email})"

    class Meta:
        ordering = ['-created_at']   