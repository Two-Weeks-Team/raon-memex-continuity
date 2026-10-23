"""Synthetic task: small in-memory tenant cache with a key collision bug."""

_values = {}


def put(tenant_id: str, key: str, value: str) -> None:
    _values[tenant_id + key] = value


def get(tenant_id: str, key: str) -> str | None:
    return _values.get(tenant_id + key)


def clear() -> None:
    _values.clear()
