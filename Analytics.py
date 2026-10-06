import pandas as pd
import numpy as np
from database import run_query


def compute_future_projections():
    """
    Computes marginal package returns across DSA tiers and future hiring
    inflation curves for technical profiles.
    """

    placed_df = run_query("""
        SELECT DSA_Problems_Solved, Package_LPA, College_Tier, GitHub_Contributions
        FROM students
        WHERE Placement_Status = 'Placed';
    """)

    if placed_df.empty:
        return {"dsa_curve": [], "tier_parity": []}

    placed_df = placed_df.copy()
    placed_df["DSA_Problems_Solved"] = pd.to_numeric(
        placed_df["DSA_Problems_Solved"], errors="coerce"
    )
    placed_df["Package_LPA"] = pd.to_numeric(
        placed_df["Package_LPA"], errors="coerce"
    )
    placed_df = placed_df.dropna(subset=["DSA_Problems_Solved", "Package_LPA"])

    bins = pd.cut(placed_df["DSA_Problems_Solved"], bins=range(0, 1201, 100), include_lowest=True)
    dsa_agg = placed_df.groupby(bins, observed=False)["Package_LPA"].mean().reset_index()
    dsa_agg = dsa_agg.dropna()
    dsa_agg["bin_mid"] = [int(b.mid) for b in dsa_agg["DSA_Problems_Solved"]]
    dsa_agg["projected_lpa"] = dsa_agg["Package_LPA"] * (1 + (dsa_agg["bin_mid"] / 1000) * 0.35)

    placed_df["Skill_Band"] = pd.qcut(
        placed_df["DSA_Problems_Solved"], q=3, duplicates="drop",
        labels=["Foundational", "Intermediate", "Advanced"],
    )
    tier_parity = (
        placed_df.groupby(["Skill_Band", "College_Tier"], observed=False)["Package_LPA"]
        .mean()
        .reset_index()
    )

    return {
        "dsa_curve": dsa_agg.to_dict(orient="records"),
        "tier_parity": tier_parity.to_dict(orient="records"),
    }