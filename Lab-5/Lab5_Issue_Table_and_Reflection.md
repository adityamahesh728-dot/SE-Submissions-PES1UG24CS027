# Lab 5: Static Code Analysis — address_book.py

**Name:** Aditya M  **SRN:** PES1UG24CS027

## Score summary

| Tool | Before | After |
|---|---|---|
| Pylint | 5.47 / 10 | 10.00 / 10 |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 4 issues | 0 issues |

## Issue table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B324 weak MD5 hash | Security (High) | 19 | `hashlib.md5` is a broken hash, flagged for security use | Replaced with `hashlib.sha256` |
| B301 / B403 pickle | Security (Medium/Low) | 3, 67 | `pickle.load` can run arbitrary code if the backup file is tampered with | Replaced pickle with `json` for backup and restore (data is plain dicts/strings) |
| B105 hardcoded password | Security (Low) | 6 | `SYNC_PASSWORD = "contacts-demo"` stored in source, and never used | Removed the unused constant |
| E225 | Style (Flake8) | 23 | `found=[]` missing whitespace around operator | `found = []` |
| E303 | Style (Flake8) | 47 | 3 blank lines before function | Reduced to 2 |
| E231 | Style (Flake8) | 84 | Missing space after comma | Added space |
| E501 | Style (Flake8) | 85 | Line 86 chars > 79 | Wrapped the print call across two lines |
| C0103 invalid-name | Convention (Pylint) | many | camelCase function/argument names (`addContact`, `fullName`, `fileName`...) | Renamed to snake_case (`add_contact`, `full_name`, `file_name`...) |
| C0114 / C0116 | Convention (Pylint) | 1 + all functions | Missing module and function docstrings | Added docstrings |
| W0718 broad-exception-caught | Warning (Pylint) | 34 | `except Exception` hides unrelated errors | Changed to `except KeyError` |
| C0200 consider-using-enumerate | Convention (Pylint) | 49 | `range(len(names))` loop | `for i, name in enumerate(sorted(contacts), start=1)` |
| W1514 unspecified-encoding | Warning (Pylint) | 54 | `open()` without encoding | Added `encoding="utf-8"` to all text-mode opens |

Extra: wrapped the script's call to `main()` in `if __name__ == "__main__":` so importing the module does not run the demo.

## Commits

1. `Fix Bandit issues: drop pickle for json, remove hardcoded password, replace MD5 with SHA-256`
2. `Fix Flake8 formatting issues (E225, E303, E231, E501)`
3. `Fix Pylint issues: snake_case names, docstrings, enumerate, encoding, specific exception`

## Reflection

**1. Which tool was most useful and why?**
Bandit caught the issues with real consequences (unsafe pickle deserialization and a weak hash), things I would not have noticed by reading the code for behavior. Pylint raised the score the most and improved readability, while Flake8 was the quickest to fix.

**2. Did any report contain false positives or low-value warnings?**
The hardcoded password warning (B105) was Low severity and the constant was unused, so it was harmless in practice, but removing it is still correct hygiene. The MD5 use was only for a short display ID, so it was not truly security critical, yet switching to SHA-256 cost nothing.

**3. How did you decide what to fix first?**
By severity: Bandit High and Medium first, then Flake8 (mechanical and fast), then Pylint. Doing one tool per commit kept each change easy to review.

**4. Did the fixes change behavior?**
Output of the program is the same except that the contact ID changes (different hash) and the backup file is now `contacts.json`. Renaming functions would break external callers, so in a larger project it would need a deprecation step.

**5. How does static analysis help code quality and maintainability?**
It catches bugs, insecure patterns and style drift automatically before runtime, enforces a consistent standard across a team, and works well in CI so problems are found on every commit instead of in review or production. It does not replace tests, since it cannot verify that the logic is correct.
