from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PenSerializer, RefillSerializer
from .models import Pen, Refill

class PenViewSet(viewsets.ModelViewSet):
    queryset = Pen.objects.all()
    serializer_class = PenSerializer

    def get_queryset(self):
        queryset = Pen.objects.all()
        params = self.request.query_params

        # Filter by category
        if params.get('category'):
            queryset = queryset.filter(category=params['category'])

        # Filter by sale status
        if params.get('on_sale'):
            queryset = queryset.filter(on_sale=params['on_sale'] == "true")

        # Filter by stock
        if params.get('in_stock'):
            queryset = queryset.filter(in_stock=params['in_stock'] == "true")

        # Filter by vintage
        if params.get('is_vintage'):
            queryset = queryset.filter(is_vintage=params['is_vintage'] == "true")

        return queryset

class RefillViewSet(viewsets.ModelViewSet):
    queryset = Refill.objects.all()
    serializer_class = RefillSerializer

    def get_queryset(self):
        queryset = Refill.objects.all()
        params = self.request.query_params

        # Optional: Filter by category
        if params.get('category'):
            queryset = queryset.filter(category=params['category'])

        # Filter by brand
        if params.get('brand'):
            queryset = queryset.filter(brand=params['brand'])

        # Filter by ink color
        if params.get('ink_color'):
            queryset = queryset.filter(ink_color=params['ink_color'])

        # Filter by stock
        if params.get('in_stock'):
            queryset = queryset.filter(in_stock=params['in_stock'] == "true")

        return queryset

@api_view(['GET'])
def get_stock(request, product_type, product_id):
    """
    URL examples:
    /api/stock/pen/3/
    /api/stock/refill/7/
    """
    model = Pen if product_type == 'pen' else Refill

    try:
        product = model.objects.get(id=product_id)
        return Response({
            "id": product.id,
            "type": product_type,
            "available_quantity": product.quantity,
        })
    except model.DoesNotExist:
        return Response({"error": f"{product_type.capitalize()} not found"}, status=404)

@api_view(['GET'])
def category_choices(request):
    return Response({
        "pen_categories": Pen.CATEGORY_CHOICES,
        "refill_categories": getattr(Refill, "CATEGORY_CHOICES", []),
    })
