from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Hardware
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
import json

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_panel(request):
    return render(request, 'admin_panel.html')

# API: Adding device
@user_passes_test(is_admin)
def add_hardware(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Hardware.objects.create(
            name=data['name'],
            brand=data['brand'],
            status='Available'
        )
        return JsonResponse({'status': 'ok'})

# API: deleting device
@user_passes_test(is_admin)
def delete_hardware(request, item_id):
    Hardware.objects.filter(id=item_id).delete()
    return JsonResponse({'status': 'ok'})

# API: Creating user (Pillar 1 Requirement)
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'User already exists'}, status=400)
        
        User.objects.create_user(username=data['username'], password=data['password'])
        return JsonResponse({'status': 'ok'})

def get_inventory(request):
    items = Hardware.objects.all().values()
    return JsonResponse(list(items), safe=False)

@login_required
def rent_item(request, item_id):
    hardware = get_object_or_404(Hardware, id=item_id)
    
    # GUARD: Only status 'Available' lets rent
    if hardware.status == 'Available':
        hardware.status = 'In Use'
        hardware.assigned_to = request.user.email
        hardware.save()
        return JsonResponse({'status': 'ok'})
    
    # If status repair or in use return 400
    return JsonResponse({'error': 'Device not available for rent'}, status=400)

@login_required
def return_item(request, item_id):
    item = get_object_or_404(Hardware, id=item_id)
    
    item.status = 'Available'
    item.assigned_to = None
    item.save()
    
    return JsonResponse({"message": f"Returned {item.name}"})

def dashboard(request):
    return render(request, 'dashboard.html')

genai.configure(api_key="AIzaSyAdv8S7XEwACLtMZPo4WeQLt0enrK5ad6E")
model_ai = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

def ai_search(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({"results": []})

    try:
        inventory_items = list(Hardware.objects.all().values_list('name', flat=True))
        
        prompt = f"""
        You are a hardware assistant. Based ONLY on this list of available devices: {inventory_items}.
        Which one is best for: "{query}"?
        Return ONLY the exact name from the list. If nothing fits, return 'None'.
        """
        
        response = model_ai.generate_content(prompt)
        suggested_name = response.text.strip()

        print(f"DEBUG: AI suggested: '{suggested_name}'")

        if "None" in suggested_name or not suggested_name:
            return JsonResponse({"results": []})

        results = list(Hardware.objects.filter(name__icontains=suggested_name).values())
        
        if not results:
            all_hardware = Hardware.objects.all()
            results = [item for item in all_hardware if item.name.lower() in suggested_name.lower()]
            results = [{"id": r.id, "name": r.name, "brand": r.brand, "status": r.status} for r in results]

        return JsonResponse({"results": results})

    except Exception as e:
        print(f"AI Error: {e}")
        return JsonResponse({"results": [], "error": str(e)}, status=500)