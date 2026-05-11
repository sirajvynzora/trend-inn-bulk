"""
Django settings for trend_in_bulk_pro project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
# WARNING: Keep secret key, passwords, and API keys secret in production!
SECRET_KEY = 'your-secret-key-here-change-in-production'
DEBUG = True  # Changed to False for production safety
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'localhost', '127.0.0.1']

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'trend_in_bulk_app',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trend_in_bulk_pro.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'trend_in_bulk_app.context_processors.google_reviews',
                'trend_in_bulk_app.context_processors.admin_unread_contacts',
                'trend_in_bulk_app.context_processors.menu_categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'trend_in_bulk_pro.wsgi.application'

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONAL
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# EMAIL - REPLACE WITH YOUR CREDENTIALS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@your-domain.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# GOOGLE REVIEWS
GOOGLE_REVIEW_RATING = 4.7
GOOGLE_REVIEW_COUNT = 900
GOOGLE_REVIEW_URL = "https://www.google.com/travel/search?q=Koodaram%20camping%20reviews"

# RECAPTCHA - REPLACE WITH YOUR KEYS
RECAPTCHA_SITE_KEY = "your-recaptcha-site-key"
RECAPTCHA_SECRET_KEY = "your-recaptcha-secret-key"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'