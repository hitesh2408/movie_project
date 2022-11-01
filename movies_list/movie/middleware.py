from .models import RequestCount

class RequestCountMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
        
    def process_request(self, request):
        count = RequestCount.objects.get(id=1)        
        count.count += 1
        count.save()

