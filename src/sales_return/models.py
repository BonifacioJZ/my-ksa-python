import uuid
from django.db import models
from src.sales.models import Sale,Detail

# Create your models here.
class SalesReturn(models.Model):
    id = id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sales_return')
    date = models.DateField(auto_now_add=True)
    penalty = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Sales Return {self.id} - Sale {self.sale.id}"
    class Meta:
        verbose_name = 'Sales Return'
        verbose_name_plural = 'Sales Returns'
        ordering = ['-create_at']

class SalesReturnDetail(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    sales_return = models.ForeignKey(SalesReturn, on_delete=models.CASCADE, related_name='sales_return_detail')
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, related_name='sales_return_detail')
    quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Sales Return Detail {self.id} - Sales Return {self.sales_return.id}"
    class Meta:
        verbose_name = 'Sales Return Detail'
        verbose_name_plural = 'Sales Return Details'
        ordering = ['-create_at']
    def save(self, *args, **kwargs):
        # Calculate the subtotal based on the quantity and the price of the detail
        self.sub_total = self.quantity * self.detail.price
        super().save(*args, **kwargs)