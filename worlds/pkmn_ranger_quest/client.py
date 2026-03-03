import logging
from typing import TYPE_CHECKING, Collection

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .data.addresses import ADDR, OFF

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def register_client():
    """This is just a placeholder function to remind new (and old) world devs to import the client file"""
    pass


class RangerQuestClient(BizHawkClient):
    game = "Pokemon Ranger (Quest)"
    system = "NDS"

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("Client")
        self.version = 0
        self.has_touched = False
        self.items_received = 0
        self.open_captures: dict[int, list[int]] = {}  # {internal pokemon id: [item indices, ...]}
        self.open_assists: tuple[list[int], list[int]] = [], []  # ([item index, ...], [assist type id, ...])
        self.debug_counter = 0
        self.checked_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        header = (await bizhawk.read(
            ctx.bizhawk_ctx, (
                (ADDR.header, 0xc0, "Main RAM"),
            )
        ))[0]
        if header[:11] != b'POKE RANGER':
            return False
        if header[15:16] == b'P':
            self.version = 0
        elif header[15:16] == b'E':
            self.version = 1
        elif header[15:16] == b'J':
            if header[0x1e:0x1f] == b'0':
                self.version = 2
            elif header[0x1e:0x1f] == b'1':
                self.version = 3
            else:
                return False
        else:
            return False
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.1
        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from . import RangerQuestWorld
        from .data import items
        try:
            if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot_data is None:
                return

            self.debug_counter = (self.debug_counter + 1) % 1000

            if not self.checked_locations and ctx.locations_checked:
                self.checked_locations.update(ctx.locations_checked)

            for item_index in range(self.items_received, len(ctx.items_received)):
                self.items_received += 1
                network_item = ctx.items_received[item_index]
                name = ctx.item_names.lookup_in_game(network_item.item)
                if name in items.capture:
                    for intern_id in items.capture[name].internal_ids:
                        if intern_id not in self.open_captures:
                            self.open_captures[intern_id] = []
                        self.open_captures[intern_id].append(item_index)
                elif name in items.assist:
                    self.open_assists[0].append(item_index)
                    self.open_assists[1].append(items.assist[name].type_id)
                else:
                    self.logger.warning(f"Quest type of \"{name}\" unknown, most likely due to an incompatible "
                                        f"version. If this quest is already completed, then no further action is "
                                        f"needed. Otherwise, you need to downgrade to an older version.")

            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (ADDR.touched[self.version]-0x20, 4, "Main RAM"),
                    (ADDR.touched[self.version], 1, "Main RAM"),
                    (ADDR.capture_ptr[self.version], 4, "Main RAM"),
                )
            )
            if not is_ptr(read[0]):
                return  # not ingame
            checked = []
            if not self.has_touched and read[1] != b'\x00':
                self.has_touched = True
                await self.check_locations({RangerQuestWorld.location_name_to_id["Inspect a pokémon"]}, ctx)
            if not is_ptr(read[2]):
                return  # not in-capture, so rest can be skipped
            capture_ptr = to_ptr(read[2])
            read = await bizhawk.read(
                ctx.bizhawk_ctx, tuple(
                    (capture_ptr + OFF.capture_pokemon_ptr + i*0x10, 4, "Main RAM") for i in range(8)
                ) + (
                    (capture_ptr + OFF.assist, 1, "Main RAM"),
                )
            )
            if read[8][0] != 0 and read[8][0] in self.open_assists[1]:
                for _ in range(self.open_assists[1].count(read[8][0])
                               if not ctx.slot_data["force_one_check_at_a_time"] else 1):
                    found = self.open_assists[1].index(read[8][0])
                    checked.append(f"Complete quest #{self.open_assists[0][found]+1}")
                    self.open_assists[0].pop(found)
                    self.open_assists[1].pop(found)
            for slot in range(8):
                if not is_ptr(read[slot]):
                    continue  # no pokémon in this slot
                pokemon_ptr = to_ptr(read[slot])
                read2 = await bizhawk.read(
                    ctx.bizhawk_ctx, (
                        (pokemon_ptr + OFF.capture_pokemon_id, 1, "Main RAM"),
                        (pokemon_ptr + OFF.capture_pokemon_success, 1, "Main RAM"),
                    )
                )
                if read2[1][0] and read2[0][0] in self.open_captures and self.open_captures[read2[0][0]]:
                    for _ in range(len(self.open_captures[read2[0][0]])
                                   if not ctx.slot_data["force_one_check_at_a_time"] else 1):
                        item_index = self.open_captures[read2[0][0]].pop(0)
                        checked.append(f"Complete quest #{item_index+1}")

            if checked:
                await self.check_locations(set(RangerQuestWorld.location_name_to_id[check] for check in checked), ctx)

            if len(self.checked_locations) >= ctx.slot_data["goal_amount"]:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            pass
        except bizhawk.ConnectorError:
            pass

    def print(self, obj, delay=20):
        if self.debug_counter % delay == 0:
            print(obj)

    async def check_locations(self, locations: set[int], ctx: "BizHawkClientContext"):
        self.checked_locations.update(locations)
        await ctx.check_locations(locations)


def is_ptr(value: bytes) -> bool:
    return 0x02000000 <= int.from_bytes(value, "little") <= 0x023fffff


def to_ptr(value: bytes) -> int:
    return int.from_bytes(value[:3], "little")
