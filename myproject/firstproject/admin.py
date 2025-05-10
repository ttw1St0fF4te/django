from django.contrib import admin
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

from .models import Product, Category, Tag

def setup_user_groups():
    # Create groups
    superuser_group, _ = Group.objects.get_or_create(name='Суперпользователь')
    seller_group, _ = Group.objects.get_or_create(name='Продавец')
    admin_group, _ = Group.objects.get_or_create(name='Администратор')
    buyer_group, _ = Group.objects.get_or_create(name='Покупатель')

    # Assign permissions to groups
    product_ct = ContentType.objects.get_for_model(Product)
    category_ct = ContentType.objects.get_for_model(Category)
    tag_ct = ContentType.objects.get_for_model(Tag)

    # Helper function to safely get or create permissions
    def get_or_create_permission(codename, name, content_type):
        try:
            return Permission.objects.get(codename=codename, content_type=content_type)
        except Permission.DoesNotExist:
            return Permission.objects.create(codename=codename, name=name, content_type=content_type)

    # Seller permissions
    seller_permissions = [
        get_or_create_permission('add_product', 'Can add product', product_ct),
        get_or_create_permission('change_product', 'Can change product', product_ct),
        get_or_create_permission('delete_product', 'Can delete product', product_ct),
    ]
    seller_group.permissions.set(seller_permissions)

    # Admin permissions
    admin_permissions = [
        get_or_create_permission('add_product', 'Can add product', product_ct),
        get_or_create_permission('change_product', 'Can change product', product_ct),
        get_or_create_permission('delete_product', 'Can delete product', product_ct),
        get_or_create_permission('add_category', 'Can add category', category_ct),
        get_or_create_permission('change_category', 'Can change category', category_ct),
        get_or_create_permission('delete_category', 'Can delete category', category_ct),
        get_or_create_permission('add_tag', 'Can add tag', tag_ct),
        get_or_create_permission('change_tag', 'Can change tag', tag_ct),
        get_or_create_permission('delete_tag', 'Can delete tag', tag_ct),
    ]
    admin_group.permissions.set(admin_permissions)

    # Buyer permissions
    buyer_permissions = [
        get_or_create_permission('view_product', 'Can view product', product_ct),
    ]
    buyer_group.permissions.set(buyer_permissions)

setup_user_groups()