# -*- coding: utf-8 -*-
import unittest

from gilded_rose import *


class GildedRoseTest(unittest.TestCase):
    # ~~~~~
    # DAVID's TESTS. 1-3 fail for logical reasons, 4 fails because of syntax
    # 1. LOGICAL - Test that "conjured" items degrade in Quality twice as fast as normal items
    def test_conjure_grade_double_speed(self):
        # Set quality default
        sell_in_default = 5
        quality_default = 50

        # Create the items to test and instantiate a Gilded Rose object
        item_1 = Item("Conjured", sell_in_default, quality_default)
        item_2 = Item("Random", sell_in_default, quality_default)
        items = [ConjuredItem(item_1), GenericGildedRoseItem(item_2)]
        gilded_rose = GildedRose(items)

        # Update the quality and grab the new items
        gilded_rose.update_quality()
        conjured_item = items[0]
        random_item = items[1]

        # Get the difference in both items compared to their original value
        difference_conjured = quality_default - conjured_item.quality
        difference_random = quality_default - random_item.quality

        # Test the difference in conjured quality is double the difference in random item quality
        self.assertEqual(difference_conjured, difference_random * 2)

    # 2. LOGICAL - Test that "Backstage passes" increase in quality by when 10 days or less until concert date
    # Assumes "sell-by" date is the same as the concert date
    def test_backstage_passes_increase_quality_ten_days(self):
        # Default values to test with. Testing days 6-10 because quality should double during these days
        first_day = 6
        last_day = 10
        sell_in_days = [day for day in range(first_day, last_day + 1)]
        quality_default = 50
        expected_difference = 2

        # Create items to test each day
        items = []
        for day in sell_in_days:
            items.append(BackstagePass(Item("Backstage Pass", day, quality_default)))

        # Instantiate GildedRose and update quality
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        # Check that all items have increased by two
        differences = [item.quality - quality_default for item in items]
        for difference in differences:
            self.assertEqual(difference, expected_difference)

    # 3. LOGICAL - Test that "Backstage passes" have a value of zero no matter what their quality is once sell in days
    # goes below zero (the concert has passed)
    def test_backstage_passes_quality_zero_after_concert(self):
        # Set default values to test with to ensure multiple values go to zero
        quality_one = 50
        quality_two = 8
        sell_in_default = -1  # Assumes 0 is day of concert
        new_quality = 0

        # Create the test items
        items = [BackstagePass(Item("Backstage Pass", sell_in_default, quality_one)),
                 BackstagePass(Item("Backstage Pass", sell_in_default,quality_two))]

        # Instantiate GildedRose and update quality
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        # Check both have a quality of 0
        for item in items:
            self.assertEqual(item.quality, new_quality)

    # 4. SYNTAX  - Check that the system updates the SellIn value for an item; this method is not yet implemented
    def test_sell_in_updates(self):
        # Set default values
        default_sell_in = 5
        new_sell_in = 4
        default_quality = 50

        # Create the test object
        item = GenericGildedRoseItem(AgedBrie(Item("Aged Brie", default_sell_in, default_quality)))

        # Apply the method to update SellIn values
        item.update_sell_in()

        # Check that the new sell in value is correct
        self.assertEqual(item.sell_in, new_sell_in)

    # END DAVID'S TESTS
    # ~~~~~~

    # example of test that checks for logical errors
    def test_sulfuras_should_not_decrease_quality(self):
        items = [Sulfuras(Item("Sulfuras", 5, 80))]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        sulfuras_item = items[0]
        self.assertEqual(80, sulfuras_item.quality)
        self.assertEqual(4, sulfuras_item.sell_in)
        self.assertEqual("Sulfuras", sulfuras_item.name)

    # example of test that checks for syntax errors
    def test_gilded_rose_list_all_items(self):
        items = [Sulfuras(Item("Sulfuras", 5, 80))]
        gilded_rose = GildedRose(items)
        all_items = gilded_rose.get_items()
        self.assertEqual(["Sulfuras"], all_items)


if __name__ == '__main__':
    unittest.main()
