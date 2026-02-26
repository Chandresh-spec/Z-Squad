from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def manage_preferences(request):
    """Get or update the user's reading preferences."""
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        # Auto-create if it somehow doesn't exist
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'GET':
        return Response({
            'reading_need': profile.reading_need,
            'reading_need_display': profile.get_reading_need_display()
        })
        
    elif request.method == 'PATCH':
        new_need = request.data.get('reading_need')
        if new_need:
            # Validate choice
            valid_choices = [c[0] for c in UserProfile.READING_NEED_CHOICES]
            if new_need in valid_choices:
                profile.reading_need = new_need
                profile.save()
                return Response({
                    'message': 'Preferences updated successfully',
                    'reading_need': profile.reading_need
                })
            else:
                return Response({'error': 'Invalid reading need choice'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'reading_need field is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_smart_settings(request):
    """Returns the CSS UI variables based on the user's profile."""
    try:
        profile = request.user.profile
        need = profile.reading_need
    except ObjectDoesNotExist:
        need = 'general'
        
    settings = {}
    
    if need == 'dyslexia':
        settings = {
            '--font-reading': "'Atkinson Hyperlegible', sans-serif",
            '--font-body': "'Atkinson Hyperlegible', sans-serif",
            '--reading-font-size': "20px",
            '--reading-line-height': "2.0",
            '--reading-letter-spacing': "0.06em",
            '--bg-primary': "#f7f1e3", # Sage/warm background reduces glare
            '--bg-card': "#ffffff",
            '--text-primary': "#2d3436"
        }
    elif need == 'adhd':
        settings = {
            '--font-reading': "'DM Sans', sans-serif",
            '--font-body': "'DM Sans', sans-serif",
            '--reading-font-size': "18px",
            '--reading-line-height': "1.8",
            '--reading-letter-spacing': "0.02em",
            '--bg-primary': "#1e272e", # Dark slate minimizes distractions
            '--bg-card': "#2d3436",
            '--text-primary': "#d2dae2",
            '--focus-mode-default': 'true' # Custom flag for frontend
        }
    elif need == 'visual':
        settings = {
            '--font-reading': "'Syne', sans-serif",
            '--font-body': "'Syne', sans-serif",
            '--reading-font-size': "26px",
            '--reading-line-height': "1.6",
            '--reading-letter-spacing': "0.04em",
            '--bg-primary': "#000000", # Pure black
            '--bg-card': "#111111",
            '--text-primary': "#ffffff" # Pure white high contrast
        }
    else: # general
        settings = {
            '--font-reading': "'Lexend', sans-serif",
            '--font-body': "'Lexend', sans-serif",
            '--reading-font-size': "20px",
            '--reading-line-height': "1.9",
            '--reading-letter-spacing': "0.04em",
            '--bg-primary': "#faf8f3",
            '--bg-card': "#ffffff",
            '--text-primary': "#2c2a26"
        }
        
    return Response({'settings': settings, 'applied_profile': need})
