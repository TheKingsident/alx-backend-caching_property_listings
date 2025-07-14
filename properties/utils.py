from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Get all properties with manual cache management.
    
    Checks Redis cache first, if not found:
    - Fetches from database
    - Stores in cache for 1 hour (3600 seconds)
    - Returns the queryset
    """
    # Try to get properties from cache
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        # Return cached data
        return cached_properties
    
    # Cache miss - fetch from database
    properties = Property.objects.all()
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set('all_properties', properties, 3600)
    
    return properties
