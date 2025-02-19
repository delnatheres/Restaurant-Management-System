from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json

# Configure the Gemini API
genai.configure(api_key='YOUR_GEMINI_API_KEY')
model = genai.GenerativeModel('gemini-pro')

@csrf_exempt
def analyze_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            review_text = data.get('review')
            
            # Prompt for Gemini
            prompt = f"""
            Analyze the following restaurant review and provide:
            1. Overall sentiment (Positive/Negative/Neutral)
            2. Key points from the review
            3. Suggestions for improvement if applicable

            Review: {review_text}
            
            Format the response as JSON with the following structure:
            {{
                "sentiment": "sentiment here",
                "keyPoints": "key points here",
                "suggestions": "suggestions here"
            }}
            """

            # Get response from Gemini
            response = model.generate_content(prompt)
            analysis = json.loads(response.text)

            return JsonResponse(analysis)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400) 