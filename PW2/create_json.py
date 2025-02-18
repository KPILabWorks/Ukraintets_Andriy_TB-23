# Практична робота 2
# Векторизоване зчитування JSON. Зчитайте великий JSON-файл у Pandas через pd.read_json() та розпакуйте вкладені структури.
import json
import random
import argparse

NUM_RECORDS = 10000

def generate_nested_data():
    return {
        "id": random.randint(1, 1000),
        "name": f"Item-{random.randint(1, 100)}",
        "details": {
            "category": random.choice(["Shoes", "Cap", "Jacket", "Pants"]),
            "price": round(random.uniform(10, 500), 2),
            "availability": random.choice([True, False])
        }
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate JSON file")
    parser.add_argument("--num_records", type=int, default=10000, help="Number of records to generate")
    parser.add_argument("--path", type=str, default='data.json', help="Output JSON file path")
    args = parser.parse_args()

    data = [generate_nested_data() for _ in range(args.num_records)]

    with open(args.path, "w") as f:
        json.dump(data, f, indent=4)
