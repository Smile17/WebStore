from django.shortcuts import render , redirect , HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView

from store.models import Category, Product, Order, OrderLine


def save_to_cart(request):
    product = request.POST.get('product')
    remove = request.POST.get('remove')
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product)
        if quantity:
            if remove:
                if quantity <= 1:
                    cart.pop(product)
                else:
                    cart[product] = quantity - 1
            else:
                cart[product] = quantity + 1

        else:
            cart[product] = 1
    else:
        cart = {}
        cart[product] = 1

    request.session['cart'] = cart
    print('cart', request.session['cart'])

# Create your views here.
class Index(View):
    def post(self, request):
        save_to_cart(request)
        return redirect('home')

    def get(self, request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')


def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_category_id(categoryID)
    else:
        products = Product.get_all_products()

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)


class ProductDetailView(DetailView):
    # specify the model to use
    model = Product
    template_name = 'product-detail.html'
    context_object_name = 'product'

    def post(self, request, pk):
        save_to_cart(request)
        product_id = request.POST.get('product')
        return redirect('detail', pk=product_id)


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request, 'cart.html', {'products': products})


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, cart, products)

        order = Order(address=address,
                      phone=phone,
                      status="Confirmed")
        order.save()

        for product in products:
            print(cart.get(str(product.id)))
            line = OrderLine(order_id=order,
                             product=product,
                             quantity=cart.get(str(product.id)),
                             price=product.price)
            line.save()
        request.session['cart'] = {}

        return render(request, 'check-out.html')

    def get(self, request):
        return render(request, 'check-out.html')
