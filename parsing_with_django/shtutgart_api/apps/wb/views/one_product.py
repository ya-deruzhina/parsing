from rest_framework.views import APIView
from rest_framework.response import Response
from shtutgart_api.tasks import save_product_inf_task

# Get data 'id' of product 
class GetProductInfView(APIView):
    def post (self,request):
        id_product = request.POST.get('id_product')
        save_product_inf_task.delay(id_product)
        return Response({"status":"loading"})
