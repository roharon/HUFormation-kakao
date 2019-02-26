from django.conf.urls import url
from . import views
from . import haksik_table_make


urlpatterns = [
    url(r'^keyboard', views.keyboard),
    url(r'^message', views.message),
    url(r'^seoul_menu', haksik_table_make.to_seo_table),
    url(r'^global_menu', haksik_table_make.to_glo_table),
    url(r'^analysis', views.analysis),
    url(r'^rest/<cafeteria>/<int:day>', views.rest_api_cafe())
]
