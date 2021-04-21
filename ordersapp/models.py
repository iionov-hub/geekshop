from django.db import models
from django.conf import settings
from mainapp.models import Product

# Create your models here.
class Order(models.Model):
    #Создаем статусы заказов
    FORMING = "FM"
    SENT_TO_PROCEED = "STP"
    PAID = "PD"
    PROCEEDED = "PRD"
    READY = "RDY"
    CANCEL = "CNC"

    #набор вариантов
    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменён')
    )

    #юзера берем из settings.AUTH_USER_MODEL (\geekshop\settings.py)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)

    status = models.CharField(
        choices=ORDER_STATUS_CHOICES,
        verbose_name='статус',
        max_length=3,
        default=FORMING
    )

    is_active = models.BooleanField(verbose_name='активен', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ {self.id}'

    def get_total_quantity(self):
        #получаем список заказов
        items = self.orderitems.select_related()
        #возвращаем сумму заказов
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        #возвращаем длину
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        #цену умножаем на количество заказов
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    # переопределяем метод, удаляющий объект
    def delete(self):
        #собираем все заказы
        for item in self.orderitems.select_related():
            #корректируем остатки продуктов на складе
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name="orderitems",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='продукт',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity


    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()


    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(self.__class__, self).delete()
