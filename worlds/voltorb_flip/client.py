import logging
from typing import TYPE_CHECKING

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

    ram_read_write_domain = "Main RAM"
    header_address = 0x3FFE00
    global_pointer_address = 0xBA8
    voltorb_flip_level_offset = 0x69D8A
    french_offset = 0x58
    italy_offset = -0xb8
    spain_offset = -0x178
    germany_offset = 0x504

    def __init__(self):
        super().__init__()
        self.global_pointer = 0
        self.version_pointer = 0
        self.voltorb_flip_level_address = 0
        self.logger = logging.getLogger("Client")
        self.language_offset = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        header = await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.header_address, 0xc0, self.ram_read_write_domain),
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
        ctx.watcher_timeout = 1
        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            if (
                not ctx.server or
                not ctx.server.socket.open or
                ctx.server.socket.closed
            ):
                return
            if self.global_pointer == 0:
                read = await bizhawk.read(
                    ctx.bizhawk_ctx, (
                        (self.global_pointer_address, 3, self.ram_read_write_domain),
                    )
                )
                self.global_pointer = int.from_bytes(read[0], "little")
                if self.global_pointer == 0:
                    return  # not initialized yet? idk
                read = await bizhawk.read(
                    ctx.bizhawk_ctx, (
                        (self.global_pointer + 0x20, 3, self.ram_read_write_domain),
                    )
                )
                self.version_pointer = int.from_bytes(read[0], "little")
                self.voltorb_flip_level_address = (self.version_pointer +
                                                   self.voltorb_flip_level_offset +
                                                   self.language_offset)
                self.logger.info(f"Voltorb Flip level address: {self.voltorb_flip_level_address}")
            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.voltorb_flip_level_address, 1, self.ram_read_write_domain),
                )
            )
            if read[0][0] in range(1, 7):
                await ctx.check_locations([8-read[0][0]])
            if read[0][0] == 1:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        except bizhawk.RequestFailedError:
            pass
        except bizhawk.ConnectorError:
            pass
