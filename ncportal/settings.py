from pathlib import Path
import dj_database_url
import os
from dotenv import load_dotenv
import cloudinary

# ✅ Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Load environment variables from .env
load_dotenv(dotenv_path=BASE_DIR / ".env")

# ✅ Safe environment parsing
def get_bool(value, default=False):
    return str(value).strip().lower() in ("true", "1", "yes") if value is not None else default

# ✅ Load config values
SECRET_KEY = os.environ.get("SECRET_KEY", "unsafe-dev-key")
DEBUG = get_bool(os.environ.get("DEBUG"))
USE_LOCAL_DB = get_bool(os.environ.get("USE_LOCAL_DB"))

# ✅ Cloudinary configuration
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("CLOUD_API_KEY"),
    api_secret=os.environ.get("CLOUD_API_SECRET"),
)

# ✅ Hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'nc-voting-portal.onrender.com']

# ✅ Installed apps
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'vote.apps.VoteConfig',
    'widget_tweaks',
    'customadmin',
    'cloudinary',
    'cloudinary_storage',
    'axes',
    # removed 'csp',
]

# ✅ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'axes.middleware.AxesMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',                     # 🔐 Blocks brute-force attempts
    'django.contrib.auth.backends.ModelBackend',     # ✅ Standard Django login
]

# ✅ URLs & Templates
ROOT_URLCONF = 'ncportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'vote' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Removed CSP context processors
                # 'ncportal.context_processors.csp_nonce',  # remove this if it's related to CSP nonce
            ],
        },
    },
]

WSGI_APPLICATION = 'ncportal.wsgi.application'

# ✅ Database switch (local SQLite or Render PostgreSQL)
if USE_LOCAL_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }

# ✅ Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Blantyre'
USE_I18N = True
USE_TZ = True

# ✅ Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'vote' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Media (Cloudinary)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUD_API_KEY'),
    'API_SECRET': os.environ.get('CLOUD_API_SECRET'),
    'SECURE': True,  # Ensures media URLs use HTTPS
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ✅ SECURITY SETTINGS (only apply in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # ✅ Safe for development (no HTTPS enforcement)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ✅ Strong session and CSRF cookie hardening (apply in all environments)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 2  # 2 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ✅ Extra security headers
SECURE_BROWSER_XSS_FILTER = True          # Enables the X-XSS-Protection: 1; mode=block header
SECURE_REFERRER_POLICY = 'same-origin'    # Controls Referer header to avoid leaking URLs

# ✅ Login
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/dashboard/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ Use Argon2 for password hashing
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # fallback
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# ✅ Axes config
AXES_FAILURE_LIMIT = 5  # Lock after 5 failed attempts
AXES_COOLOFF_TIME = 1  # Lock lasts 1 hour
AXES_RESET_ON_SUCCESS = True
