# Anti-Patterns

These are technical prose anti-patterns. Fix the underlying failure rather than merely deleting the surface phrase.

## Empty Importance Signals

Avoid standalone sentences that only announce importance:

- "That matters."
- "This is important."
- "The point is narrow but important."
- "This is worth noting."

Repair by naming the actual consequence or distinction:

> Skyrms's setup, by contrast, fixes a theorem-level protocol.

## Odd Negations, Rathering, and Denial-Then-Assertion Frames

The pattern "not A, it is B" or "not A, but B" is often filler. The same failure often appears in adjacent sentences:

- "We do not claim that A. We claim that B."
- "The point is not A. The point is B."
- "This is not about A. It is about B."
- "The issue is not A. The issue is B."

Prefer a direct B claim. Also scan for negative statements that do not have the exact "not A, but B" form. If a simple positive sentence says the same thing, use it.

Anti-pattern:

> We accept the distinction, but our use of it is not to confine the paper to theorem statements. The unified theorem supplies the common mathematical object, and the later sections ask what argument forms that object makes available.

Pattern:

> We accept the distinction, and we will be interested in theorems as well as arguments. The unified theorem supplies the common mathematical object, and the later sections ask what argument forms that object makes available.

If the limitation matters, add it after the affirmative claim and make its scope precise. Keep the negative side only when it:

- blocks a live misreading;
- records a source's taxonomy;
- states a formal exclusion;
- separates concepts the reader is likely to conflate.

Bad:

> That is not a victory for every Dutch book argument. It is a restriction on what we claim.

Better:

> This restricts what we claim about Dutch book arguments.

Bad:

> We do not claim that the theorem settles every Dutch book argument. We claim that it identifies the shared price-posting structure.

Better:

> The theorem identifies the shared price-posting structure of the three arguments. It does not settle the normative force of every Dutch book argument.

## Filler Labels

Suspect phrases:

- "the key insight is";
- "the broader implication is";
- "for present purposes";
- "in this context";
- "it is helpful to note";
- "this raises the question."

Keep them only when they change scope or prevent a real misreading. Usually the following clause should stand on its own.

## Fake Agency

Watch for abstractions doing actions they cannot do:

- "the theorem wants";
- "the section solves";
- "the comparison prices the missing information";
- "the argument remembers";
- "the distinction asks."
- "In the direction from safety to universal adequacy, the unified theorem gives Piccione--Rubinstein consistency."

Repair by naming the actual relation: states, shows, entails, rules out, represents, records, assumes, requires, or motivates.

Bad:

> In the direction from safety to universal adequacy, the unified theorem gives Piccione--Rubinstein consistency.

Better:

> If a belief is safe in the coherence game, the unified theorem implies that it is Piccione--Rubinstein consistent.

## Vague Demonstratives

Words such as "this", "that", "these", and "it" need clear antecedents. If the antecedent is a whole paragraph or an unstated idea, name the object.

Bad:

> This shows the issue.

Better:

> The zero denominator shows why the representation condition imposes no local constraint at that information set.

## Noun Stacks

Avoid long stacks before the head noun:

- "Lewis--Teller price schedule object";
- "local oracle-free side-payment fee component";
- "full valuation-dependent arbitrage endpoint."

Unpack into clauses naming the object and the relation.

## Over-Softening

Remove repeated hedges once the qualification has been made.

Avoid stacks such as:

- "might perhaps";
- "in some sense";
- "arguably may";
- "it seems plausible that."

Use one accurate hedge or none.

## Pull-Quote Endings

Avoid ending paragraphs with aphorisms, slogans, or generalities that sound detached from the technical work. End with the local consequence, limitation, or next object instead.

## Metronomic Rhythm

Avoid strings of sentences with the same shape:

> This X does Y. This Z does W. This Q does R.

Vary sentence length only when it serves the paragraph path. Do not add fragments for drama.
