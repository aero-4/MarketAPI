from src.admins.router import admin_router
from src.auth.router import auth_router
from src.cart.router import cart_router
from src.items.router import items_router
from src.orders.router import order_router
from src.payments.router import payment_router
from src.questions.router import question_router
from src.reviews.router import reviews_router
from src.search.router import search_router
from src.session.router import session_router
from src.user.router import user_router
from src.wish.router import wish_router

routers = [
    items_router,
    session_router,
    auth_router,
    search_router,
    reviews_router,
    admin_router,
    user_router,
    wish_router,
    question_router,
    order_router,
    cart_router,
    payment_router
]
