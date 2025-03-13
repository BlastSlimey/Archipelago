from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class SonicRushClient(BizHawkClient):
    game = "Sonic Rush"
    system = "NDS"
    patch_suffix = ".aprush"  # Unsure about suffix: .apsonicrush would definitely be unique, but .aprush looks better
    
