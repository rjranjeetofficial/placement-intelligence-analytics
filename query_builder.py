from typing import List, Tuple, Dict, Any


def build_parameterized_filter(
    tiers: List[str],
    branches: List[str],
    cgpa_range: Tuple[float, float],
    min_dsa: int,
    placed_only: bool = True
) -> Tuple[str, Dict[str, Any]]:
    """
    Constructs a sanitized SQL WHERE clause and corresponding
    named-parameter dictionary.
    """

    conditions = []
    params: Dict[str, Any] = {}

    # Filter by college tier
    if tiers:
        tier_keys = [f"tier_{i}" for i in range(len(tiers))]
        placeholders = ", ".join([f":{k}" for k in tier_keys])

        conditions.append(
            f"College_Tier IN ({placeholders})"
        )

        for k, val in zip(tier_keys, tiers):
            params[k] = val

    # Filter by branch
    if branches:
        branch_keys = [f"branch_{i}" for i in range(len(branches))]
        placeholders = ", ".join([f":{k}" for k in branch_keys])

        conditions.append(
            f"Branch IN ({placeholders})"
        )

        for k, val in zip(branch_keys, branches):
            params[k] = val

    # Filter by CGPA range
    conditions.append(
        "CGPA BETWEEN :cgpa_min AND :cgpa_max"
    )

    params["cgpa_min"] = float(cgpa_range[0])
    params["cgpa_max"] = float(cgpa_range[1])

    # Filter by minimum DSA problems solved
    conditions.append(
        "DSA_Problems_Solved >= :min_dsa"
    )

    params["min_dsa"] = int(min_dsa)

    # Filter only placed students
    if placed_only:
        conditions.append(
            "Placement_Status = :status"
        )

        params["status"] = "Placed"

    # Construct WHERE clause
    where_clause = (
        f"WHERE {' AND '.join(conditions)}"
        if conditions
        else ""
    )

    return where_clause, params