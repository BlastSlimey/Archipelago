from .items import capture, assist

items: dict[str, str] = {
    name: "A quest for capturing a specific pokémon, that grants an AP item when completed." for name in capture
} | {
    name: ("A quest for using a specific Poké Assist type while capturing another pokémon, "
           "that grants an AP item when completed.") for name in assist
}
# | {
#     name: ("A quest for using a specific type of field moves on any level, "
#            "that grants an AP item when completed.") for name in field_any
# } | {
#     name: ("A quest for using a specific type of field moves on a specific level, "
#            "that grants an AP item when completed.") for name in field_level
# }
