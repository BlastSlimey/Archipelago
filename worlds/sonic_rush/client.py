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

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {}
        self.local_found_key_items = {}
        self.seed_verify = False

    async def receive_set_flag(self, address: int, ctx: "BizHawkClientContext", current_bits: int, to_be_set: int):
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, (current_bits | (1 << to_be_set)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain
            )],
        )

    async def receive_unset_flag(self, address: int, ctx: "BizHawkClientContext", current_bits: int, to_be_unset: int):
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, (current_bits & ~(1 << to_be_unset)).to_bytes(length=1, byteorder="little"), self.ram_mem_domain
            )],
        )

    async def receive_increase_byte(self, address: int, ctx: "BizHawkClientContext", current_byte: int):
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(
                address, min(current_byte + 1, 255).to_bytes(length=1, byteorder="little"), self.ram_mem_domain
            )],
        )

    async def receive_halve_byte(self, address: int, ctx: "BizHawkClientContext", current_byte: int):
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

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        self.seed_verify = False
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
        try:
            if ctx.seed_name is None:
                return
            await asyncio.sleep(0.1)

            savedata_initialized_offset = 0x2c476f

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (savedata_initialized_offset, 1, self.ram_mem_domain),
                ]
            )

            # Return if save data not yet initialized, else it's 0xff, and that's bad
            if int.from_bytes(read_state[0]) != 0:
                return

            last_received_offset = 0x2c475e
            zone_unlocks_sonic_offset = 0x2c4760
            zone_unlocks_blaze_offset = 0x2c4761
            progressive_level_unlocks_sonic_offset = 0x2c4762
            progressive_level_unlocks_blaze_offset = 0x2c4763
            special_stages_offset = 0x2c4764
            chaos_emeralds_offset = 0x2C468F
            sol_emeralds_offset = 0x2c4765
            boss_flags_offset = 0x2c4766
            sidekick_showing_offset = 0x2c4767
            level_scores_sonic_offset = 0x2c4690
            level_scores_blaze_offset = 0x2c46e8
            extra_lives_sonic_offset = 0x2C468E
            extra_lives_blaze_offset = 0x2C46E6

            read_state = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (last_received_offset, 2, self.ram_mem_domain),
                    (zone_unlocks_sonic_offset, 1, self.ram_mem_domain),
                    (zone_unlocks_blaze_offset, 1, self.ram_mem_domain),
                    (progressive_level_unlocks_sonic_offset, 1, self.ram_mem_domain),
                    (progressive_level_unlocks_blaze_offset, 1, self.ram_mem_domain),
                    (special_stages_offset, 1, self.ram_mem_domain),
                    (chaos_emeralds_offset, 1, self.ram_mem_domain),
                    (sol_emeralds_offset, 1, self.ram_mem_domain),
                    (boss_flags_offset, 1, self.ram_mem_domain),
                    (sidekick_showing_offset, 1, self.ram_mem_domain),
                    (extra_lives_sonic_offset, 1, self.ram_mem_domain),
                    (extra_lives_blaze_offset, 1, self.ram_mem_domain),
                    (level_scores_sonic_offset, 84, self.ram_mem_domain),
                    (level_scores_blaze_offset, 84, self.ram_mem_domain),
                ]
            )

            received_in_sav = int.from_bytes(read_state[0], "little")
            zone_unlocks_sonic_in_sav = int.from_bytes(read_state[1])
            zone_unlocks_blaze_in_sav = int.from_bytes(read_state[2])
            progressive_level_unlocks_sonic_in_sav = int.from_bytes(read_state[3])
            progressive_level_unlocks_blaze_in_sav = int.from_bytes(read_state[4])
            special_stages_checks = int.from_bytes(read_state[5])
            chaos_emeralds_in_sav = int.from_bytes(read_state[6])
            sol_emeralds_in_sav = int.from_bytes(read_state[7])
            boss_flags_checks = int.from_bytes(read_state[8])
            sidekick_showing_in_sav = int.from_bytes(read_state[9])
            extra_lives_sonic_in_sav = int.from_bytes(read_state[10])
            extra_lives_blaze_in_sav = int.from_bytes(read_state[11])
            level_scores_sonic: Dict[int, Dict[int, int]] = {}
            level_scores_blaze: Dict[int, Dict[int, int]] = {}
            for zone in range(7):
                level_scores_sonic[zone] = {}
                level_scores_blaze[zone] = {}
                for act in range(3):
                    offset = zone*12+act*4
                    level_scores_sonic[zone][act] = int.from_bytes(read_state[12][offset:(offset+4)], "little")
                    level_scores_blaze[zone][act] = int.from_bytes(read_state[13][offset:(offset+4)], "little")

            if len(ctx.items_received) > received_in_sav:
                network_item = ctx.items_received[received_in_sav]
                name = item_lookup_by_id[network_item.item]
                match name:
                    case "Unlock Zone 1 (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 0)
                    case "Unlock Zone 2 (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 1)
                    case "Unlock Zone 3 (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 2)
                    case "Unlock Zone 4 (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 3)
                    case "Unlock Zone 5 (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 4)
                    case "Unlock Zone 6 (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 5)
                    case "Unlock Zone 7 (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 6)
                    case "Unlock F-Zone (Sonic)":
                        await self.receive_set_flag(zone_unlocks_sonic_offset, ctx, zone_unlocks_sonic_in_sav, 7)
                    case "Unlock Zone 1 (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 0)
                    case "Unlock Zone 2 (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 1)
                    case "Unlock Zone 3 (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 2)
                    case "Unlock Zone 4 (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 3)
                    case "Unlock Zone 5 (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 4)
                    case "Unlock Zone 6 (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 5)
                    case "Unlock Zone 7 (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 6)
                    case "Unlock F-Zone (Blaze)":
                        await self.receive_set_flag(zone_unlocks_blaze_offset, ctx, zone_unlocks_blaze_in_sav, 7)
                    case "Progressive Level Select (Sonic)":
                        await self.receive_increase_byte(progressive_level_unlocks_sonic_offset, ctx,
                                                         progressive_level_unlocks_sonic_in_sav)
                    case "Progressive Level Select (Blaze)":
                        await self.receive_increase_byte(progressive_level_unlocks_blaze_offset, ctx,
                                                         progressive_level_unlocks_blaze_in_sav)
                    case "Red Chaos Emerald":
                        await self.receive_set_flag(chaos_emeralds_offset, ctx, chaos_emeralds_in_sav, 0)
                    case "Blue Chaos Emerald":
                        await self.receive_set_flag(chaos_emeralds_offset, ctx, chaos_emeralds_in_sav, 1)
                    case "Yellow Chaos Emerald":
                        await self.receive_set_flag(chaos_emeralds_offset, ctx, chaos_emeralds_in_sav, 2)
                    case "Green Chaos Emerald":
                        await self.receive_set_flag(chaos_emeralds_offset, ctx, chaos_emeralds_in_sav, 3)
                    case "White Chaos Emerald":
                        await self.receive_set_flag(chaos_emeralds_offset, ctx, chaos_emeralds_in_sav, 4)
                    case "Turquoise Chaos Emerald":
                        await self.receive_set_flag(chaos_emeralds_offset, ctx, chaos_emeralds_in_sav, 5)
                    case "Purple Chaos Emerald":
                        await self.receive_set_flag(chaos_emeralds_offset, ctx, chaos_emeralds_in_sav, 6)
                    case "Red Sol Emerald":
                        await self.receive_set_flag(sol_emeralds_offset, ctx, sol_emeralds_in_sav, 0)
                    case "Blue Sol Emerald":
                        await self.receive_set_flag(sol_emeralds_offset, ctx, sol_emeralds_in_sav, 1)
                    case "Yellow Sol Emerald":
                        await self.receive_set_flag(sol_emeralds_offset, ctx, sol_emeralds_in_sav, 2)
                    case "Green Sol Emerald":
                        await self.receive_set_flag(sol_emeralds_offset, ctx, sol_emeralds_in_sav, 3)
                    case "White Sol Emerald":
                        await self.receive_set_flag(sol_emeralds_offset, ctx, sol_emeralds_in_sav, 4)
                    case "Turquoise Sol Emerald":
                        await self.receive_set_flag(sol_emeralds_offset, ctx, sol_emeralds_in_sav, 5)
                    case "Purple Sol Emerald":
                        await self.receive_set_flag(sol_emeralds_offset, ctx, sol_emeralds_in_sav, 6)
                    case "Tails":
                        await self.receive_set_flag(sidekick_showing_offset, ctx, sidekick_showing_in_sav, 0)
                    case "Cream":
                        await self.receive_set_flag(sidekick_showing_offset, ctx, sidekick_showing_in_sav, 1)
                    case "Kidnapping Tails":
                        await self.receive_unset_flag(sidekick_showing_offset, ctx, sidekick_showing_in_sav, 0)
                    case "Kidnapping Cream":
                        await self.receive_unset_flag(sidekick_showing_offset, ctx, sidekick_showing_in_sav, 1)
                    case "Extra Life (Sonic)":
                        await self.receive_increase_byte(extra_lives_sonic_offset, ctx, extra_lives_sonic_in_sav)
                    case "Extra Life (Blaze)":
                        await self.receive_increase_byte(extra_lives_blaze_offset, ctx, extra_lives_blaze_in_sav)
                    case "Halving Extra Lives (Sonic)":
                        await self.receive_halve_byte(extra_lives_sonic_offset, ctx, extra_lives_sonic_in_sav)
                    case "Halving Extra Lives (Blaze)":
                        await self.receive_halve_byte(extra_lives_blaze_offset, ctx, extra_lives_blaze_in_sav)
                await self.receive_set_half_word(last_received_offset, ctx, received_in_sav+1)
                await asyncio.sleep(0.1)

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
                    locations_to_send.add(location_lookup_by_name[f"Zone {zone+1} Act Boss (Blaze)"])
                if ctx.slot_data["include_s_rank_checks"] in ["only_acts", "all"]:
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
