# title: Replace MarkItDown parsing with direct pandas read_excel

Simpler + more reliable path:
Excel → pandas.read_excel() → clean text columns → to_csv
Keep MarkItDown only as fallback for completely broken files

**Assignee**: @me
**Priority**:
**Status**: Todo

