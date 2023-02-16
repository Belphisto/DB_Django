from decimal import Decimal
from django.conf import settings
from store.models import Manga

class Cart(object):
    def __init__(self, request):
        """Cart initialization"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #save in session empty cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """Get all manga in cart"""
        manga_ids = self.cart.keys()
        all_manga = Manga.objects.filter(id__in=manga_ids)
        cart = self.cart.copy()
        for manga in all_manga:
            cart[str(manga.id)]['manga'] = manga
            print(manga)
        print(cart.values())
        for item in cart.values():
            item['price'] = (Decimal(item['price']))
            item['total_price'] = item['price'] *Decimal(item['quantity'])
            item['price'] = round(item['price'], 2)
            item['total_price'] = round(item['total_price'], 2)
            print(item)
            yield item

    def __len__(self):
        """Return total quantity in cart"""
        summ = 0
        for item in self.cart.values():
            summ+= int(item['quantity'])
        summ = round(summ, 2)
        print(summ)
        return summ

    def add(self, manga, quantity=1, update_quantity=False):
        """Add Manga in cart or change its quantity"""
        manga_id = str(manga.id)
        if manga_id not in self.cart:
            self.cart[manga_id] = {'quantity': 0, 'price': str(manga.price)}
        if update_quantity:
            self.cart[manga_id]['quantity'] = quantity
        else:
            self.cart[manga_id]['quantity'] += quantity
        self.save()

    def save(self):
        #Mark session as modified
        self.session.modified = True

    def remove(self, manga):
        "Remove manga from cart"
        manga_id = str(manga.id)
        if manga_id in self.cart:
            del self.cart[manga_id]
            self.save()

    def get_total_price(self):
        summ = 0
        for item in self.cart.values():
            summ += Decimal(item['price'])*Decimal(item['quantity'])
        summ = round(summ, 2)
        print(summ)
        return summ

    def clear(self):
        """Clear cart"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
