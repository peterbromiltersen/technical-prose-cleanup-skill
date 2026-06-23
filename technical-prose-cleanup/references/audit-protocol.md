# Audit Protocol

Use these checks paragraph by paragraph and sentence by sentence. They are diagnostics, not mechanical rewrite rules. A cleanup pass is complete only when every prose sentence in scope has been assigned a role and audited against the paragraph job.

## Paragraph Job

Identify the paragraph's main job before editing:

- motivate a model or construction;
- define an object;
- prepare a formula;
- interpret a formula;
- state an example or sanity check;
- state a theorem idea;
- mark a limitation;
- position a source or objection;
- connect one part of the argument to the next.

If a true sentence pulls the reader away from that job, move it, shorten it, or remove it.

## Sentence Inventory

For each prose paragraph, list each sentence mentally or in notes before editing. For each sentence decide whether it:

- defines an object;
- prepares notation or a formula;
- interprets notation or a formula;
- states a claim;
- marks a limitation;
- positions a source or objection;
- gives an example;
- connects the paragraph to the next step.

If a sentence has no role, delete it. If it has a role but hides the role behind filler, rewrite it. Do not delete a good metaphor merely because it is metaphorical; delete it only when it replaces the technical claim, overstates the claim, or reads as generic flourish.

## Phrase Audit

For each nontrivial technical noun phrase, identify:

1. the head noun;
2. each modifier;
3. what each modifier attaches to;
4. what literal claim the phrase makes;
5. whether that claim is true, useful, and readable here.

Reject phrases that hide mechanism in a noun stack. Prefer clauses that name the object and the relation.

## Sentence Audit

For each sentence, identify:

1. the main subject;
2. the main verb;
3. the object or complement;
4. prepositions and other relational words;
5. pronouns and demonstratives;
6. what the sentence literally says.

Reject sentences where the nouns are right but the grammar assigns the wrong roles. The subject must be able to do what the verb says.

## Math-Language Fit

Natural-language mathematics must match object types.

- Sets contain members; subsets are subsets of sets.
- Functions map arguments to values, assign values to arguments, and have domains and codomains.
- Relations hold between objects or relate objects.
- Values equal values; variables range over domains; tuples have coordinates or components.
- Histories extend histories; plays are terminal histories; information sets contain histories; distributions assign probability or mass.
- Theorems state or imply claims. Proofs establish claims. Arguments support conclusions.

Before accepting a sentence with math, ask what type each object has and whether the grammar fits that type.

## Paragraph Path

Prefer this order when possible:

1. plain-language orientation;
2. minimal notation;
3. formula or definition;
4. immediate interpretation;
5. example or consequence.

Do not open a paragraph with a source name, theorem label, objection, or verdict unless the previous sentence has prepared its role.

## Wrong-Sentence Challenge

Before writing a replacement sentence, imagine being told:

> There is something seriously wrong with that sentence in this context.

If a problem is visible in scope, grammar, source attribution, type discipline, direction of explanation, or relation to the paragraph, revise before inserting the sentence.
