# Do not change anything about these imports unless you know what you do
if __name__ == '__main__':
    from data.api import PluginProtocol
else:
    from .data.api import PluginProtocol


class Plugin(PluginProtocol):
    name = "Pokemon BW Dexsanitysanity"
    domain = "dexsanitysanity"
    version = "1.0.0"
    author = "BlastSlimey"


if __name__ == '__main__':
    from data.build import build

    build(Plugin.name, Plugin.version, Plugin.author)
