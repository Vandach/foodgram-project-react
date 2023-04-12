# from django import template
# from food.models import Category

# register = template.Library()


# @register.simple_tag(name='get_cats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)


# @register.inclusion_tag('list_categories.html')
# def show_categories(sort=None, cat_selected=0):
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)

#     return {'cats': cats, 'cat_selected': cat_selected}
