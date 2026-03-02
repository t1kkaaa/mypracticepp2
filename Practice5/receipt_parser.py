#2.2 exercise
import re
import json

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    items = []
    product_pattern = re.compile(r'\d+\.\n(.*?)\n.*?\n(\d+,\d{2})\nСтоимость', re.MULTILINE)
    
    matches = product_pattern.findall(content)
    
    total_calculated = 0.0
    for name, price_str in matches:
        price = float(price_str.replace(',', '.'))
        items.append({
            "name": name.strip(),
            "price": price
        })
        total_calculated += price

    date_time_match = re.search(r'(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2})', content)
    date_time = date_time_match.group(1) if date_time_match else "Не найдено"

    payment_method_match = re.search(r'(Карта|Наличные|Оплата\s+\w+)', content, re.IGNORECASE)
    payment_method = payment_method_match.group(1) if payment_method_match else "Карта" 

    result = {
        "items": items,
        "total_amount": round(total_calculated, 2),
        "date_time": date_time,
        "payment_method": payment_method
    }

    return result

if __name__ == "__main__":
    parsed_data = parse_receipt('raw.txt')
    
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))