from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование категории')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование тега')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_deleted = models.BooleanField(default=False, verbose_name='Удалён')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, verbose_name='Номер заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    delivery_address = models.CharField(max_length=200, verbose_name='Адрес доставки')
    customer_phone = models.CharField(max_length=20, verbose_name='Телефон клиента')
    customer_name = models.CharField(max_length=100, verbose_name='Имя клиента')

    products = models.ManyToManyField(Product, through='OrderItem', verbose_name='Товары')

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка')

    def __str__(self):
        return f"{self.product.name} в {self.order.order_number}"

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
