import os
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
from .models import ConversionLog

def index(view_request):
    return render(view_request, 'core/index.html')

@csrf_exempt
def convert_images(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    files = request.FILES.getlist('images')
    if not files:
        return JsonResponse({'error': 'No images uploaded'}, status=400)
    
    if len(files) > 30:
        return JsonResponse({'error': 'Maximum 30 images allowed'}, status=400)

    order = request.POST.getlist('order')
    
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdfs')
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(pdf_dir, exist_ok=True)

    saved_files = {}
    allowed_extensions = {'png', 'jpg', 'jpeg'}

    for file in files:
        ext = file.name.rsplit('.', 1)[-1].lower()
        if ext in allowed_extensions:
            unique_name = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(upload_dir, unique_name)
            with open(filepath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            saved_files[file.name] = filepath

    # Arrange paths according to user drag-and-drop order
    ordered_paths = [saved_files[name] for name in order if name in saved_files]
    if not ordered_paths:
        ordered_paths = list(saved_files.values())

    if not ordered_paths:
        return JsonResponse({'error': 'No valid images processed'}, status=400)

    try:
        images = [Image.open(p).convert('RGB') for p in ordered_paths]
        pdf_filename = f"{uuid.uuid4()}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        
        images[0].save(pdf_path, save_all=True, append_images=images[1:])

        # Save record in SQLite DB
        ConversionLog.objects.create(filename=pdf_filename, image_count=len(images))

        pdf_url = f"{settings.MEDIA_URL}pdfs/{pdf_filename}"
        return JsonResponse({'success': True, 'pdf_url': pdf_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)