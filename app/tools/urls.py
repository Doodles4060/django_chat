from django.urls import path

from . import views

app_name = 'tools'

PIXELATE_SVG_URLS = [
    path('svg-pixelation/', views.SVGPixelationView.as_view(), name='svg_pixelation'),
]

urlpatterns = [
    *PIXELATE_SVG_URLS,
]
