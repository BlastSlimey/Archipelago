# Based (read: copied almost wholesale and edited) off the KHDays and Manual Clients.

import asyncio
from typing import Dict, List

import Utils
from CommonClient import CommonContext, server_loop, gui_enabled, get_base_parser

from .data.locations import all_locations


class Shapez2Context(CommonContext):
    items_handling = 0b000  # None
    game = "shapez 2"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = 'Kingdom Hearts Days'
        self.slot_data = None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.slot_data = args["slot_data"]

    def run_gui(self):
        from kvui import GameManager
        from kivy.uix.tabbedpanel import TabbedPanelItem
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.gridlayout import GridLayout
        from kivy.uix.layout import Layout

        class TrackerLayout(BoxLayout):
            pass

        class CommanderButton(Button):
            pass

        class CommanderGroup(GridLayout):
            pass

        class Shapez2Manager(GameManager):
            base_title = "Archipelago shapez 2 Client"
            ctx: Shapez2Context
            commander_buttons: Dict[int, List[CommanderButton]]
            location_buttons: List[CommanderButton]

            def build(self) -> Layout:
                container = super().build()
                panel = TabbedPanelItem(text="Locations")
                panel.content = self.build_locations_panel()
                self.tabs.add_widget(panel)
                return container

            def build_locations_panel(self) -> TrackerLayout:
                try:
                    adjust = self.ctx.slot_data["options"]["location_adjustments"]
                    milestones: int = adjust["Milestones"]
                    task_lines: int = adjust["Task lines"]
                    operator_levels: int = adjust["Operator level checks"]
                    tracker = TrackerLayout(orientation="horizontal")
                    commander_group = CommanderGroup(cols=5)
                    for i in range(milestones):
                        commander_button = CommanderButton(text=f"Milestone {i+1}")
                        commander_button.bind(on_press=lambda instance: self.send_milestone(i+1))
                        commander_group.add_widget(commander_button)
                    for i in range(task_lines):
                        for j in range(1, 6):
                            commander_button = CommanderButton(text=f"Task #{i+1}-{j}")
                            commander_button.bind(on_press=lambda instance: self.send_task(i+1, j))
                            commander_group.add_widget(commander_button)
                    for i in range(operator_levels):
                        commander_button = CommanderButton(text=f"Operator level {i+1}")
                        commander_button.bind(on_press=lambda instance: self.send_operator_level(i+1))
                        commander_group.add_widget(commander_button)
                    tracker.add_widget(commander_group)
                    return tracker
                except Exception as e:
                    print(e)

            def send_milestone(self, num: int):
                self.ctx.check_locations(tuple(
                    all_locations[f"Milestone {num} reward #{i}"].location_id for i in range(1, 13)
                ))

            def send_task(self, line: int, num: int):
                self.ctx.check_locations((all_locations[f"Task #{line}-{num}"].location_id, ))

            def send_operator_level(self, level: int):
                self.ctx.check_locations((all_locations[f"Operator level {level}"].location_id, ))

        self.ui = Shapez2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def main():
    # Text Mode to use !hint and such with games that have no text entry
    Utils.init_logging("shapez2Client", exception_logger="Client")

    async def _main():
        ctx = Shapez2Context(None, None)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="shapez 2 manual-like client, intended for playing without the mod.")
    args = parser.parse_args()
    main()
