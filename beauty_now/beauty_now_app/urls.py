from django.urls import path

from .views.beautier_views import (beautier_by_id, beautiers,
                                   beautiers_for_specialties)
from .views.service_views import (calendars_for_beautiers,
                                  service_by_category_id, service_by_id,
                                  service_categories, service_category_by_id)
from .views.user_views import UserActivationView, me
from .views.work_order_views import work_orders, get_formatted_address, payment, send_email

urlpatterns = [
    path('api/beautiers', beautiers),
    path('api/beautiers/<int:pk>', beautier_by_id),
    path('api/beautiers/specialties/', beautiers_for_specialties),
    path('api/beautiers-calendars', calendars_for_beautiers),
    path('api/services/<int:pk>', service_by_id),
    path('api/services/category/<int:service_category_id>', service_by_category_id),
    path('api/service-categories', service_categories),
    path('api/service-categories/<int:pk>', service_category_by_id),
    path('activate/<str:uid>/<str:token>', UserActivationView.as_view()),
    path('api/work-orders/', work_orders),
    path('api/payment/', payment),
    path('api/send-email/', send_email),
    path('api/formatted-address/', get_formatted_address),
    path('api/users/me', me),
]
