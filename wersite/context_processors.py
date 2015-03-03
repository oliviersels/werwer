from django.conf import settings

def analytics_processor(request):
    my_dict = {
        'ga_id': getattr(settings, 'GA_ID', ''),
    }

    return my_dict
