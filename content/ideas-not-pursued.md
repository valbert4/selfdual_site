# Ideas Sketched But Not Pursued

This page is for ideas that are useful to know about but are not current
highest-priority build targets.

The goal is not to hide abandoned routes. The goal is to prevent contributors
from spending weeks rediscovering why a tempting route was deprioritized.

## Categories

### Saturated Relaxations

Several LP, SDP, and aggregate-mixture tests were implemented and found to
saturate. They are not failures; they are evidence that the remaining problem is
not visible to those relaxations.

Examples to expand:

- aggregate residual biweight mixtures;
- anchored-aggregated Mode-1 mixture;
- length-40 B4, which saturates to Delsarte;
- weight-hierarchy partition, which is non-vacuous but kills no current row.

### Validation-Heavy Routes

Some promising routes require more stringent certificates before they should
affect the public menu count:

- A3/Schrijver-style SDP cuts need exact constraint systems and replayable
  certificates;
- Mode-1 per-coset gluing needs exact image counts and witness-preserving
  reconciliation;
- LP-derived infeasibilities need exact input reconstruction before exact
  simplex arithmetic is trusted.

These belong on the [Validation Standards](audit-trail.md) page, but this page
can summarize why not to rebuild the same route unchanged.

### Too Weak At The Current Scale

Some ideas are mathematically correct but too loose:

- plain constant-weight bounds at length 56;
- B4 on the residual minimum-word configuration;
- further aggregate refinements that preserve continuous slack.

### Parked For Later

Some directions remain conceptually interesting but need a sharper trigger:

- genus-4 lift constraints with actual code relations;
- doubly-anchored higher SDP objects;
- CFT or modular-bootstrap constraints beyond the currently forced code data;
- heuristic construction searches.

### Closed By An Exact Argument

These are not parked; they are ruled out as written.

- **Construction A as a bridge to an extremal 72-dimensional lattice.** The
  Construction-A lattice of the code, `Λ = (1/√2){x : x mod 2 ∈ C}`, always
  contains `√2·Z^72` (the zero codeword), so `√2·e_1 ∈ Λ` has norm `2`. Its
  minimum norm is therefore `2`, not `8`: it is even unimodular but **not**
  extremal (an extremal even unimodular lattice in dimension 72 has minimum norm
  `8`). The converse — searching a known extremal lattice for a `√2·Z^72`
  coordinate frame whose cosets form a doubly-even self-dual code — is vacuous
  for the same reason: an extremal lattice cannot contain such a frame, since the
  frame would inject a norm-`2` vector below the minimum. Plain Construction A is
  not the code↔extremal-lattice bridge in either direction. What does carry over
  is the methodological mirror: anchoring a minimal vector and using design
  moments to pin the cross-shell distribution exactly, the lattice image of the
  anchored-design machinery used on the code side.

## How To Present A Parked Idea

Each idea should have:

```text
Idea:
Why it was tempting:
What was tried:
What happened:
Why it is parked:
What would make it worth revisiting:
Source files:
```
