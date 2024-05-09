"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import markdown
from django.http import HttpResponse
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.constants.config import get_current_version, get_home_page
from api.endpoints.auth_view import generate_key
from api.endpoints.gen.chat.chat_name_view import perform_chat_name
from api.endpoints.gen.chat.chat_view import perform_chat
from api.endpoints.gen.health_checks.health_check_view import perform_health_check
from api.endpoints.gen.hgen.hgen_view import perform_hgen
from api.endpoints.gen.summarize.summarize_view import perform_summarization_job, perform_summarization_sync
from api.endpoints.gen.trace.trace_view import perform_embedding_search, perform_trace_prediction
from api.endpoints.health_view import health_metrics
from api.endpoints.task_view import cancel_job, get_active_task_ids, get_pending_task_ids, get_result, get_status
from api.endpoints.wait_view import perform_wait
from api.server.app_endpoints import AppEndpoints


def wrap_html(body: str) -> str:
    """
    Wraps text body in HTML page.
    :param body: The body to display.
    :return: The HTML of the page containing body
    """
    markdown_body = markdown.markdown(body)
    return f"<html><body>{markdown_body}</body></html>"


def homePageView(request):
    """
    Returns the home page of TGEN.
    :param request: Ignored.
    :return: HTTP containing home page.
    """
    home_page = get_home_page()
    return HttpResponse(wrap_html(home_page))


schema_view = get_schema_view(
    openapi.Info(
        title="TGen API",
        default_version=f"{get_current_version()}",
        description="TGen is SAFA's Trace Generation server.",
        contact=openapi.Contact(email="alberto@safa.ai"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', homePageView),
    re_path(r'^playground/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Api Endpoints,
    path(AppEndpoints.API.as_path(), generate_key),
    # Generation Endpoints
    path(AppEndpoints.TGEN.as_path(), perform_trace_prediction),
    path(AppEndpoints.TGEN.as_path(suffix="sync"), perform_embedding_search),
    path(AppEndpoints.HGEN.as_path(), perform_hgen),
    path(AppEndpoints.CHAT.as_path(), perform_chat),
    path(AppEndpoints.CHAT_TITLE.as_path(), perform_chat_name),
    path(AppEndpoints.HEALTH.as_path(), perform_health_check),
    path(AppEndpoints.SUMMARIZE.as_path(), perform_summarization_job),
    path(AppEndpoints.SUMMARIZE.as_path(suffix="sync"), perform_summarization_sync),
    # Celery Endpoints
    path(AppEndpoints.STATUS.as_path(), get_status),
    path(AppEndpoints.CANCEL.as_path(), cancel_job),
    path(AppEndpoints.RESULTS.as_path(), get_result),
    # Health/Testing Endpoints
    path(AppEndpoints.WAIT.as_path(), perform_wait),
    path(AppEndpoints.TASKS_ACTIVE.as_path(), get_active_task_ids()),
    path(AppEndpoints.TASKS_PENDING.as_path(), get_pending_task_ids()),
    path(AppEndpoints.SYSTEM.as_path(), health_metrics())
]
