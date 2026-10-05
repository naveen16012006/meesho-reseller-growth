"""Mask reseller names before any narrative is treated as externally shareable."""


def alias_for(reseller_id: str) -> str:
    return f"ALIAS-{reseller_id[3:]}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    return not any(name and name in text for name in reseller_names)


if __name__ == "__main__":
    safe = "The West region's ALIAS-19 exceeded the spend threshold."
    unsafe = "Mumbai Reseller 1 exceeded the spend threshold."
    assert alias_for("RS019") == "ALIAS-19"
    assert assert_no_raw_names_leak(safe, ["Mumbai Reseller 1"])
    assert not assert_no_raw_names_leak(unsafe, ["Mumbai Reseller 1"])
