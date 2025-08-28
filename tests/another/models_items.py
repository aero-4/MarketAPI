import datetime
import json
import random



def generate_random_item_data():
    return {
        "title": f"Item {random.randint(1, 1000)}",
        "description": "Описание товара",
        "count_all": str(random.randint(1, 50)),
        "price": str(round(random.uniform(100, 5000), 2)),
        "discount": str(round(random.uniform(0, 50), 2)),
        "cat": "electronics",
        "sub_cat": "smartphone",
        "params": json.dumps({
            "brand": str(random.randint(1, 100)),
            "model": str(random.randint(1, 100)),
            "price": str(random.randint(100, 5000)),
            "release_date": str(datetime.date.today()),
            "screen_size": round(random.uniform(5.0, 7.0), 1),
            "battery_capacity": random.randint(2000, 5000),
            "ram": random.choice([4, 8, 16]),
            "storage": random.choice([32, 64, 128, 256]),
            "camera_megapixels": round(random.uniform(8.0, 108.0), 1),
            "os": random.choice(["Android", "Apple"]),
            "connectivity": random.sample(["5G", "Wifi", "Bluetooth", "NFC"], k=2),
        }),
    }


print(generate_random_item_data())
