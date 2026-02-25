from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from deep_translator import GoogleTranslator

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def translate_text(request):
    text = request.data.get('text', '')
    target_lang = request.data.get('target', 'kn')

    if not text:
        return Response({'error': 'No text provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        # Use deep-translator to convert English to target
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return Response({'translated_text': translated})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
