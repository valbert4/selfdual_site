# Current Map

## What Is Forced

- Any `[72,36,16]` Type II code has a fixed Gleason weight enumerator.
- In particular, the number of weight-16 codewords is `A_16 = 249849`.
- Anchoring one weight-16 word forces a residual `[56,21,>=16]` object with
  exactly `5082` weight-16 words.
- Anchoring again produces a finite length-40 menu.

## What Has Been Reduced

The current public reduction is:

```text
[72,36,16]
  -> [56,21,>=16]
  -> [40,k,>=16] menu
  -> [24,1,24]
```

The length-40 menu is the best public progress artifact:

```text
132 raw candidates
60 eliminated
72 surviving
```

## What Remains

The remaining progress is likely to come from:

- route-3A existence or empty-exhaust work on unresolved length-40 rows;
- exact integer obstructions that cannot be absorbed by continuous relaxations;
- new anchored structures beyond the saturated single-anchor SDP line;
- an actual construction.

## Related Pages

- [The Hierarchy](hierarchy.md)
- [Length-40 Menu](menu-summary.md)
- [Tests](tests/index.md)
- [Validation Standards](audit-trail.md)
