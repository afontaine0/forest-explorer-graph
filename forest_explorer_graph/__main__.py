from __future__ import annotations
import pandas as pd
import os


def main():
    df = load_data()
    start_edges = get_start_edges(df)
    print("START EDGES: ", start_edges)

    paths_with_lengths = []
    
    for start in start_edges:
        path = get_path(df, start)
        path_length = get_path_length(df, path)
        
        print(f"PATH: {path} LENGTH: {path_length}")

        paths_with_lengths.append((path, path_length))

    longest_path = max(paths_with_lengths, key=lambda x: x[1])
    print(f"LONGEST PATH: {longest_path[0]} LENGTH: {longest_path[1]}")


if __name__ == "__main__":
    main()


def load_data() -> pd.DataFrame:
    return pd.read_csv(
        os.path.join(os.path.dirname(__file__), "..", "data", "data.csv")
    )


def get_start_edges(df: pd.DataFrame) -> list[str]:
    return df[df["type_aretes"] == "depart"]["arete_id"].tolist()


def get_path(df: pd.DataFrame, start: str) -> list[str]:
    current_edge = df[df["arete_id"] == start].iloc[0]
    path = [current_edge["arete_id"]]

    if current_edge["type_aretes"] == "arrivee":
        return path
    
    next_edge = df[df["noeud_amont"] == current_edge["noeud_aval"]].iloc[0]
    
    path.extend(get_path(df, next_edge["arete_id"]))

    return path


def get_path_length(df: pd.DataFrame, path: list[str]) -> float:
    return df[df["arete_id"].isin(path)]["distance"].sum()
