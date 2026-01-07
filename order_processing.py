TAX_RATE = 0.21

SAVE10_RATE = 0.10
SAVE20_RATE_HIGH = 0.20
SAVE20_RATE_LOW = 0.05

VIP_DISCOUNT_HIGH = 50
VIP_DISCOUNT_LOW = 10
VIP_THRESHOLD = 100
SAVE20_THRESHOLD = 200

def parse_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency

def validate_request(user_id, items, currency):
    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    if currency is None:
        currency = "USD"

    if type(items) is not list:
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    validate_items(items)

    return currency

def validate_items(items):
    for it in items:
        if "price" not in it or "qty" not in it:
            raise ValueError("item must have price and qty")
        if it["price"] <= 0:
            raise ValueError("price must be positive")
        if it["qty"] <= 0:
            raise ValueError("qty must be positive")


def calculate_subtotal(items):
    subtotal = 0
    for it in items:
        subtotal += it["price"] * it["qty"]
    return subtotal

def calculate_discount(subtotal, coupon):
    if not coupon:
        return 0
    elif coupon == "SAVE10":
        return int(subtotal * SAVE10_RATE)
    elif coupon == "SAVE20":
        if subtotal >= SAVE20_THRESHOLD:
            return int(subtotal * SAVE20_RATE_HIGH)
        else:
            return int(subtotal * SAVE20_RATE_LOW)
    elif coupon == "VIP":
        if subtotal >= VIP_THRESHOLD:
            return VIP_DISCOUNT_HIGH
        else:
            return VIP_DISCOUNT_LOW
    else:
        raise ValueError("unknown coupon")

def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = parse_request(request)

    currency = validate_request(user_id, items, currency)

    subtotal = calculate_subtotal(items)

    discount = calculate_discount(subtotal, coupon)


    total_after_discount = subtotal - discount
    if total_after_discount < 0:
        total_after_discount = 0

    tax = int(total_after_discount * 0.21)
    total = total_after_discount + tax

    order_id = str(user_id) + "-" + str(len(items)) + "-" + "X"

    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }