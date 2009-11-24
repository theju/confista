from menu.models import Menu_Item

def menu(request):
    return {"menu_items": Menu_Item.objects.iterator()}
