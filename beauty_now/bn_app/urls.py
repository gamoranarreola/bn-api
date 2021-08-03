from django.urls import path

from .views import (
    beautiers,
    beautier_by_id,
    beautiers_for_specialties,
    calendars_for_beautiers,
    service_by_id,
    service_by_category_id,
    service_categories,
    service_category_by_id,
    UserActivationView,
    me,
    work_orders,
    handle_payment,
    get_formatted_address
)

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
    path('api/work-orders', work_orders),
    path('api/payment/', handle_payment),
    path('api/formatted-address/', get_formatted_address),
    path('api/users/me', me),
]
