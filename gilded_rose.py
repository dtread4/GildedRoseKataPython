# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Item:
    """ DO NOT CHANGE THIS CLASS!!!"""

    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class GildedRoseItem(Item):
    def __init__(self, item):
        super().__init__(item.name, item.sell_in, item.quality)
        self.single_sell_in_reduction = 1
        self.single_quality_reduction = 1
        self.last_sell_in_days = 0
        self.min_quality = 0
        self.max_quality = 50

    def reduce_sell_in(self):
        """
        Reduces the sell in value
        :return: The new sell_in value
        """
        self.sell_in -= self.single_sell_in_reduction
        return self.sell_in

    def check_min_quality(self):
        """
        Checks that quality is not below the minimum value
        :return: The quality value of the item after checking
        """
        self.quality = max(self.quality, self.min_quality)
        return self.quality

    def check_max_quality(self):
        """
        Makes sure that quality is never above the maximum
        :return: The quality value of the item after checking
        """
        self.quality = min(self.quality, self.max_quality)
        return self.quality

    def reduce_quality(self):
        """
        Reduces the quality once
        :return: The new quality
        """
        # Prevent quality from being reduced below 0
        self.quality = self.quality - self.single_quality_reduction
        self.check_min_quality()
        return self.quality

    def update_sell_in(self):
        """
        Updates the sell in value of an item
        :return: The new sell in value
        """
        self.reduce_sell_in()
        return self.sell_in

    def update_quality(self):
        """
        Handles generic item's quality update algorithm
        :return: The new item quality
        """
        # Update the sell in value
        self.update_sell_in()

        # Reduce quality
        self.reduce_quality()

        # If sell in value is now less than 0 (past sell by date), reduce quality again
        if self.sell_in < self.last_sell_in_days:
            self.reduce_quality()

        # Check that max quality is not violated
        self.check_max_quality()

        # Return updated quality
        return self.quality


class GenericGildedRoseItem(GildedRoseItem):
    def __init__(self, item):
        super().__init__(item)


class AgedBrie(GildedRoseItem):
    def __init__(self, item):
        super().__init__(item)
        self.quality_increase = 1

    def update_quality(self):
        """
        Updates the quality. For Aged Brie, this means adding one
        :return: The updated quality value
        """
        self.quality += self.quality_increase
        self.check_max_quality()
        return self.quality


class BackstagePass(GildedRoseItem):
    def __init__(self, item):
        super().__init__(item)
        self.default_sell_value = 1
        self.bonus_sell_value = 2
        self.bonus_2_sell_value = 3
        self.first_bonus_day = 10
        self.second_bonus_day = 5
        self.min_quality = 0

    def update_quality(self):
        """
        Updates the quality. For Backstage Passes, this means increasing by one generally,
        but this may change depending on how many days are left until the concert
        :return: The updated quality value
        """
        if self.sell_in > self.first_bonus_day:
            self.quality += self.default_sell_value
        elif self.second_bonus_day < self.sell_in <= self.first_bonus_day:
            self.quality += self.bonus_sell_value
        elif 0 <= self.sell_in <= self.second_bonus_day:
            self.quality += self.bonus_2_sell_value
        else:  # sell in must be less than 0
            self.quality = self.min_quality
        return self.quality


class Sulfuras(GildedRoseItem):
    def __init__(self, item):
        super().__init__(item)
        self.quality = 80
        self.min_quality = self.quality
        self.max_quality = self.quality
        self.single_quality_reduction = 0


class ConjuredItem(GildedRoseItem):
    def __init__(self, item):
        super().__init__(item)
        self.quality_reduction_multiple = 2
        self.single_quality_reduction = self.single_quality_reduction * self.quality_reduction_multiple


class GildedRose(object):

    def __init__(self, items: list[Item]):
        # DO NOT CHANGE THIS ATTRIBUTE!!!
        self.items = items

    def get_items(self):
        """
        Creates a list of all item names in the GildedRose object
        :return: The list of all item name Strings
        """
        all_item_names = []
        for item in self.items:
            all_item_names.append(item.name)
        return all_item_names

    def update_quality(self):
        for item in self.items:
            item.update_quality()

# # OLD
# if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
#     if item.quality > 0:
#         if item.name != "Sulfuras, Hand of Ragnaros":
#             item.quality = item.quality - 1
# else:
#     if item.quality < 50:
#         item.quality = item.quality + 1
#         if item.name == "Backstage passes to a TAFKAL80ETC concert":
#             if item.sell_in < 11:
#                 if item.quality < 50:
#                     item.quality = item.quality + 1
#             if item.sell_in < 6:
#                 if item.quality < 50:
#                     item.quality = item.quality + 1
# if item.name != "Sulfuras, Hand of Ragnaros":
#     item.sell_in = item.sell_in - 1
# if item.sell_in < 0:
#     if item.name != "Aged Brie":
#         if item.name != "Backstage passes to a TAFKAL80ETC concert":
#             if item.quality > 0:
#                 if item.name != "Sulfuras, Hand of Ragnaros":
#                     item.quality = item.quality - 1
#         else:
#             item.quality = item.quality - item.quality
#     else:
#         if item.quality < 50:
#             item.quality = item.quality + 1
