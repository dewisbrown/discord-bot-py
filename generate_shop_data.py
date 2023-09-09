import csv
import json

rarity_counts = {
    'Legendary': 1,
    'Exotic': 1,
    'Very Rare': 1,
    'Rare': 1,
    'Uncommon': 2,
    'Common': 3
}

# Dictionary of arrays for each rarity
categorized_items = {rarity: [] for rarity in rarity_counts}

# Categorize items based on rarity
with open('./shop.csv', 'r', encoding='utf-8', newline='') as file:
    reader = csv.DictReader(file)

    for item in reader:
        item_name = item['item_name']
        rarity = item['rarity']
        value = item['value']
        categorized_items[rarity].append({'item_name': item_name, 'rarity': rarity, 'value': value})

# Write to JSON file so it can be read in bot command
with open('./categorized_items.json', 'w', encoding='utf-8') as json_file:
    json.dump(categorized_items, json_file)
