import random
from django.core.mail import send_mail
from store.serializers import ProductInstanceSerializer
from store.models import Order, Product
from django.template.loader import render_to_string


def generate_random_six_character_string():
    """ Examples would be: 1a45g3, 3c32df..."""
    to_ret = []
    for i in range(6):
        num = random.randint(0,61)
        if num < 10:
            to_ret.append(str(num))
        else:
            to_ret.append(num_to_char[num])

    return "".join(to_ret)


num_to_char = {
    10:"a",
    11:"b",
    12:"c",
    13:"d",
    14:"e",
    15:"f",
    16:"g",
    17:"h",
    18:"i",
    19:"j",
    20:"k",
    21:"l",
    22:"m",
    23:"n",
    24:"o",
    25:"p",
    26:"q",
    27:"r",
    28:"s",
    29:"t",
    30:"u",
    31:"v",
    32:"w",
    33:"x",
    34:"y",
    35:"z",
    36:"A",
    37:"B",
    38:"C",
    39:"D",
    40:"E",
    41:"F",
    42:"G",
    43:"H",
    44:"I",
    45:"J",
    46:"K",
    47:"L",
    48:"M",
    49:"N",
    50:"O",
    51:"P",
    52:"Q",
    53:"R",
    54:"S",
    55:"T",
    56:"U",
    57:"V",
    58:"W",
    59:"X",
    60:"Y",
    61:"Z",
}


def send_order_email(dj_order_id, to_email):
    order = Order.objects.get(dj_order_id=dj_order_id)

    info = []
    for cart_product_instance in order.cart_product_instances.all():
        stuff = {}
        product = cart_product_instance.product_instance.product
        size = cart_product_instance.product_instance.size

        stuff['title'] = product.title
        stuff['quantity'] = cart_product_instance.quantity
        stuff['size'] = size

        info.append(stuff)

    data = {
        "order_id": order.dj_order_id,
        "total": order.total,
        "product_instances": info,
    }

    msg_plain = render_to_string('store/email.txt', data)
    msg_html = render_to_string('store/email.html', data)

    send_mail('order', msg_plain, 'orders@store.danmallon.com', [to_email], html_message=msg_html)
