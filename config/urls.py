from django.contrib import admin
from django.urls import include, path

from accounts.views import admin_dashboard


urlpatterns = [

    # =========================
    # لوحة Django الأصلية
    # =========================

    path(
        "admin/",
        admin.site.urls
    ),

    # =========================
    # لوحة تحكم المدير
    # =========================

    path(
        "dashboard/admin/",
        admin_dashboard,
        name="admin_dashboard"
    ),

    # =========================
    # الأكاديمية
    # =========================

    path(
        "",
        include("academy.urls")
    ),

    # =========================
    # الحسابات
    # =========================

    path(
        "accounts/",
        include("accounts.urls")
    ),
]