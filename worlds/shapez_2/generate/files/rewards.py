from typing import Iterator

from ...data.items import all_items


def get_rewards(item: str) -> Iterator[dict[str, str | int]]:
    data = all_items[item]
    # Assumes that there are no mixed points items
    if data.amount_rp:
        yield {"$type": "ResearchPointsReward", "Amount": data.amount_rp}
        return
    if data.amount_bp:
        yield {"$type": "BlueprintCurrencyReward", "Amount": data.amount_bp}
        return
    if data.amount_pc:
        yield {"$type": "ChunkLimitReward", "Amount": data.amount_pc}
        return
    for reward in data.reward_ids_buildings:
        yield {"$type": "BuildingReward", "BuildingDefinitionGroupId": reward}
    for reward in data.reward_ids_islands:
        yield {"$type": "IslandGroupReward", "GroupId": reward}
    for reward in data.reward_ids_mechanics:
        yield {"$type": "MechanicReward", "MechanicId": reward}


def get_bundle(item: str) -> dict[str, str | int]:
    data = all_items[item]
    # Assumes that there are no mixed points items
    if data.amount_rp:
        return {"$type": "ResearchPointsReward", "Amount": data.amount_rp}
    if data.amount_bp:
        return {"$type": "BlueprintCurrencyReward", "Amount": data.amount_bp}
    if data.amount_pc:
        return {"$type": "ChunkLimitReward", "Amount": data.amount_pc}
    return {'$type': 'ContentBundleReward', 'ContentBundleId': data.remote_id}
