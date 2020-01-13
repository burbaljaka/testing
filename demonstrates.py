
class Item(models.Model):
    name = models.CharField(max_length=200)
    detail_quantity = models.BigIntegerField(blank=True)
    drawing_quantity = models.BigIntegerField(blank=True)
    weight = models.BigIntegerField(blank=True)
    value = models.DecimalField(decimal_places=2, max_digits=20, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    number = models.BigIntegerField(blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True, through='ItemOrder')
    contract = models.BigIntegerField(blank=True, null=True)
    contract_value = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_to_pay = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    ship_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def total(self):
        return self.productorder_set.aggregate(price_sum=Sum(F('quantity')*F('item__value')))['price_sum']

    def __str__(self):
        return str(self.number)


class ItemOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.BigIntegerField(default=1)

    def __str__(self):
        return str(self.id) + ' Order: ' + str(self.order)


class Task(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    is_complete = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200, blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
