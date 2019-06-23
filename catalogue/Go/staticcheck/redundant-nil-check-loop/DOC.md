**What it does:** Removes redundant `nil` checks.
**Reference:** See [Statticheck](https://staticcheck.io/docs/checks#S1009)
**Author:** Anonymous
**Id:** staticcheck-replace-with-bytes-equal-1004
**Tags:** ["Style"]
**Known problems:** This rule is only allowed on maps and slices, but may match on if statements that check pointers. Checks on pointers should not be removed.
