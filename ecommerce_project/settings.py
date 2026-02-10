

# """
# Django settings for ecommerce_project project.
# ONLY FOR LOCAL DEVELOPMENT
# """

# from pathlib import Path
# import os
# from dotenv import load_dotenv

# # Build paths inside the project
# BASE_DIR = Path(__file__).resolve().parent.parent

# # .env file load karein
# load_dotenv(BASE_DIR / '.env')

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-key-123')

# # Local pe hamesha True rakhein taaki errors dikhen
# DEBUG = True

# # Local machine ke liye allow karein
# ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles', # Default static files
    
#     # Aapke local apps
#     'products',
#     'cart',
#     'login',
#     'dashboard',
#     'order',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'ecommerce_project.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'cart.context_processors.global_quantity',
#                 'products.context_processors.category_list',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# # Database - Sirf SQLite use hoga local ke liye
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # Password validation
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
# ]

# # Internationalization
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

# # Static files (CSS, JavaScript)
# STATIC_URL = 'static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
# # Local deployment ke liye staticfiles ka folder
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# # Media Files (Images local folder mein save hongi)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # Default storage settings (Cloudinary hata diya gaya hai)
# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# .env file load karein (sirf local ke liye kaam karega)
load_dotenv(os.path.join(BASE_DIR, '.env'))

# --- SECURITY ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-key-123')

# Render par Environment Variable mein DEBUG=False set karna zaroori hai
# DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
DEBUG = True

ALLOWED_HOSTS = ['shoppingkart-django.onrender.com', 'localhost', '127.0.0.1', '.onrender.com']

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'cloudinary_storage',  # Staticfiles se pehle hona chahiye
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    
    # Third party & Local Apps
    'widget_tweaks',
    'products',
    'cart',
    'login',
    'dashboard',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Static files ke liye
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.global_quantity',
                'products.context_processors.category_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Render par PostgreSQL use karne ke liye
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# --- STATIC & MEDIA SETTINGS ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary Config
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}
# --- STORAGE SYSTEM FIX (Simplified for Render & Django 6.0) ---

if DEBUG:
    # Local Storage
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    # Render Production:
    # 'CompressedStaticFilesStorage' ko hata kar sirf 'StaticFilesStorage' kiya hai
    # Isse missing .map files ka error nahi aayega.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'




# WhiteNoise ke nakhre khatam karne ke liye extra settings
WHITENOISE_MANIFEST_STRICT = False  # Missing files par build fail nahi hoga
WHITENOISE_USE_FINDERS = True       # Static files ko dhoondne mein help karega

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# WhiteNoise: AdminLTE .map files missing error fix
WHITENOISE_MANIFEST_STRICT = False

# --- OTHERS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'