# Lab 5 – Issues Found and Fixed
**Name:** Dhanush S S | **SRN:** PES1UG24AM082 | **Section:** B | **Repo:** L5_19_music_catalog

Scores before → after: Pylint **4.57 → 10.00/10**, Bandit **4 → 0 issues**, Flake8 **7 → 0 issues**.

| # | Issue | Tool (code) | Severity | Line(s) (orig.) | Description | Fix Approach |
|---|-------|-------------|----------|-----------------|-------------|--------------|
| 1 | SQL injection | Bandit B608 | Medium | 10 | `INSERT` built with `%` string formatting, so a title like `x'); DROP TABLE songs;--` is executed as SQL | Use a parameterised query with `?` placeholders and a tuple of values |
| 2 | Unsafe deserialisation | Bandit B301 / B403 | Medium / Low | 1, 29, 33 | `pickle.loads` can run arbitrary code if the playlist blob is untrusted | Replace pickle with `json.dumps` / `json.loads` (a playlist is just a list of strings) |
| 3 | Mutable default argument | Pylint W0102 | Medium (bug) | 9 | `playlist=[]` is created once and shared, so songs added without a playlist leak into later calls | Default to `None` and create a new list inside the function |
| 4 | Bare `except` | Pylint W0702 / Flake8 E722 | Medium | 39 | Catches everything, including `KeyboardInterrupt`/`SystemExit`, and hides real bugs | Catch only `sqlite3.Error`; also return `0` when `SUM` is `NULL` on an empty table |
| 5 | Insecure random generator | Bandit B311 | Low | 17 | `random.choice` is not cryptographically secure | Use `secrets.choice`, and return `None` when the catalog is empty instead of crashing |
| 6 | Naming convention | Pylint C0103 | Low | 9, 15, 28, 32, 36 | camelCase function names (`addSong`, `shufflePick`, ...) | Rename to snake_case (`add_song`, `shuffle_pick`, ...) |
| 7 | Missing docstrings | Pylint C0114 / C0116 | Low | 1, 9–43 | No module or function docstrings | Add a module docstring and a one-line docstring for every function |
| 8 | Unnecessary `else` after `return` | Pylint R1705 | Low | 22–25 | Extra nesting | Remove the `else` and de-indent |
| 9 | Multiple statements on one line | Pylint C0321 / Flake8 E701 | Low | 48 | `if ...: print(...)` on one line | Split onto two lines |
| 10 | Ambiguous variable name | Flake8 E741 | Low | 47 | `l` is easily confused with `1` / `I` | Rename to `loaded` |
| 11 | Lines too long | Flake8 E501 / Pylint C0301 | Low | 6, 10, 21, 49 | Lines over 79 characters | Wrap the calls across several lines |
| 12 | Code runs on import | Best practice | Low | 52 | `main()` runs whenever the module is imported | Wrap it in `if __name__ == "__main__":` |

Reports are in `reports/before/` and `reports/after/`.
