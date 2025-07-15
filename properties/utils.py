from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property

# Set up logging
logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    """
    Get Redis cache performance metrics.
    
    Connects to Redis via django_redis and retrieves:
    - keyspace_hits: Number of successful lookups
    - keyspace_misses: Number of failed lookups  
    - hit_ratio: Percentage of successful cache hits
    
    Returns:
        dict: Dictionary containing cache metrics
    """
    try:
        # Get Redis connection via django_redis
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO stats
        info = redis_conn.info()
        
        # Extract keyspace statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 2),
            'hit_ratio_formatted': f"{hit_ratio:.2f}%"
        }
        
        # Log metrics
        logger.info(f"Redis Cache Metrics - Hits: {keyspace_hits}, "
                   f"Misses: {keyspace_misses}, Hit Ratio: {hit_ratio:.2f}%")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
            'hit_ratio_formatted': "0.00%"
        }
