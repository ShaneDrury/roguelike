from health_potion import HealthPotion

all_items = {'health_potion': HealthPotion}


def get_item(name):
    return all_items[name]
