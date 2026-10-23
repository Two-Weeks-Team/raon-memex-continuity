"""Synthetic task: retry delay with a missing Retry-After branch."""


def retry_delay(status: int, retry_after: str | None, attempt: int) -> float:
    if status != 429:
        return 0.0
    return float(min(2 ** max(attempt, 0), 30))
