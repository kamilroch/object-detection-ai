import pandas as pd


def time_format(seconds):
    if seconds is None:
        return "-"
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"00:{minutes:02d}:{sec:02d}"

def create_summary_csv(summary):
    summary_df = pd.DataFrame([{
        "pojazdy_strazy_pozarnej": summary["fire_count"],
        "inne_pojazdy": summary["other_count"],
        "lacznie_pojazdow": summary["total_count"],
        "sredni_poziom_pewnosci": round(summary["avg_conf"], 2),
        "najwyzszy_poziom_pewnosci": round(summary["max_conf"], 2),
        "czas_pierwszego_fire_truck": summary["first_fire_time"],
        "czas_ostatniego_fire_truck": summary["last_fire_time"]
    }])

    return summary_df.to_csv(
        index=False,
        sep=";",
        encoding="utf-8-sig"
    ).encode("utf-8-sig")
