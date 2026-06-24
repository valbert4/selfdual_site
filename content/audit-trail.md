# Validation Standards

These are the standards required for a test to change the headline menu count.
Every claimed elimination must be independently checkable.

## Public Rule

```text
No public status change without exact input data, an exact certificate, or an
independent verifier.
```

## Proof-Grade Eliminations

A published elimination says:

- what mathematical object is tested;
- which exact necessary condition fails;
- what certificate or exact verifier confirms the failure;
- which row or branch is affected;
- how the certificate can be replayed from public data.

## Validation Targets

Some methods are useful but need stronger public certificates before they count
as eliminators:

- A3/Schrijver-style SDP tests need an exact constraint system, exact objective
  data, and a replayable certificate.
- Mode-1 per-coset gluing needs independently checked image counts and
  witness-preserving reconciliation.
- Pairwise/subgroup coset coupling needs exact normalization across all local
  tables.
- LP-derived infeasibility needs exact reconstruction of the input coefficients
  before exact simplex arithmetic is trusted.

## Downloadable Computations

The same standard applies to downloadable computational artifacts:

- JSON enumerator files include provenance and generation notes.
- The triweight routine bundle separates source code from large generated
  caches and machine-specific logs.
- Large coefficient objects are distributed in machine-readable form, with
  compact checksums or summaries for the webpage.

## Why This Matters

The project distinguishes:

- proof-grade eliminations;
- saturated relaxations;
- useful probes;
- open validation targets.

That distinction is central to making the project community-verifiable.
