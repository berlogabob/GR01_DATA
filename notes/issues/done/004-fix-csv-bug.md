# title: Fix CSV comma-in-cell bug

Current manual pipe splitting breaks when user comments contain commas or newlines
pandas to_csv already handles quoting → stop manual parsing

**Assignee**: @me
**Priority**:
**Status**: Todo

