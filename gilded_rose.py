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
    """
    Parent class all Gilded Rose items will inherit from
    """
    def __init__(self, item):
        super().__init__(item.name, item.sell_in, item.quality)
        self.single_sell_in_reduction = 1
        self.single_quality_reduction = 1
        self.last_sell_in_days = 0
        self.max_quality = 50

    def reduce_sell_in(self):
        """
        Reduces the sell in value
        :return: The new sell_in value
        """
        self.sell_in -= self.single_sell_in_reduction
        return self.sell_in

    def reduce_quality(self):
        """
        Reduces the quality once
        :return: The new quality
        """
        # Prevent quality from being reduced below 0
        self.quality = max(0, self.quality - self.single_quality_reduction)
        return self.quality

    def set_max_quality(self):
        """
        Makes sure that quality is never above the maximum
        :return: The quality value of the item after checking
        """
        self.quality = min(self.quality, self.max_quality)
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

        # Return updated quality
        return self.quality


class GenericGildedRoseItem(GildedRoseItem):
    """
    Class for generic Gilded Rose items
    """
    def __init__(self, item):
        super().__init__(item)


class GildedRose(object):

    def __init__(self, items: list[Item]):
        # DO NOT CHANGE THIS ATTRIBUTE!!!
        self.items = items

    def update_quality(self):
        for item in self.items:
            this_item = GenericGildedRoseItem(item)
            this_item.update_quality()
            item.quality = this_item.quality

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

    # Handle special rules
    # Each item has its own special rule handler that handle special rules refers to
