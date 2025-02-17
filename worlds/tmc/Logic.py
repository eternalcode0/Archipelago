from BaseClasses import MultiWorld


def create_connections(multiworld: MultiWorld, player: int):
    dungeon_entrances = []
    for reg1, reg2 in multiworld.worlds[player].dungeon_entrances.items():
        dungeon_entrances.append([reg1, reg2, True, None])


    all_logic = [
        dungeon_entrances,
    ]

    # Create connections
    for logic_array in all_logic:
        for entrance_desc in logic_array:
            region_1 = multiworld.get_region(entrance_desc[0], player)
            region_2 = multiworld.get_region(entrance_desc[1], player)
            is_two_way = entrance_desc[2]
            rule = entrance_desc[3]

            region_1.connect(region_2, None, rule)
            if is_two_way:
                region_2.connect(region_1, None, rule)
