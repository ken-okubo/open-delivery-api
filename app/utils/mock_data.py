# app/utils/mock_data.py
import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models.menu import Menu
from app.models.category import Category
from app.models.item import Item
from app.models.item_offer import ItemOffer
from app.models.order import Order, OrderItem, OrderCustomer, OrderDelivery, OrderStatus, OrderType

# Function to generate consistent UUIDs based on strings


def generate_uuid(seed):
    return uuid.uuid5(uuid.NAMESPACE_DNS, seed)


async def populate_database():
    # Get a database session
    db = AsyncSession(bind=create_async_engine(
        "postgresql+asyncpg://postgres:postgres@db:5432/ihungry", echo=True
    ))

    try:

        # Create main menu
        main_menu = Menu(
            id=generate_uuid("menu-principal"),
            name="Main Menu",
            description="Our complete menu",
            externalCode="menu-001"
        )
        db.add(main_menu)

        # Create categories
        cat_pizzas = Category(
            id=generate_uuid("cat-pizzas"),
            index=1,
            name="Pizzas",
            description="Our delicious pizzas",
            externalCode="cat-001",
            status="AVAILABLE"
        )
        db.add(cat_pizzas)

        cat_drinks = Category(
            id=generate_uuid("cat-drinks"),
            index=2,
            name="Drinks",
            description="Refreshing beverages",
            externalCode="cat-002",
            status="AVAILABLE"
        )
        db.add(cat_drinks)

        await db.flush()  # To get IDs

        # Create items
        item_cheese_pizza = Item(
            id=generate_uuid("item-cheese-pizza"),
            name="Cheese Pizza",
            description="Traditional cheese pizza with tomato sauce",
            externalCode="item-001",
            status="AVAILABLE",
            unit="UN"
        )
        db.add(item_cheese_pizza)

        item_pepperoni_pizza = Item(
            id=generate_uuid("item-pepperoni-pizza"),
            name="Pepperoni Pizza",
            description="Pepperoni pizza with onions and oregano",
            externalCode="item-002",
            status="AVAILABLE",
            unit="UN"
        )
        db.add(item_pepperoni_pizza)

        item_coke = Item(
            id=generate_uuid("item-coke"),
            name="Coca-Cola 2L",
            description="Coca-Cola soda 2 liters",
            externalCode="item-003",
            status="AVAILABLE",
            unit="UN"
        )
        db.add(item_coke)

        await db.flush()  # To get IDs

        # Create item offers
        offer_cheese = ItemOffer(
            id=generate_uuid("offer-cheese"),
            itemId=item_cheese_pizza.id,
            index=1,
            status="AVAILABLE",
            price={"value": 49.90, "currency": "BRL"}
        )
        db.add(offer_cheese)

        offer_pepperoni = ItemOffer(
            id=generate_uuid("offer-pepperoni"),
            itemId=item_pepperoni_pizza.id,
            index=2,
            status="AVAILABLE",
            price={"value": 54.90, "currency": "BRL"}
        )
        db.add(offer_pepperoni)

        offer_coke = ItemOffer(
            id=generate_uuid("offer-coke"),
            itemId=item_coke.id,
            index=1,
            status="AVAILABLE",
            price={"value": 12.90, "currency": "BRL"}
        )
        db.add(offer_coke)

        # Connect categories with offers
        cat_pizzas.itemOfferId = [offer_cheese.id, offer_pepperoni.id]
        cat_drinks.itemOfferId = [offer_coke.id]

        # Connect menu with categories
        main_menu.categoryId = [cat_pizzas.id, cat_drinks.id]

        # Create orders in different statuses
        orders = []
        for i, status in enumerate([OrderStatus.CREATED, OrderStatus.CONFIRMED, OrderStatus.DISPATCHED, OrderStatus.DELIVERED]):
            # Create order
            order = Order(
                id=generate_uuid(f"order-{i}"),
                display_id=f"OD-100{i}",
                type=OrderType.DELIVERY,
                status=status,
                created_at=datetime.utcnow() - timedelta(hours=i),
                total_amount=62.80 if i % 2 == 0 else 54.90
            )
            db.add(order)
            orders.append(order)

            # Add customer
            customer = OrderCustomer(
                id=generate_uuid(f"customer-{i}"),
                order_id=order.id,
                name=f"Customer {i+1}",
                phone=f"119876543{i}",
                email=f"customer{i+1}@example.com"
            )
            db.add(customer)

            # Add delivery info
            delivery = OrderDelivery(
                id=generate_uuid(f"delivery-{i}"),
                order_id=order.id,
                address={
                    "street": "Example Street",
                    "number": f"{100+i}",
                    "city": "São Paulo",
                    "state": "SP",
                    "postal_code": "01311-000",
                    "complement": f"Apt {i+1}"
                }
            )
            db.add(delivery)

            # Add items to order
            if i % 2 == 0:
                # Order with pizza and coke
                item1 = OrderItem(
                    id=generate_uuid(f"order-item-{i}-1"),
                    order_id=order.id,
                    item_id=item_cheese_pizza.id,
                    name=item_cheese_pizza.name,
                    quantity=1,
                    unit_price=49.90
                )
                db.add(item1)

                item2 = OrderItem(
                    id=generate_uuid(f"order-item-{i}-2"),
                    order_id=order.id,
                    item_id=item_coke.id,
                    name=item_coke.name,
                    quantity=1,
                    unit_price=12.90
                )
                db.add(item2)
            else:
                # Order with just pizza
                item = OrderItem(
                    id=generate_uuid(f"order-item-{i}"),
                    order_id=order.id,
                    item_id=item_pepperoni_pizza.id,
                    name=item_pepperoni_pizza.name,
                    quantity=1,
                    unit_price=54.90
                )
                db.add(item)

        await db.commit()
        print("Database successfully populated!")

    except Exception as e:
        await db.rollback()
        print(f"Error populating database: {e}")
    finally:
        await db.close()

# Run the script
if __name__ == "__main__":
    asyncio.run(populate_database())
