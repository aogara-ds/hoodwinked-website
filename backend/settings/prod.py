from .base import *

DEBUG = False
ALLOWED_HOSTS = ['hoodwinked.onrender.com']
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'https://hoodwinked.ai', 
    'https://www.hoodwinked.ai',
    'https://hoodwinked.vercel.app'
]

CSRF_TRUSTED_ORIGINS = [
    'https://hoodwinked.ai', 
    'https://www.hoodwinked.ai',
    'https://hoodwinked.vercel.app'
]