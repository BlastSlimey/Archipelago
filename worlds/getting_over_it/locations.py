from BaseClasses import Location

instant_spots = ["Tree", "Paddle"]
early_spots = ["Concrete Pipe", "Barrels", "Cup", "Trash", "First Lamp", "Second Lamp", "Bathtub", "Grill",
               "Kids Slide"]
midgame_spots = ["Pliers", "Child", "Car", "Staircase", "Security Cam", "Toilet", "Orange Table", "Gargoyle",
                 "Church Top", "Hedge", "Hat", "Anvil"]
late_spots = ["Telephone Booth", "Snake Ride", "Bucket", "Landing Stage", "Ice Mountain", "Shopping Cart", "Temple",
              "Antenna Top"]
float_only_spots = ["Big Balloon", "Sexy Hiking Character"]

spots_list = instant_spots + early_spots + midgame_spots + late_spots + float_only_spots
completions_list = [f"Got Over It #{count}" for count in range(1, 10)]

locations_list = spots_list + completions_list


class GOILocation(Location):
    game = "Getting Over It"
