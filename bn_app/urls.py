from django.urls import path

from .views import (
    UserActivationView,
    admin_customer_profiles,
    admin_staff_assignments,
    admin_staff_lines,
    admin_work_orders,
    beautier_work,
    beautiers,
    calendars_for_beautiers,
    get_regions,
    handle_payment,
    service_categories,
    work_orders,
)

urlpatterns = [
    path("api/beautiers", beautiers),
    path("api/beautiers/<int:pk>/work", beautier_work),
    path("api/beautiers-calendars", calendars_for_beautiers),
    path("api/service-categories", service_categories),
    path("api/services/regions", get_regions),
    path("activate/<str:uid>/<str:token>", UserActivationView.as_view()),
    path("api/work-orders", work_orders),
    path("api/payment/", handle_payment),
    # ADMIN
    path("api/admin/customer-profiles", admin_customer_profiles),
    path("api/admin/work-orders", admin_work_orders),
    path("api/admin/staff-assignments/", admin_staff_assignments),
    path("api/admin/staff-lines/", admin_staff_lines),
    path("api/admin/staff-lines/<int:pk>", admin_staff_lines),
]
