import os  # noqa: I001

from .base import *

from dotenv import load_dotenv

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

DEBUG = os.environ["DJANGO_DEBUG"].lower() == "true"


ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")


DATABASE = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
