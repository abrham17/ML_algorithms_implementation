from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser, Inventory, Transaction, Schedule
from .serializers import UserSerializer, InventorySerializer, TransactionSerializer, ScheduleSerializer
from .mcp.processor import MCPProcessor

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Auto-deduct stock logic
        transaction = serializer.save(user=self.request.user)
        if transaction.transaction_type == 'SALE' and transaction.product:
            transaction.product.stock_quantity -= transaction.quantity
            transaction.product.save()
        elif transaction.transaction_type == 'PURCHASE' and transaction.product:
            transaction.product.stock_quantity += transaction.quantity
            transaction.product.save()

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def send(self, request):
        message = request.data.get('message')
        if not message:
            return Response({'error': 'Message required'}, status=status.HTTP_400_BAD_REQUEST)
        
        processor = MCPProcessor()
        try:
            # Pass user context if needed (e.g. user id)
            response_text = processor.process_message(message, user_context=f"User ID: {request.user.id}")
            return Response({'response': response_text})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
