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
from api.endpoints.completion.completion_view import perform_completion
from api.endpoints.views.hgen_view import perform_hgen
from api.endpoints.views.project_summary_view import perform_project_summary
from api.endpoints.views.result_view import cancel_job, get_active_task_ids, get_pending_task_ids, get_result, get_status
from api.endpoints.views.summarize_view import perform_summarization_job, perform_summarization_sync
from api.endpoints.views.trace_view import perform_prediction, perform_search
from api.endpoints.views.wait_view import perform_wait
from api.server.app_endpoints import AppEndpoints


def wrap_html(body: str):
    markdown_body = markdown.markdown(body)
    return f"<html><body>{markdown_body}</body></html>"


def homePageView(request):
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
    re_path(r'^playground/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', homePageView),
    path(AppEndpoints.COMPLETE.as_path(), perform_completion),
    path(AppEndpoints.TGEN.as_path(), perform_prediction),
    path(AppEndpoints.TGEN.as_path(suffix="sync"), perform_search),
    path(AppEndpoints.HGEN.as_path(), perform_hgen),
    path(AppEndpoints.PROJECT_SUMMARY.as_path(), perform_project_summary),
    path(AppEndpoints.SUMMARIZE.as_path(), perform_summarization_job),
    path(AppEndpoints.SUMMARIZE.as_path(suffix="sync"), perform_summarization_sync),
    path(AppEndpoints.STATUS.as_path(), get_status),
    path(AppEndpoints.CANCEL.as_path(), cancel_job),
    path(AppEndpoints.RESULTS.as_path(), get_result),
    path(AppEndpoints.TASKS_ACTIVE.as_path(), get_active_task_ids()),
    path(AppEndpoints.TASKS_PENDING.as_path(), get_pending_task_ids()),
    path(AppEndpoints.WAIT.as_path(), perform_wait)
]
