from .category_controller import register_route as category_route
from .products_controller import register_route as product_route
from .seller_controller import register_route as seller_route
from .user_controller import register_route as user_route
from .cart_controller import register_route as cart_route
from .order_controller import register_route as orders_route
def register_all_routes(app):
    category_route(app)
    product_route(app)
    seller_route(app)
    user_route(app)
    cart_route(app)
    orders_route(app)

# Register routes with base path
    base_routes = {
        '/product': product_route,
        '/category': category_route,
        # '/product_media': register_product_media_routes,
        # '/media_type': register_media_type_routes
    }

    