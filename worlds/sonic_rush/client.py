from typing import TYPE_CHECKING, Set, Dict

from NetUtils import ClientStatus
import asyncio

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .locations import location_lookup_by_name
from .items import item_lookup_by_id

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class SonicRushClient(BizHawkClient):
    game = "Sonic Rush"
    system = "NDS"
    patch_suffix = ".aprush"
    local_checked_locations: Set[int]
    goal_flag: int
    ram_mem_domain = "Main RAM"
    goal_complete = False
    outside_deathlink = 0
    deathlink_sender = ""
    deathlink_message: str = ""
    received_items_count: int = 0

    received_offset = 0x2c475e
    zone_unlocks_sonic_offset = 0x2c4760
    zone_unlocks_blaze_offset = 0x2c4761
    progressive_level_unlocks_sonic_offset = 0x2c4762
    progressive_level_unlocks_blaze_offset = 0x2c4763
    special_stages_offset = 0x2c4764
    chaos_emeralds_offset = 0x2C468F
    sol_emeralds_offset = 0x2c4765
    emeralds_buffer_offset = 0x2c4588
    boss_flags_offset = 0x2c4766
    sidekick_showing_offset = 0x2c4767
    # savedata_initialized_offset = 0x2c476f
    selected_character_offset = 0x2c4560
    maybe_gamestate_offset = 0x2c45b4
    sonic_storyprog_offset = 0x2c468C
    level_scores_sonic_offset = 0x2c4690
    level_scores_blaze_offset = 0x2c46e8
    extra_lives_sonic_offset = 0x2C468E
    extra_lives_blaze_offset = 0x2C46E6

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.seed_verify = False

    async def receive_set_flag_in_byte(self, address: int, ctx: "BizHawkClientContext", to_be_set: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_bits = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, (current_bits | (1 << to_be_set)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain
            )],
        )

    async def receive_unset_flag_in_byte(self, address: int, ctx: "BizHawkClientContext", to_be_unset: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_bits = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, (current_bits & ~(1 << to_be_unset)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain
            )],
        )

    async def receive_increase_byte(self, address: int, ctx: "BizHawkClientContext"):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_byte = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, min(current_byte + 1, 255).to_bytes(length=1, byteorder="little"), self.ram_mem_domain
            )],
        )

    async def receive_halve_byte(self, address: int, ctx: "BizHawkClientContext"):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        current_byte = int.from_bytes(read_state[0])
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, (current_byte // 2).to_bytes(length=1, byteorder="little"), self.ram_mem_domain
            )],
        )

    async def receive_set_half_word(self, address: int, ctx: "BizHawkClientContext", to_be_set: int) -> None:
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, to_be_set.to_bytes(length=2, byteorder="little"),self.ram_mem_domain
            )]
        )

    async def receive_is_byte(self, address: int, ctx: "BizHawkClientContext", value: int):
        read_state = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (address, 1, self.ram_mem_domain),
            ]
        )
        read_byte = int.from_bytes(read_state[0])
        return read_byte == value

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1
        self.seed_verify = False
        if not await bizhawk.get_hash(ctx.bizhawk_ctx) == "DB9D446F8AB4A2799246FE77CC934CC649A1CE61":
            logger.warn("The patched rom is different from what was expected. "
                        "Please check you vanilla rom file and patch again.")
            return False
        return True

    def on_package(self, ctx, cmd, args) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]
        if cmd != "Bounced":
            return
        if "tags" not in args:
            return
        if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
            pass

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        # from CommonClient import logger
        try:
            if ctx.slot_data is None:
                return

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx, [
                    (self.sonic_storyprog_offset, 1, self.ram_mem_domain),
                ]
            )

            # Return if save data not yet initialized, else it's 0xff, and that's bad
            # Also after booting the entire memory will be 0x00, which is also not good for receiving items
            if int.from_bytes(read_state[0]) == 0:
                return

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (self.received_offset, 2, self.ram_mem_domain),
                    (self.special_stages_offset, 1, self.ram_mem_domain),
                    (self.boss_flags_offset, 1, self.ram_mem_domain),
                    (self.level_scores_sonic_offset, 84, self.ram_mem_domain),
                    (self.level_scores_blaze_offset, 84, self.ram_mem_domain),
                ]
            )

            received_in_sav = int.from_bytes(read_state[0], "little")
            special_stages_checks = int.from_bytes(read_state[1])
            boss_flags_checks = int.from_bytes(read_state[2])
            level_scores_sonic: Dict[int, Dict[int, int]] = {}
            level_scores_blaze: Dict[int, Dict[int, int]] = {}
            for zone in range(7):
                level_scores_sonic[zone] = {}
                level_scores_blaze[zone] = {}
                for act in range(3):
                    offset = zone*12+act*4
                    level_scores_sonic[zone][act] = int.from_bytes(read_state[3][offset:(offset+4)], "little")
                    level_scores_blaze[zone][act] = int.from_bytes(read_state[4][offset:(offset+4)], "little")

            if ctx.items_received:
                for index in range(min(self.received_items_count, received_in_sav), len(ctx.items_received)):
                    network_item = ctx.items_received[index]
                    name = item_lookup_by_id[network_item.item]
                    match name:
                        # Blaze's zone unlock bits have to stay in numerical order here,
                        # because of the rom already converting current location to zone on flag checking
                        case "Unlock Zone 1 (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 0)
                        case "Unlock Zone 2 (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 1)
                        case "Unlock Zone 3 (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 2)
                        case "Unlock Zone 4 (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 3)
                        case "Unlock Zone 5 (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 4)
                        case "Unlock Zone 6 (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 5)
                        case "Unlock Zone 7 (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 6)
                        case "Unlock F-Zone (Sonic)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_sonic_offset, ctx, 7)
                        case "Unlock Zone 1 (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 0)
                        case "Unlock Zone 2 (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 1)
                        case "Unlock Zone 3 (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 2)
                        case "Unlock Zone 4 (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 3)
                        case "Unlock Zone 5 (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 4)
                        case "Unlock Zone 6 (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 5)
                        case "Unlock Zone 7 (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 6)
                        case "Unlock F-Zone (Blaze)":
                            await self.receive_set_flag_in_byte(self.zone_unlocks_blaze_offset, ctx, 7)
                        case "Progressive Level Select (Sonic)":
                            if index >= received_in_sav:
                                await self.receive_increase_byte(self.progressive_level_unlocks_sonic_offset, ctx)
                        case "Progressive Level Select (Blaze)":
                            if index >= received_in_sav:
                                await self.receive_increase_byte(self.progressive_level_unlocks_blaze_offset, ctx)
                        case "Red Chaos Emerald":
                            if await self.receive_is_byte(self.maybe_gamestate_offset, ctx, 3):
                                if await self.receive_is_byte(self.selected_character_offset, ctx, 0):
                                    await self.receive_set_flag_in_byte(self.emeralds_buffer_offset, ctx, 0)
                            await self.receive_set_flag_in_byte(self.chaos_emeralds_offset, ctx, 0)
                        case "Blue Chaos Emerald":
                            if await self.receive_is_byte(self.maybe_gamestate_offset, ctx, 3):
                                if await self.receive_is_byte(self.selected_character_offset, ctx, 0):
                                    await self.receive_set_flag_in_byte(self.emeralds_buffer_offset, ctx, 1)
                            await self.receive_set_flag_in_byte(self.chaos_emeralds_offset, ctx, 1)
                        case "Yellow Chaos Emerald":
                            if await self.receive_is_byte(self.maybe_gamestate_offset, ctx, 3):
                                if await self.receive_is_byte(self.selected_character_offset, ctx, 0):
                                    await self.receive_set_flag_in_byte(self.emeralds_buffer_offset, ctx, 2)
                            await self.receive_set_flag_in_byte(self.chaos_emeralds_offset, ctx, 2)
                        case "Green Chaos Emerald":
                            if await self.receive_is_byte(self.maybe_gamestate_offset, ctx, 3):
                                if await self.receive_is_byte(self.selected_character_offset, ctx, 0):
                                    await self.receive_set_flag_in_byte(self.emeralds_buffer_offset, ctx, 3)
                            await self.receive_set_flag_in_byte(self.chaos_emeralds_offset, ctx, 3)
                        case "White Chaos Emerald":
                            if await self.receive_is_byte(self.maybe_gamestate_offset, ctx, 3):
                                if await self.receive_is_byte(self.selected_character_offset, ctx, 0):
                                    await self.receive_set_flag_in_byte(self.emeralds_buffer_offset, ctx, 4)
                            await self.receive_set_flag_in_byte(self.chaos_emeralds_offset, ctx, 4)
                        case "Turquoise Chaos Emerald":
                            if await self.receive_is_byte(self.maybe_gamestate_offset, ctx, 3):
                                if await self.receive_is_byte(self.selected_character_offset, ctx, 0):
                                    await self.receive_set_flag_in_byte(self.emeralds_buffer_offset, ctx, 5)
                            await self.receive_set_flag_in_byte(self.chaos_emeralds_offset, ctx, 5)
                        case "Purple Chaos Emerald":
                            if await self.receive_is_byte(self.maybe_gamestate_offset, ctx, 3):
                                if await self.receive_is_byte(self.selected_character_offset, ctx, 0):
                                    await self.receive_set_flag_in_byte(self.emeralds_buffer_offset, ctx, 6)
                            await self.receive_set_flag_in_byte(self.chaos_emeralds_offset, ctx, 6)
                        case "Red Sol Emerald":
                            await self.receive_set_flag_in_byte(self.sol_emeralds_offset, ctx, 0)
                        case "Blue Sol Emerald":
                            await self.receive_set_flag_in_byte(self.sol_emeralds_offset, ctx, 1)
                        case "Yellow Sol Emerald":
                            await self.receive_set_flag_in_byte(self.sol_emeralds_offset, ctx, 2)
                        case "Green Sol Emerald":
                            await self.receive_set_flag_in_byte(self.sol_emeralds_offset, ctx, 3)
                        case "White Sol Emerald":
                            await self.receive_set_flag_in_byte(self.sol_emeralds_offset, ctx, 4)
                        case "Turquoise Sol Emerald":
                            await self.receive_set_flag_in_byte(self.sol_emeralds_offset, ctx, 5)
                        case "Purple Sol Emerald":
                            await self.receive_set_flag_in_byte(self.sol_emeralds_offset, ctx, 6)
                        case "Tails":
                            await self.receive_set_flag_in_byte(self.sidekick_showing_offset, ctx, 0)
                        case "Cream":
                            await self.receive_set_flag_in_byte(self.sidekick_showing_offset, ctx, 1)
                        case "Kidnapping Tails":
                            await self.receive_unset_flag_in_byte(self.sidekick_showing_offset, ctx, 0)
                        case "Kidnapping Cream":
                            await self.receive_unset_flag_in_byte(self.sidekick_showing_offset, ctx, 1)
                        case "Extra Life (Sonic)":
                            if index >= received_in_sav:
                                await self.receive_increase_byte(self.extra_lives_sonic_offset, ctx)
                        case "Extra Life (Blaze)":
                            if index >= received_in_sav:
                                await self.receive_increase_byte(self.extra_lives_blaze_offset, ctx)
                        case "Halving Extra Lives (Sonic)":
                            if index >= received_in_sav:
                                await self.receive_halve_byte(self.extra_lives_sonic_offset, ctx)
                        case "Halving Extra Lives (Blaze)":
                            if index >= received_in_sav:
                                await self.receive_halve_byte(self.extra_lives_blaze_offset, ctx)
                        case _:
                            raise Exception("Bad item name received: " + name)
                    if index >= received_in_sav:
                        await self.receive_set_half_word(self.received_offset, ctx, index+1)
                    self.received_items_count = index+1
                    await asyncio.sleep(0.005)

            # Check for location checks
            locations_to_send = set()

            for zone in range(7):
                for act in range(2):
                    if level_scores_sonic[zone][act] != 0:
                        locations_to_send.add(location_lookup_by_name[f"Zone {zone+1} Act {act+1} (Sonic)"])
                    if level_scores_blaze[zone][act] != 0:
                        locations_to_send.add(location_lookup_by_name[f"Zone {zone+1} Act {act+1} (Blaze)"])
                    if ctx.slot_data["include_s_rank_checks"] in ["only_acts", "all"]:
                        if level_scores_sonic[zone][act] >= 100000:
                            locations_to_send.add(
                                location_lookup_by_name[f"Zone {zone+1} Act {act+1} S Rank (Sonic)"])
                        if level_scores_blaze[zone][act] >= 100000:
                            locations_to_send.add(
                                location_lookup_by_name[f"Zone {zone+1} Act {act+1} S Rank (Blaze)"])
                if level_scores_sonic[zone][2] != 0:
                    locations_to_send.add(location_lookup_by_name[f"Zone {zone+1} Boss (Sonic)"])
                if level_scores_blaze[zone][2] != 0:
                    locations_to_send.add(location_lookup_by_name[f"Zone {zone+1} Boss (Blaze)"])
                if ctx.slot_data["include_s_rank_checks"] in ["only_bosses", "all"]:
                    if level_scores_sonic[zone][2] >= 50000:
                        locations_to_send.add(location_lookup_by_name[f"Zone {zone+1} Boss S Rank (Sonic)"])
                    if level_scores_blaze[zone][2] >= 50000:
                        locations_to_send.add(location_lookup_by_name[f"Zone {zone+1} Boss S Rank (Blaze)"])

            if boss_flags_checks & 1:
                locations_to_send.add(location_lookup_by_name["F-Zone (Sonic)"])
            if boss_flags_checks & 2:
                locations_to_send.add(location_lookup_by_name["F-Zone (Blaze)"])
            if boss_flags_checks & 4:
                locations_to_send.add(location_lookup_by_name["Extra Zone"])

            for zone in range(7):
                if special_stages_checks & (1 << zone):
                    locations_to_send.add(location_lookup_by_name[f"Special Stage Zone {zone+1}"])

            # Send locations if there are any to send.
            if locations_to_send != self.local_checked_locations:
                self.local_checked_locations = locations_to_send
                if locations_to_send is not None:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locations_to_send)}])

            # Check for completing the goal and send it to the server
            if not self.goal_complete:
                goaled: bool
                match ctx.slot_data["goal"]:
                    case "bosses_once":
                        goaled = False
                        if ((level_scores_sonic[0][2] or level_scores_blaze[1][2]) and
                            (level_scores_sonic[1][2] or level_scores_blaze[3][2]) and
                            (level_scores_sonic[2][2] or level_scores_blaze[2][2]) and
                            (level_scores_sonic[3][2] or level_scores_blaze[0][2]) and
                            (level_scores_sonic[4][2] or level_scores_blaze[5][2]) and
                            (level_scores_sonic[5][2] or level_scores_blaze[4][2]) and
                            (level_scores_sonic[6][2] or level_scores_blaze[6][2])):
                           if ctx.slot_data["screw_f_zone"] or boss_flags_checks & 1 or boss_flags_checks & 2:
                               goaled = True
                    case "bosses_both":
                        goaled = True
                        for zone in range(7):
                            if not (level_scores_sonic[zone][2] and level_scores_blaze[zone][2]):
                                goaled = False
                                break
                        if not (ctx.slot_data["screw_f_zone"] or (boss_flags_checks & 1 and boss_flags_checks & 2)):
                            goaled = False
                    case "extra_zone":
                        goaled = bool(boss_flags_checks & 4)
                    case "100_percent":
                        goaled = True
                        for zone in range(7):
                            if not (level_scores_sonic[zone][2] and level_scores_blaze[zone][2]):
                                goaled = False
                                break
                        if not (ctx.slot_data["screw_f_zone"] or (boss_flags_checks & 1 and boss_flags_checks & 2 and
                                                                  boss_flags_checks & 4)):
                            goaled = False
                    case _:
                        raise Exception("Bad goal in slot data: " + ctx.slot_data["goal"])

                if goaled:
                    self.goal_complete = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect.
            pass
        except bizhawk.ConnectorError:
            pass
