"""Turn measured tokens into money, using the fetched price sheet."""
import json
from pathlib import Path

SHEET = json.loads((Path(__file__).resolve().parents[1] / "data" / "prices.json").read_text())


# snippet:cost
def cost(row: dict, tokens_in: int, tokens_out: int, cached_in: int = 0, batch: bool = False) -> float:
    """USD for one task. `cached_in` is the part of tokens_in read from the provider's prompt cache."""
    price_in, price_out = (row["batch_input"], row["batch_output"]) if batch else (row["input"], row["output"])
    if price_in is None or price_out is None:
        raise ValueError(f"{row['model']} has no batch price on its sheet")
    fresh = tokens_in - cached_in
    return (fresh * price_in + cached_in * (row["cached"] or price_in) + tokens_out * price_out) / 1_000_000
# end:cost
