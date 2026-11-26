# data/

This folder is not tracked by git (see `.gitignore`); only this README and the empty
`raw/` and `processed/` folders are.

- `raw/`: original files, downloaded unchanged.
  - Wyscout soccer match event dataset, Pappalardo et al. (2019), CC BY 4.0,
    <https://figshare.com/collections/_/4415000>.
  - PlayeRank scores (`playerank.json`), CC BY 4.0,
    <https://figshare.com/articles/PlayeRanks/9361148>.
- `processed/`: tables built by scripts in `src/`.
  - `player_match.parquet`: one row per (`matchId`, `playerId`), features and target.
  - `playerank_side_info.parquet`: quarantine table for `minutesPlayed` and `goalScored`
    (published with the target). Never joined to the feature table by default;
    see `report/project_specification.md`, Section 6.

The download script is added in task T1 (module M1).
