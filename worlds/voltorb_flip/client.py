import asyncio
import logging
from typing import TYPE_CHECKING

import Utils
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def register_client():
    """This is just a placeholder function to remind new (and old) world devs to import the client file"""
    pass


class VoltorbFlipClient(BizHawkClient):
    game = "Voltorb Flip"
    system = "NDS"

    header_address = 0x3FFE00
    global_pointer_address = 0xBA8

    total_coins_offset = 0x94  # 16 bit
    map_id_offset = 0x1244  # 16 bit
    points_gained_offset = 0x69D80  # 16 bit
    points_possible_offset = 0x69D82  # 16 bit
    level_offset = 0x69D8A  # 8 bit
    board_counter_offset = 0x69D8B  # 8 bit

    french_offset = 0x58
    italy_offset = -0xb8
    spain_offset = -0x178
    germany_offset = 0x504

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("Client")
        self.language_offset = 0
        self.total_gained = 0
        self.vf_data_address = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        header = await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.header_address, 0xc0, "Main RAM"),
            )
        )
        if header[0][:10] not in (b'POKEMON SS', b'POKEMON HG'):
            return False
        if header[0][15:16] == b'D':
            self.language_offset = self.germany_offset
        elif header[0][15:16] == b'F':
            self.language_offset = self.french_offset
        elif header[0][15:16] == b'I':
            self.language_offset = self.italy_offset
        elif header[0][15:16] == b'S':
            self.language_offset = self.spain_offset
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.2
        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]
        elif cmd == "Connected":
            Utils.async_start(ctx.send_msgs([
                {
                    "cmd": "Set",
                    "key": f"voltorb_flip_coins_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": True,
                    "operations": [{"operation": "default", "value": None}]  # value is ignored
                }, {
                    "cmd": "SetNotify",
                    "keys": [f"voltorb_flip_coins_{ctx.team}_{ctx.slot}"]
                }
            ]))
        elif cmd == "SetReply":
            if args.get("key", "") == f"voltorb_flip_coins_{ctx.team}_{ctx.slot}":
                self.total_gained = args["value"]  # Intentionally crash if no value argument to keep track of bugs

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            if (
                not ctx.server or
                not ctx.server.socket.open or
                ctx.server.socket.closed or
                ctx.slot_data is None
            ):
                return

            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.global_pointer_address, 3, "Main RAM"),
                )
            )
            global_pointer = int.from_bytes(read[0], "little")
            if global_pointer == 0:
                return  # Just to make sure we don't hit a very bad moment
            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (global_pointer + 0x20, 4, "Main RAM"),
                )
            )
            if read[0][3] != 0x02:
                return  # Not yet initialized
            version_pointer = int.from_bytes(read[0][:3], "little")
            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (version_pointer + self.map_id_offset, 2, "Main RAM"),
                )
            )
            if read[0] not in (b'\x18\x02', b'\x19\x02'):
                return  # Wrong map, might have other data in upcoming addresses
            vf_data_address = version_pointer + 0x69D80 + self.language_offset
            if self.vf_data_address != vf_data_address:
                self.vf_data_address = vf_data_address
                self.logger.info(f"Global pointer {hex(global_pointer)}, "
                                 f"version pointer {hex(version_pointer)}, "
                                 f"vf data address {hex(vf_data_address)}")

            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (vf_data_address, 0x10, "Main RAM"),
                )
            )
            if read[0][2:4] == b'\0\0':
                return  # not ingame
            if read[0][0:2] != read[0][2:4]:
                return  # level not finished yet

            coins_won = int.from_bytes(read[0][0:2], "little")
            new_total = self.total_gained + coins_won
            coin_steps = ctx.slot_data["coin_locations_adjustments"]["Steps"]
            new_coin_checks = [i for i in range(0, new_total+1, coin_steps)]
            await ctx.check_locations([8 - read[0][0xA]] + new_coin_checks)
            self.total_gained = new_total
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"voltorb_flip_coins_{ctx.team}_{ctx.slot}",
                "default": 0,
                "operations": [{"operation": "add", "value": coins_won}]
            }])

            match ctx.slot_data["goal"]:
                case "levels":
                    if 8 - read[0][0xA] >= ctx.slot_data["level_locations_adjustments"]["Maximum"]:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                case "coins":
                    if new_total >= ctx.slot_data["coin_locations_adjustments"]["Maximum"]:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            while read[0][0:2] == read[0][2:4]:
                await asyncio.sleep(ctx.watcher_timeout)
                read = await bizhawk.read(
                    ctx.bizhawk_ctx, (
                        (vf_data_address, 0x10, "Main RAM"),
                    )
                )

        except bizhawk.RequestFailedError:
            pass
        except bizhawk.ConnectorError:
            pass
