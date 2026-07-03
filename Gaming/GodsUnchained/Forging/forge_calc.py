from typing import Optional
from config import QUALITIES, FORGE_RATIOS, MARKETPLACE_FEES, MARKETPLACE_FEE, DEFAULT_GODS_COSTS


def next_quality(quality: str) -> Optional[str]:
    try:
        idx = QUALITIES.index(quality)
    except ValueError:
        return None
    return QUALITIES[idx + 1] if idx < len(QUALITIES) - 1 else None


def forge_ratio(from_quality: str) -> int:
    return FORGE_RATIOS.get(from_quality, 2)


def marketplace_fee(output_quality: str) -> float:
    return MARKETPLACE_FEES.get(output_quality, MARKETPLACE_FEE)


def gods_cost_for(rarity: str, custom_costs: Optional[dict] = None) -> float:
    """GODS per single forge — flat by rarity, same for any quality transition."""
    costs = custom_costs or DEFAULT_GODS_COSTS
    return costs.get(rarity.lower(), DEFAULT_GODS_COSTS.get("common", 0.1))


def max_forgeable(count: int, from_quality: str) -> int:
    return count // forge_ratio(from_quality)


def calc_profit(
    input_floor_eth: float,      # floor price of 1 input card (0 for in-game plain cards)
    output_floor_eth: float,
    from_quality: str,
    to_quality: str,
    gods_amount: float,
    gods_eth: float,
) -> dict:
    ratio      = forge_ratio(from_quality)
    fee        = marketplace_fee(to_quality)
    revenue    = output_floor_eth * (1.0 - fee)
    input_cost = ratio * input_floor_eth          # opportunity cost of burning input cards
    gods_spend = gods_amount * gods_eth
    total_cost = input_cost + gods_spend
    profit     = revenue - total_cost
    roi        = (profit / total_cost * 100.0) if total_cost > 0 else 0.0
    return {
        "revenue":    revenue,
        "input_cost": input_cost,
        "gods_spend": gods_spend,
        "total_cost": total_cost,
        "fee_pct":    fee * 100,
        "profit":     profit,
        "roi":        roi,
    }
