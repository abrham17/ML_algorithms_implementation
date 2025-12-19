from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, InventoryViewSet, TransactionViewSet, ScheduleViewSet, ChatViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'chat', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]
