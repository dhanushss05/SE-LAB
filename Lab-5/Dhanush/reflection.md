# Lab 5 – Reflection
**Name:** Dhanush S S | **SRN:** PES1UG24AM082 | **Section:** B

**1. Which issues were the easiest to fix, and which were the hardest? Why?**
The easiest were the style issues: long lines, the one-line `if`, the `l` variable name, docstrings and snake_case renames. They are mechanical and don't change behaviour. The hardest were the security issues. To fix the SQL injection I had to understand why string formatting is dangerous and switch to parameterised queries. To replace pickle I had to check that JSON could still represent the playlist and that the save/load round-trip still worked. The mutable default argument was also tricky because the code *looks* correct and the bug only appears across several calls.

**2. Did the static analysis tools report any false positives? If so, describe one example.**
Bandit B311 (use of `random`) is close to a false positive here. Shuffling songs is not a security or cryptographic task, so `random.choice` is fine in practice. I still switched to `secrets.choice` because it costs nothing and gives a clean report, though adding `# nosec B311` with a justification would also have been reasonable. B403 (importing pickle) is also only a warning about the import; the real risk is `pickle.loads` on untrusted data (B301).

**3. How would you integrate static analysis tools into your actual software development workflow?**
I would run Flake8 and Pylint on save in the editor, and run all three tools in a pre-commit hook so problems are caught before they reach the repo. In CI (for example GitHub Actions) I would run them on every pull request and fail the build if there are Bandit medium/high findings, Flake8 errors, or a Pylint score below a threshold such as 9.5. A shared config (`.pylintrc`, `setup.cfg`) keeps the rules the same for the whole team.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**
The Pylint score went from 4.57 to 10.00, and the Bandit and Flake8 issue counts went from 4 and 7 to 0. The code is now safe against SQL injection and malicious playlist data. It no longer shares state between calls through the mutable default, and it no longer hides errors behind a bare `except`. It also handles an empty catalog: `shuffle_pick` returns `None` and `total_plays` returns `0` instead of crashing or returning `None`. Snake_case names, docstrings and shorter lines make it easier to read, and the `__main__` guard means the module can be imported without running the demo. The program still produces the same output.
