from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = Property.objects.all()
    
    # Convert properties to list of dictionaries
    properties_data = []
    for property in properties:
        properties_data.append({
            'id': property.id,
            'title': property.title,
            'description': property.description,
            'price': str(property.price),
            'location': property.location,
            'created_at': property.created_at.isoformat(),
        })
    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data),
        'cached': True,
    })
