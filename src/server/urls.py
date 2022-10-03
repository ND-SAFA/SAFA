"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponse
from django.urls import path, include, re_path
from rest_framework import permissions
from server import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def homePageView(request):
    return HttpResponse("Welcome to SAFA's trace generation server!")


schema_view = get_schema_view(
    openapi.Info(
        title="TGen API",
        default_version='v1',
        description="TGen is SAFA's Trace Generation server. It allows for the creation of deep learning models, "
                    "the training of these models, and the prediction of new trace links.",
        contact=openapi.Contact(email="alberto@safa.ai"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^playground/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', homePageView),
    path('predict/', views.PredictView.as_view()),
    path('train/', views.TrainView.as_view()),
    path('models/', views.ModelView.as_view())
]
