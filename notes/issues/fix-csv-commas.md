# Fix CSV comma-in-cell bug

Current manual pipe splitting breaks when user comments contain commas or newlines.
pandas.to_csv already handles quoting → just stop parsing markdown manually.

**Priority**: P1
**Status**: Todo