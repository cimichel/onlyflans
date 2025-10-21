from django.shortcuts import render
from django.http import HttpResponse
from .models import Flan



def index(request):
    return HttpResponse("🍮 OnlyFlans - Coming Soon! 🍮")

def flan_list(request):
    # Using Django ORM to get all flans
    flans = Flan.objects.all()
    
    # Using list comprehension (modern Python!)
    flan_data = [{
        'name': flan.name,
        'description': flan.description,
        'image_url': flan.image_url,
        'type': flan.get_flan_type_display(),  # Gets the display value
        'price': flan.get_display_price(),
        'is_premium': flan.is_premium
    } for flan in flans]
    
    return render(request, 'flans/list.html', {'flans': flan_data})