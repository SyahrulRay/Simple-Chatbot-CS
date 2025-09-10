from app.db import Message
from app.db import SessionLocal, Order, Product

def get_last_k_messages(conversation_id:int, k:int=3):
    with SessionLocal() as s:
        rows = s.query(Message).filter(Message.conversation_id==conversation_id)\
               .order_by(Message.created_at.desc()).limit(k*2).all()
        return list(reversed(rows))


def get_warranty_policy(product_id:str):
    info = get_product_info(product_id)
    return info["warranty_policy"] if info else None


def get_order_status(order_id: str):
    with SessionLocal() as db:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        product = db.query(Product).filter(Product.id == order.product_id).first()
        return {
            "id": order.id,
            "status": order.status,
            "courier": order.courier,
            "tracking_number": order.tracking_number,
            "last_update": order.last_update,
            "name": product.name if product else "Produk tidak ditemukan"
        }

def get_product_info(product_id: str):
    with SessionLocal() as db:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        return {
            "id": product.id,
            "name": product.name,
            "features": product.features,
            "warranty_policy": product.warranty_policy
        }