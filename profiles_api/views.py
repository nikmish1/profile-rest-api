from rest_framework.views import APIView
from rest_framework.response import Response


# expect function for differnt type request can be made to APIVIew
class HelloApiView(APIView):
    """Test API View"""


    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
                "Uses HTTP method as function(get, post, patch, put, delete)",
                "Is similar to Django View",
                "Gives you most control over your application logic",
                "Is mapped manually to URLs"
        ]

        return Response({'message':'Hello!', 'an_apiview': an_apiview})
