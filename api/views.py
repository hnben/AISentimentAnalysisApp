from django.http import JsonResponse

# Create your views here.

def get_hi(request):
    
    query_params = request.GET
    
    data = {
        'message': "Hello, this is a http test",
        'status': 'success'
    }
    
    return JsonResponse(data)

