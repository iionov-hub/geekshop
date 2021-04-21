from basketapp.models import Basket

def baskets(request):
   baskets = []
   if request.user.is_authenticated:
       baskets = Basket.objects.filter(user=request.user)
   return {
       'baskets': baskets,
   }