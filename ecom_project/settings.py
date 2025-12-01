from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")
MIGRATION_SECRET = os.getenv("MIGRATION_SECRET")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "rohitrajvaidya25.pythonanywhere.com",
    "e-commerce-project-yb1q.onrender.com",
]

# ---------------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Your apps
    "products",
    "orders",
    "accounts.apps.AccountsConfig",
    # Cloudinary
    "cloudinary",
    "cloudinary_storage",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ROOT_URLCONF = "ecom_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "products.context_processors.cart_item_count",
            ],
        },
    },
]

WSGI_APPLICATION = "ecom_project.wsgi.application"

# ---------------------------------------------------------
# DATABASE CONFIG — POSTGRESQL FOR RENDER
# ---------------------------------------------------------

ENVIRONMENT = os.getenv("ENV", "local")

if ENVIRONMENT == "production":
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEBUG = ENVIRONMENT != "production"

# ---------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# STATIC & MEDIA (STATICFILES + CLOUDINARY FIXED)
# ---------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUD_API_KEY"),
    "API_SECRET": os.getenv("CLOUD_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Django still needs MEDIA_URL, but Cloudinary stores files, not local disk
MEDIA_URL = "/"

# DO NOT use MEDIA_ROOT with Cloudinary
# MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------
# EMAIL SETTINGS
# ---------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# ---------------------------------------------------------
# RAZORPAY
# ---------------------------------------------------------

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

# ---------------------------------------------------------
# DEFAULT FIELD TYPE
# ---------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"


SESSION_COOKIE_AGE = 15 * 60  # 15 minutes
SESSION_SAVE_EVERY_REQUEST = True  # refresh timer on each request
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
