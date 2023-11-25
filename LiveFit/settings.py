

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

SECRET_KEY = "django-insecure-z1rzy#y)5p84sc_7u8kikd#cp4o^be+!k(vrjycmt$)23fbg&&"

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'home',
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'ckeditor',


]


JAZZMIN_SETTINGS = {
    "site_title": "LiveFit Store Admin",  # Title displayed in the admin panel
    "site_header": "LiveFit Store Admin",  # Header text at the top of the admin panel
    "site_brand": "LiveFit-Store",  # Brand name displayed in the sidebar

    # Logo displayed in the top-left corner of the admin panel (replace 'logo1.png' with the actual image path)
    "site_logo": "app/images/logo1.png",

    # Customize the login page logo and dark version (if desired)
    "login_logo": None,
    "login_logo_dark": None,

    # CSS classes for the site logo (you can customize this for styling)
    "site_logo_classes": "img-circle",

    # Favicon (site icon) displayed in the browser tab (replace 'favicon.ico' with the actual icon path)
    "site_icon": "favicon.ico",

    # Welcome message displayed in the admin panel
    "welcome_sign": "Welcome to LiveFit Store Admin",

    # Copyright information
    "copyright": "© 2023 Live Fit Ltd",

    # User avatar settings (you can customize this)
    "user_avatar": None,

    # Top menu links for easy navigation (customize as needed)
    "topmenu_links": [
        {"name": "Users", "url": "admin:auth_user_changelist", "permissions": ["auth.view_user"]},
        {"name": "Products", "url": "admin:app_product_changelist", "permissions": ["app.view_product"]},
        {"name": "Carts", "url": "admin:app_cart_changelist", "permissions": ["app.view_cart"]},
        {"name": "Customers", "url": "admin:app_customer_changelist", "permissions": ["app.view_customer"]},
        {"name": "Orders", "url": "admin:app_orderplaced_changelist", "permissions": ["app.view_orderplaced"]},
    ],

    # User menu links (customize as needed)
    "usermenu_links": [
        {"name": "Profile", "url": "admin:auth_user_change", "permissions": ["auth.change_user"]},
        {"name": "My Customers", "url": "admin:app_customer_changelist", "permissions": ["app.view_customer"]},
    ],

    # Sidebar settings
    "show_sidebar": True,  # Display the sidebar
    "navigation_expanded": True,  # Expand the navigation menu by default

    # Customizing what apps and models are shown in the admin panel (hide_apps, hide_models)
    "hide_apps": [],  # List of app names to hide
    "hide_models": [],  # List of model names to hide

    # Ordering of models (customize as needed)
    "order_with_respect_to": ["auth", "app", "app.cart", "app.orderplaced"],

    # Custom links in the app menu (customize as needed)
    "custom_links": {
        "app": [
            {
                "name": "Make Messages",
                "url": "make_messages",
                "icon": "fas fa-comments",
                "permissions": ["app.ProductView"]
            },
        ],
    },

    # Icons for models (customize as needed)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app.Verification": "fas fa-address-card",
        "app.cart": "fas fa-shopping-cart",
        "app.OrderPlaced": "fas fa-shipping-fast",
        "app.brand": "fab fa-font-awesome-flag",
        "app.Customer": "fas fa-user-check",
        "app.product": "fab fa-product-hunt",
    },

    # Default icons for parent and child items
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Toggle for related modal (customize as needed)
    "related_modal_active": False,

    # Custom CSS and JS (you can add paths to your custom CSS and JS files here)
    "custom_css": [
        "path/to/custom-style.css",
    ],
    "custom_js": [
        "path/to/custom-script.js",
    ],

    # Show or hide the UI builder and language chooser
    "show_ui_builder": False,
    "language_chooser": False,
    "show_ui_builder": True,
    
    # Theme settings (customize the theme and color scheme)
    "theme": "darkly",  # Available themes: 'default', 'cosmo', 'darkly', 'flatly', 'journal', 'litera', 'lumen', 'lux', 'materia', 'minty', 'pulse', 'sandstone', 'simplex', 'sketchy', 'slate', 'solar', 'spacelab', 'superhero', 'united', 'yeti'
    "dark_mode_theme": "darkly",  # Dark mode theme
    "brand_colour": "navbar-primary",  # Color for the brand in the navbar
    "accent": "accent-primary",  # Accent color

    # Navbar and sidebar styles (customize as needed)
    "navbar": "navbar-dark bg-primary",  # Navbar style
    "no_navbar_border": False,  # Toggle navbar border
    "navbar_fixed": False,  # Fix navbar at the top
    "layout_boxed": False,  # Enable boxed layout
    "footer_fixed": False,  # Fix footer at the bottom
    "sidebar_fixed": True,  # Fix sidebar on scroll
    "sidebar": "sidebar-dark",  # Sidebar style
    "sidebar_nav_small_text": False,  # Use small text in the sidebar navigation
    "sidebar_disable_expand": False,  # Disable sidebar expand/collapse
    "sidebar_nav_child_indent": False,  # Indent child items in the sidebar navigation
    "sidebar_nav_compact_style": False,  # Use compact style in the sidebar navigation
    "sidebar_nav_legacy_style": False,  # Use legacy style in the sidebar navigation
    "sidebar_nav_flat_style": False,  # Use flat style in the sidebar navigation
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",  # Change this to a suitable color like "navbar-success"
    "accent": "accent-primary",  # Change this to an accent color like "accent-info"
    "navbar": "navbar-navy navbar-dark",  # You can experiment with different styles
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",  # Adjust sidebar color and style as needed
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",  # You can try other themes like "slate" or "cerulean"
    "dark_mode_theme": "darkly",  # Customize dark mode theme if desired
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}




MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "LiveFit.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "LiveFit.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

CKEDITOR_UPLOAD_PATH = "uploads/"  
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 300,
        'width': 800,
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['Link', 'Unlink'],
            ['NumberedList', 'BulletedList'],
            ['RemoveFormat'],
        ],
    },
}

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_REDIRECT_URL = '/profile/'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT =587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sauravsubedii19@gmail.com'
EMAIL_HOST_PASSWORD = 'phyctyqlhvfewfmc'

