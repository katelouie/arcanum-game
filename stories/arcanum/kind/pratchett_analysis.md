# A CONDITION OF THE HEART
## Real Analysis for People Who Think in Stories

### by Terry Pratchett

*Cambridge University Press, 2008*
*Third Edition*

---

*For everyone who was told they weren't a math person.*
*You were. You just hadn't met the right book yet.*

---

### From the Preface to the Third Edition

This book began, as most worthwhile things do, with an argument.

In 1971, I was a second-year student at Cambridge, and I was failing Real Analysis. Not because I couldn't do it — I could, eventually, the way a man with no map can eventually find the sea by walking downhill — but because nobody had bothered to explain *why* we were doing it. The textbooks of the era treated proof as something the reader ought to already understand, the way recipe books assume you know what an oven is. They were written by mathematicians for mathematicians, which is rather like writing a dictionary in the language it's meant to teach.

I survived. Many of my classmates did not — not because they lacked ability, but because they lacked a bridge between the mathematics they knew (computational, practical, the kind where you get answers) and the mathematics they were being asked to do (abstract, structural, the kind where you get *truth*).¹

This book is that bridge.

It assumes you can do calculus. It assumes you are intelligent. It does *not* assume you have ever written a formal proof, because in the author's experience, the number of students who arrive at university having been properly taught proof-writing is approximately the same as the number of people who have been to the moon: technically nonzero, but not something you'd want to bet a curriculum on.²

¹ There is a meaningful difference between "I can't do this" and "nobody taught me how to do this," and the inability of most educational systems to distinguish the two is, in my view, a minor ongoing atrocity.

² As of this edition: twelve. The number of people who have been to the moon is twelve. The number of students who arrive at Cambridge having been properly taught proof-writing is, by my informal survey, about nine per year, and at least three of those learned it from their mathematician parents, which shouldn't count.

---

## CHAPTER 1
# In Which We Discuss What a Proof Is, Why We Need Them, and Why Nobody Bothered to Tell You This Earlier

### 1.1 The Problem

You know how to calculate.

I don't mean this dismissively. Calculation is a skill — a powerful, useful, magnificent skill. You can differentiate. You can integrate. You can solve differential equations, find eigenvalues, compute Fourier transforms. You have spent years learning to *get answers,* and you are very good at it.

The difficulty is that you have now arrived at a course — real analysis, probably, or abstract algebra, or topology — where getting the answer is not the point. The point is *proving the answer is correct.*³

This is, I appreciate, rather like being told that after years of learning to drive, you must now explain how an internal combustion engine works. While the car is moving. In French.

But here we are.

³ Some students, upon hearing this for the first time, experience a sensation not unlike grief. They are grieving for the version of mathematics where you plugged numbers into formulas and got results. That mathematics is not gone. It is simply no longer sufficient. This is what growing up feels like, in mathematics as in life.

### 1.2 What a Proof Actually Is

A proof is an argument.

Not the kind of argument you have with your landlord about the hot water, though it shares certain structural features.⁴ A mathematical proof is a sequence of statements, each of which follows logically from the previous ones (or from things we've already agreed are true), culminating in the thing we wanted to show.

That's it. That's the whole enterprise.

If this sounds simple, it's because it *is* simple — in the same way that "put words in an order that makes people feel things" is a simple description of writing a novel. The principle is straightforward. The execution is where you will spend the next several years of your life.

Let us begin with an example that requires no background beyond common sense.

**Theorem 1.1.** *There is no largest natural number.*

**Proof.** Suppose, for the sake of contradiction, that there IS a largest natural number. Call it N.⁵

Now consider N + 1.

N + 1 is a natural number (because adding 1 to a natural number gives you another natural number — this is what natural numbers *do*). And N + 1 is larger than N (because that is what adding 1 *does*).

But we said N was the largest natural number. We have just found one that is larger. This is a contradiction.

Therefore, our assumption was wrong. There is no largest natural number. ∎

That's a proof. You just read one. You may have understood it without any difficulty, because it is fundamentally an exercise in common sense: "you can always add one more."

The point is not the *result* — you already knew there was no largest number. The point is the *structure.* We assumed the opposite of what we wanted to show. We followed the assumption to its logical conclusion. The conclusion was absurd. Therefore the assumption was wrong.

This technique is called **proof by contradiction**, and it is one of approximately four tools you will need for the rest of this book.⁶

⁴ Though if your landlord's arguments were as logically rigorous as a mathematical proof, the hot water situation would likely have been resolved some time ago.

⁵ We call things letters in mathematics for the same reason we call characters names in novels: so we can refer to them later without starting from scratch each time. N is a fine name. It has the advantage of suggesting "Number" without being so on-the-nose as to embarrass anyone.

⁶ Four. There are essentially four proof techniques: direct proof, proof by contradiction, proof by contrapositive, and proof by induction. This is not unlike learning that there are essentially four basic plots in fiction: someone goes on a journey, a stranger comes to town, someone searches for something, and someone loses something and gets it back. All stories are variations on these four. All proofs are variations on the four techniques. Once you see this, mathematics becomes considerably less terrifying.

### 1.3 The Four Techniques (A Roadmap)

Before we discuss each technique in detail, let me tell you what they are, so that when we encounter them in the wild you will recognize them the way you recognize a chord progression in a song — not because you've memorized it, but because you've heard it before and your ear knows the shape.

**Direct Proof:** You want to show that A implies B. So you start with A, apply logic, and arrive at B. Walking from your front door to the pub. The path is clear. You go forward.

**Proof by Contradiction:** You want to show something is true. So you assume it's FALSE, follow the consequences, and arrive at something impossible. Like assuming your wallet is in your coat pocket, checking, finding it isn't, and concluding it must be somewhere else. Except in mathematics, the "somewhere else" is the truth.

**Proof by Contrapositive:** You want to show "if A then B." Instead, you show "if NOT B then NOT A," which is logically equivalent.⁷ This is surprisingly useful, because sometimes the back door is easier than the front.

**Proof by Induction:** You want to show something is true for ALL natural numbers. So you show it's true for 1, and then you show that if it's true for any number k, it must also be true for k+1. Then you sit back and let the dominoes fall.⁸

That's the toolkit. Four tools. Everything else is knowing when to use which one, which comes with practice, which comes with doing problems, which comes with not giving up, which comes with having a book that doesn't make you feel like an idiot for not already knowing this.

Which is what this book is for.

⁷ "If it's raining, then I have my umbrella" is logically equivalent to "if I don't have my umbrella, then it's not raining." These say the same thing. If you find the second one easier to verify than the first — good. That's the contrapositive, and you've been using it your entire life without knowing its name.

⁸ The metaphor of dominoes is traditional. I prefer to think of it as a rumor: you tell one person (the base case), and then you demonstrate that anyone who hears it will tell the next person (the inductive step). Given these two conditions, the rumor reaches everyone. Mathematical induction is gossip with better logical foundations.

### 1.4 Direct Proof: The Walk to the Pub

In a direct proof, you start with what you know and end with what you want to show. Each step follows from the previous one by logic, definition, or a result you've already established.

Here is the structure:

> **Want to show:** If A, then B.
>
> **Proof:** Assume A is true.
> [Logical step 1]
> [Logical step 2]
> ...
> Therefore B is true. ∎

An example.

**Theorem 1.2.** *If n is an even integer, then n² is an even integer.*

Before we prove this, we need to agree on a definition. An integer n is **even** if it can be written as n = 2k for some integer k.

This is important. In proof-based mathematics, every word has a *precise* meaning. "Even" doesn't mean "feels even" or "looks even" or "I checked a few cases and they were all even." It means *exactly one thing:* the number is 2 times some integer. When you use a definition in a proof, you are unpacking it — replacing the word with its precise meaning — the way a programmer replaces a function call with its implementation.⁹

**Proof.** Assume n is an even integer.

By definition, this means n = 2k for some integer k.

Then n² = (2k)² = 4k² = 2(2k²).

Let m = 2k². Since k is an integer, 2k² is an integer, so m is an integer.

Therefore n² = 2m, where m is an integer.

By definition, this means n² is even. ∎

Read that again. Slowly. Notice the structure:

1. We started with the definition of "even" (unpacked the word).
2. We did algebra (the part you already know how to do).
3. We ended by pointing at the definition again and saying "look — this matches."

The algebra is not the proof. The algebra is a *step in* the proof. The proof is the *argument* — the logical chain from "n is even" to "n² is even." The algebra merely gets us from one link to the next.

This distinction — between computation and argument — is the single most important thing this chapter can teach you. If you understand nothing else, understand this: **in proof-based mathematics, the computation serves the logic, not the other way around.**

⁹ If you are a computer science student, and you almost certainly are because this is the twenty-first century and everyone is a computer science student, then you already understand this principle perfectly. A function call and a definition are the same thing: a name that stands for a precise set of instructions. `isEven(n)` returns True if `n % 2 == 0`. The mathematical definition of "even" is `n = 2k for some integer k`. These are the same idea in different notation. You have been writing proofs in Python for years. You just didn't know that's what they were called.

### 1.5 Proof by Contradiction: Burning Down the Wrong House

We met this technique in Theorem 1.1 (there is no largest natural number). Let's examine it more carefully, because it is the technique that students find most disorienting, and also the most fun.¹⁰

The structure:

> **Want to show:** P is true.
>
> **Proof.** Suppose, for contradiction, that P is false.
> [Follow the consequences...]
> [Arrive at something impossible.]
> This is a contradiction.
> Therefore P must be true. ∎

The logic is: if assuming the opposite leads to nonsense, then the opposite must be wrong, so the original statement must be right.

This is, philosophically, the mathematical equivalent of the detective technique where you eliminate the impossible and whatever remains, however improbable, must be the truth. Except in mathematics, we don't need the word "improbable," because we deal in certainty.¹¹

**Theorem 1.3.** *√2 is irrational.*

This is one of the oldest proofs in mathematics — attributed to the Pythagoreans, who were reportedly so disturbed by the result that they drowned the man who discovered it.¹² We will not drown anyone. We will simply follow the logic.

**Proof.** Suppose, for contradiction, that √2 IS rational.

Then we can write √2 = p/q, where p and q are integers with no common factors. (Every rational number can be written this way — you just cancel until you can't cancel anymore.)

Squaring both sides: 2 = p²/q².

Therefore: p² = 2q².

This means p² is even (it equals 2 times something).

By Theorem 1.2, if p² is even, then p is even.¹³

So p = 2m for some integer m.

Substituting: (2m)² = 2q², which gives 4m² = 2q², which gives q² = 2m².

By the same argument, q² is even, so q is even.

But wait. We said p and q have no common factors. We've just shown they're BOTH even — they share a factor of 2.

Contradiction.

Therefore √2 is not rational. ∎

Notice something: we used Theorem 1.2 *inside* this proof. Proofs build on proofs. Theorems reference theorems. The whole structure of mathematics is a vast, interconnected argument where each result supports the ones above it, like a cathedral made entirely of logic.¹⁴

This is why the order matters. This is why your textbook is organized the way it is. This is why you can't skip Chapter 3.

¹⁰ I say "most fun" because there is a particular pleasure in assuming your opponent's position and then demolishing it from within. It is the mathematical equivalent of putting on a disguise, infiltrating the enemy's castle, and then setting it on fire. From the inside.

¹¹ I am aware that I have just quoted Sherlock Holmes in a mathematics textbook. I am not apologizing.

¹² The story is almost certainly apocryphal. But it speaks to something true: mathematical discoveries that overturn what we thought we knew are always disturbing. The irrationality of √2 meant that the Pythagorean belief in the perfection of whole-number ratios was wrong. Some truths are uncomfortable. Mathematics finds them anyway. This is either its greatest strength or its greatest cruelty, depending on your temperament.

¹³ Ah — but we proved "if n is even then n² is even." We're using it in the other direction: "if n² is even then n is even." Can we do that? Not automatically. "If A then B" does not automatically mean "if B then A." (If it's raining, I carry an umbrella. But carrying an umbrella doesn't make it rain.) We'd need to prove the converse separately. For this particular case, the converse is true and provable, and I've placed the proof in the exercises because you should try it yourself. Trust me, you can do it. You just did something harder.

¹⁴ A cathedral made entirely of logic sounds like something that would exist in a fantasy novel. I once wrote a story about a flat world on the back of a turtle and even THAT didn't have a logic cathedral. Perhaps I should have been more ambitious.

### 1.6 Proof by Contrapositive: The Back Door

Sometimes the front door of a proof is locked. The statement "if A then B" resists direct proof — A doesn't seem to lead anywhere useful, and B doesn't seem to follow from anything you can reach.

In these cases, try the back door.

The **contrapositive** of "if A then B" is "if not B, then not A." These are logically equivalent. Proving one proves the other.¹⁵

> **Want to show:** If A, then B.
>
> **Proof (by contrapositive).** Assume B is false.
> [Logical steps...]
> Therefore A is false. ∎

**Theorem 1.4.** *If n² is odd, then n is odd.*

Direct proof is awkward here — starting with "n² is odd" doesn't give you much to work with. But the contrapositive is: "If n is NOT odd (i.e., n is even), then n² is NOT odd (i.e., n² is even)."

We already proved that. It's Theorem 1.2.

**Proof.** We prove the contrapositive: if n is even, then n² is even.

This is Theorem 1.2. ∎

That's a valid proof. It's three lines long. It works because we already did the heavy lifting — we just needed to recognize that the problem we're facing is the *same problem* we already solved, viewed from a different angle.

This happens constantly in mathematics. Half of being good at proofs is recognizing which problem you're *actually* looking at. The other half is having a library of techniques to draw from.¹⁶

¹⁵ A story: I once spent three days trying to prove a statement directly, filling notebook after notebook with failed attempts, until my supervisor asked me if I'd tried the contrapositive. I had not. The proof took four lines. I considered asking for a refund on the three days, but the universe does not have a returns policy.

¹⁶ If you are a programmer — and again, you almost certainly are — this is *refactoring.* You recognize that two apparently different problems share underlying structure, extract the common logic, and reuse it. Mathematicians have been doing this since Euclid. Programmers reinvented it and gave it a name with more syllables. The principle is identical.

### 1.7 Proof by Induction: The Domino Argument

Induction is the technique for proving that something is true for ALL natural numbers — all of them, infinitely many, without checking each one individually, which would take rather a long time.¹⁷

The structure:

> **Want to show:** P(n) is true for all natural numbers n ≥ 1.
>
> **Base Case:** Show P(1) is true.
>
> **Inductive Step:** Assume P(k) is true for some arbitrary k ≥ 1. (This assumption is called the *inductive hypothesis.*) Show that P(k+1) must also be true.
>
> **Conclusion:** By induction, P(n) is true for all n ≥ 1. ∎

The logic: P(1) is true (base case). Since P(1) is true, P(2) is true (inductive step with k=1). Since P(2) is true, P(3) is true. Since P(3) is true, P(4) is true. And so on, forever.

It's dominoes. You set up the first one (base case). You prove that each domino knocks over the next (inductive step). Then every domino falls.¹⁸

**Theorem 1.5.** *For all natural numbers n ≥ 1:*

*1 + 2 + 3 + ... + n = n(n+1)/2*

**Proof.**

*Base case:* When n = 1, the left side is 1. The right side is 1(2)/2 = 1. They agree. ✓

*Inductive step:* Assume the formula holds for some k ≥ 1. That is, assume:

1 + 2 + 3 + ... + k = k(k+1)/2.

We need to show it holds for k+1:

1 + 2 + 3 + ... + k + (k+1) = (k+1)(k+2)/2.

Starting from the left side:

1 + 2 + ... + k + (k+1) = [k(k+1)/2] + (k+1)     ← using the inductive hypothesis

= k(k+1)/2 + (k+1)

= k(k+1)/2 + 2(k+1)/2

= [k(k+1) + 2(k+1)] / 2

= (k+1)(k+2) / 2     ← factoring out (k+1)

This is exactly what we wanted. ✓

By induction, the formula holds for all n ≥ 1. ∎

I want to draw your attention to one moment in that proof — the moment where we used the **inductive hypothesis**. That's line one of the calculation: we replaced "1 + 2 + ... + k" with "k(k+1)/2" because *we assumed we could.* That's the inductive hypothesis doing its job. You assume the formula works for k, and then you use that assumption to show it works for k+1.

Students often feel uncomfortable with this. "How can we assume the thing we're trying to prove?" The answer is: we're not assuming it for ALL n. We're assuming it for ONE specific value k, and showing that this forces it to be true for k+1. Combined with the base case, this covers everything.

Think of it this way: you're not claiming all the dominoes have already fallen. You're saying "IF this one has fallen, THEN the next one falls too." And since the first one definitely falls (base case), the chain is unbreakable.¹⁹

¹⁷ The natural numbers are 1, 2, 3, 4, ... and they go on forever, which is one of those facts that seems obvious until you think about it too hard, at which point it becomes either deeply disturbing or deeply beautiful, depending on whether you are a philosopher or a mathematician. Mathematicians tend to find it beautiful. Philosophers tend to find it a headache. This is the fundamental difference between the two professions.

¹⁸ I keep using the domino metaphor because it works, but I should note that actual dominoes are a poor model for mathematical induction in one important respect: real dominoes can be stopped by a finger, a table edge, or an inattentive cat. Mathematical induction cannot be stopped. Once the base case is established and the inductive step is proved, the conclusion is *inevitable.* There is no cat.

¹⁹ A student once asked me, "But what if the chain breaks at some number we can't see? What if there's a really big number where it stops working?" The answer is: there can't be. The inductive step proves that FOR ANY k, P(k) implies P(k+1). "For any" includes big numbers, small numbers, numbers you haven't thought of, and numbers so large they make the national debt look like pocket change. Mathematics does not make exceptions for numbers it hasn't personally met.

### 1.8 How to Read a Proof (A Survival Guide)

You will, in the course of your studies, encounter proofs in textbooks. Many of these proofs will be difficult. Some will be opaque. A few will make you question your life choices.²⁰

Here is how to read them:

**First pass:** Read the statement of the theorem. Understand what it *claims.* Do not read the proof yet. Ask yourself: "Does this seem true? Why might it be true?" Form an intuition. Even if the intuition is wrong, having one is better than approaching the proof as a wall of symbols to be endured.

**Second pass:** Read the proof. Don't try to understand every step. Just get the *shape* — what technique is being used? Is it direct proof, contradiction, contrapositive, induction? Where does the proof start? Where does it end? What's the key moment where something clever happens?

**Third pass:** Now go slowly. Line by line. At each step, ask: "Why is this true? What justifies this?" If you can answer, move on. If you can't, stop. Find out.

**Fourth pass:** Close the book. Try to reconstruct the proof from memory. Not word-for-word — just the *argument.* The shape of it. The key moves. If you can explain the proof to an empty room, you understand it.²¹

This process is slow. It is meant to be slow. A proof is not something you read — it is something you *work through.* The speed at which you work through it is not a measure of your intelligence. Some of the best mathematicians I know read proofs at the speed of continental drift. They just read them very, very *thoroughly.*²²

²⁰ This is normal. I have been a professional mathematician for forty years and I question my life choices approximately once per proof. The frequency does not decrease with experience. You simply become more comfortable with the questioning.

²¹ If the room is not empty — if, for instance, you are explaining a proof to a dog, or a poster of a musician, or your grandmother who does not speak English — this works equally well. The audience does not matter. What matters is the act of constructing the argument aloud, without notes, which forces you to identify the parts you actually understand and the parts you've been pretending to understand. The pretending is the dangerous part. Mathematics does not reward pretending.

²² The cult of speed in mathematics is one of the great lies of mathematical education. "She solved it so fast" is not a compliment — it is, at best, an observation about processing speed, which is the least interesting quality a mathematician can possess. The interesting qualities are persistence, creativity, and the willingness to be wrong for extended periods of time. These are slow qualities. They cannot be timed. Nobody ever wrote a great proof against a clock.

---

## Selected Excerpts from Later Chapters

---

### From Chapter 4: "The Epsilon-Delta Business, or How to Be Precise About Being Close"

#### 4.1 The Problem of "Close"

In calculus, you learned that the limit of f(x) as x approaches a is L. Your teacher probably said something like: "as x gets *closer and closer* to a, f(x) gets *closer and closer* to L."

This is fine as an intuition. It is not fine as a definition.

The difficulty is that "closer and closer" is a qualitative statement — it describes a *direction* without specifying a *standard.* How close is close? Closer than what? Closer than the distance between London and Paris? Closer than the width of a hair? Closer than the distance between two adjacent atoms?

The answer — and this is the answer that will define the rest of your mathematical life — is: **as close as anyone demands.**

That's the epsilon-delta definition. Someone demands a degree of closeness (ε, epsilon — think of it as an *extremely picky customer*). You provide a neighborhood around a (δ, delta — think of it as *how carefully you need to aim*) such that whenever x is within δ of a, f(x) is within ε of L.

The ε is the *challenge.* The δ is the *response.* The limit exists if you can *always* respond, no matter how unreasonable the challenge.²³

**Definition 4.1.** We say lim(x→a) f(x) = L if for every ε > 0, there exists a δ > 0 such that whenever 0 < |x - a| < δ, we have |f(x) - L| < ε.

Read that again. It's the most important definition in analysis. Every theorem in this book depends on it. It says:

1. Pick any positive number ε, no matter how small. (The challenge.)
2. I can find a positive number δ. (The response.)
3. Such that if x is within δ of a (but not equal to a), then f(x) is within ε of L.

And this must work for EVERY ε. Not just the ones that are convenient. Every single positive real number, down to the unimaginably tiny, must have a δ that works.

This is the mathematical equivalent of a promise: "No matter how picky you are, I can satisfy you." It is, I've always felt, rather romantic.²⁴

²³ I once described this to a student as follows: "Imagine you run a restaurant. A food critic comes in and says 'I want the steak done to within 0.5 degrees of exactly medium-rare.' You can do that — you're good at your job. The next day a different critic comes in and says 'within 0.01 degrees.' Harder, but you manage. Then someone comes in and says 'within 0.0000001 degrees.' The limit exists if you can ALWAYS deliver, no matter how absurdly precise the demand. If there's ANY level of precision you can't meet, the limit does not exist, and you should probably close the restaurant." The student found this helpful. His supervisor found it undignified. I stand by it.

²⁴ My wife, who is a novelist, once asked me to describe what I find beautiful about mathematics. I described the epsilon-delta definition. She said: "So it's a love story. Someone keeps asking for more, and the other person always delivers." I said: "That's exactly what it is." She said: "You should have led with that instead of the symbols." She was right. She is always right. This is unrelated to mathematics but important to document.

#### 4.2 A First Limit Proof

Let us prove that lim(x→3) (2x + 1) = 7.

You already know this is true — plug in x = 3, get 2(3) + 1 = 7. But "plug in and check" is not a proof. A proof must work for *every* ε, not just for plugging in. We must show the *process,* not just the answer.

**Proof.** Let ε > 0 be given. (This is how every epsilon-delta proof starts. The challenger has named their price.)

We need to find δ > 0 such that if 0 < |x - 3| < δ, then |(2x + 1) - 7| < ε.

Let's work out what we need. We want:

|(2x + 1) - 7| < ε

|2x - 6| < ε

2|x - 3| < ε

|x - 3| < ε/2

There it is. If |x - 3| < ε/2, then |(2x + 1) - 7| < ε. So we choose δ = ε/2.

*Now we write it up properly:*

Choose δ = ε/2. Then if 0 < |x - 3| < δ = ε/2, we have:

|(2x + 1) - 7| = |2x - 6| = 2|x - 3| < 2(ε/2) = ε. ✓

Therefore lim(x→3) (2x + 1) = 7. ∎

I want to be very clear about what just happened. We did the work *backwards* — we started with what we wanted (|f(x) - L| < ε) and figured out what δ needed to be. Then we presented the proof *forwards,* starting with "choose δ = ε/2" as if we'd known all along.

This is standard practice. Every epsilon-delta proof is secretly written backwards and presented forwards. The scratchwork is for you. The clean version is for the reader. This is not dishonesty — it's *editing.* The same thing a novelist does between the first draft and the final manuscript.²⁵

²⁵ Nobody writes a proof correctly on the first try. Nobody writes a novel correctly on the first try. Nobody writes anything correctly on the first try. The myth of effortless mathematical genius is exactly as true as the myth of effortless literary genius: it isn't. Behind every elegant proof is a notebook full of crossed-out attempts, wrong turns, and moments of profound despair. The difference between a good mathematician and a struggling student is not that the good mathematician doesn't struggle — it's that the good mathematician has learned to regard the struggle as the *work,* rather than as evidence of failure.

---

### From Chapter 6: "Sequences, or Patience as a Mathematical Virtue"

#### 6.1 What Sequences Are and Why They Move

A sequence is a list of numbers that goes on forever.

1, 2, 3, 4, 5, ...
1, 1/2, 1/3, 1/4, 1/5, ...
1, -1, 1, -1, 1, -1, ...
3, 3.1, 3.14, 3.141, 3.1415, ...

The first one grows without bound. The second one shrinks toward zero. The third one can't make up its mind. The fourth one is becoming π, one digit at a time, with the patience of a saint and the precision of a Swiss watchmaker.

The central question of this chapter is: **where does a sequence go?**

Not "where does it get to" — that implies a destination, a stopping point, and sequences never stop. They go on forever, which is rather the point. The question is: does the sequence *converge* — does it settle toward a specific value, getting closer and closer (in the epsilon-delta sense, not the hand-wavy sense) and staying there?

If it does, that value is the **limit** of the sequence.²⁶

²⁶ Sequences and limits are the backbone of analysis. Everything you will study in this course — continuity, differentiability, integration, series — is built on the idea of a sequence approaching a value. Master this chapter and the rest of the course is variations on a theme. Fail to master this chapter and the rest of the course is a foreign country whose language you don't speak. I cannot overstate how important this is. I am overstating it anyway, because I'd rather overstate it and have you pay attention than understate it and have you skip ahead.

#### 6.3 The Bolzano-Weierstrass Theorem

This is the big one. The theorem that separates the students who survive analysis from the ones who change majors. Not because it's difficult — it isn't, once you see it — but because it's *surprising,* and surprises in mathematics tend to be either delightful or terrifying, and often both.

**Theorem 6.7 (Bolzano-Weierstrass).** *Every bounded sequence of real numbers has a convergent subsequence.*

Let me translate. A bounded sequence is one that stays within some finite range — it doesn't fly off to infinity, it doesn't plunge to negative infinity, it just... stays put. Wanders around. Maybe oscillates. Maybe does something complicated. But it stays in the box.

The theorem says: no matter how wildly the sequence behaves *inside* the box, there's always a sub-pattern within it that converges to something.²⁷

Always. Not "usually." Not "under certain conditions." ALWAYS. Every bounded sequence, no matter how chaotic, contains within itself a thread of convergence.

I find this profoundly comforting, for reasons that are mathematical and also not.²⁸

**Proof sketch.** (The full proof is in §6.4. Here I give the idea, because the idea is more important than the details, and I will not apologize for saying so.)

The sequence is bounded. It lives in some interval [a, b]. Cut the interval in half. At least one half contains infinitely many terms of the sequence — possibly both halves do, but at least one must, because you can't put infinitely many terms in two finite boxes without at least one box getting infinitely many.

Pick the half with infinitely many terms. Now cut *that* in half. Again, at least one half-of-the-half has infinitely many terms. Pick it.

Keep going. At each step, you have a smaller interval with infinitely many terms in it. The intervals are nested — each one inside the previous — and they're shrinking, halving each time.

The widths go: (b-a), (b-a)/2, (b-a)/4, (b-a)/8, ...

These widths converge to 0. The intervals are closing in on a single point. And at each stage, you can pick a term of the sequence from within the interval.

The terms you picked form a subsequence. The intervals they live in are converging to a point. The subsequence converges to that point. ∎

That's Bolzano-Weierstrass. You trap the sequence in ever-smaller boxes until the boxes collapse to a point and the sequence has no choice but to converge.²⁹

²⁷ A bounded sequence, much like a person from a small town with limited resources but unlimited stubbornness, must eventually converge to *something.* The theorem does not specify WHAT it converges to, which is rather the point. The sequence doesn't know where it's going. It just knows it's going somewhere. This is, in the author's experience, the human condition in a nutshell, and also the plot of most novels worth reading.

²⁸ When I was twenty-two and failing this course for the first time, my supervisor — a kind woman named Dr. Hayes who had the patience of a sequence converging very, very slowly — told me that Bolzano-Weierstrass was her favorite theorem because it proved that even chaotic things contain order. "You feel chaotic," she said. "But somewhere in you there's a convergent subsequence." I didn't understand the mathematics yet. I understood her perfectly.

²⁹ The technique of nested intervals — trapping something in smaller and smaller boxes — appears throughout analysis. It is the mathematical equivalent of the detective who narrows the suspects until only one remains. You never find the limit by looking at it directly. You find it by eliminating everywhere it ISN'T.

---

### From Chapter 8: "Continuity, or the Art of Not Jumping"

#### 8.3 The Intermediate Value Theorem

We arrive at the theorem that, in my biased but considered opinion, is the most *satisfying* result in this book. Not the deepest. Not the most surprising. The most satisfying, in the way that a well-constructed plot is satisfying: everything that came before leads inevitably to this moment.

**Theorem 8.5 (Intermediate Value Theorem).** *Let f be a continuous function on the closed interval [a, b]. If f(a) < 0 and f(b) > 0 (or vice versa), then there exists a point c in (a, b) where f(c) = 0.*

In English: if a continuous function starts below zero and ends above zero, it must cross zero somewhere in between.

This is, at first glance, so obvious that it hardly seems worth proving. Of *course* it crosses zero. How could it not? It would have to jump over zero without passing through it, and continuous functions don't jump. That's what continuous *means.*

And yet — and this is the beauty and the frustration of analysis — "of course" is not a proof. Your intuition is correct. The theorem is true. But between the intuition and the theorem there is a gap, and the gap must be filled with logic, not hand-waving, because there exist pathological functions in mathematics that seem like they should behave nicely and do not, and the only way to distinguish the well-behaved from the pathological is to *prove things.³⁰*

**Proof.** Consider a function f walking from Ankh-Morpork to Lancre.³¹

I'm joking. But only slightly — the proof really is about a journey, and the technique is bisection, which we already met in Bolzano-Weierstrass.

We know f(a) < 0 and f(b) > 0. Somewhere between a and b, f must cross zero. We'll find where by narrowing the interval.

Let c₁ = (a + b)/2. The midpoint.

Compute f(c₁). There are three cases:

- If f(c₁) = 0, we're done. (Unlikely, but polite to mention.)
- If f(c₁) < 0, then f is negative at c₁ and positive at b, so the zero must be in [c₁, b]. Rename: a₁ = c₁, b₁ = b.
- If f(c₁) > 0, then f is negative at a and positive at c₁, so the zero must be in [a, c₁]. Rename: a₁ = a, b₁ = c₁.

Either way, we now have a new interval [a₁, b₁] that is half the size of [a, b], with f(a₁) < 0 and f(b₁) > 0.

Repeat. And repeat. And repeat. We get a sequence of nested intervals, each half the previous width, each containing the zero we're looking for.

By the Nested Intervals Theorem (a consequence of Bolzano-Weierstrass), the intervals converge to a single point. Call it c.

Since f(aₙ) < 0 for all n, and aₙ → c, and f is *continuous,* we have f(c) ≤ 0.

Since f(bₙ) > 0 for all n, and bₙ → c, and f is continuous, we have f(c) ≥ 0.

Therefore f(c) = 0. ∎

Everything came together. The interval bisection from Chapter 6. The convergence of nested intervals. The definition of continuity from earlier in this chapter. The Intermediate Value Theorem is not a standalone result — it's the *payoff* of everything you've learned so far.

This is what I mean when I say mathematics is storytelling. Every chapter is an act. Every theorem is a scene. And the Intermediate Value Theorem is the moment in the third act where all the threads converge and you realize the story was going *here* all along.³²

³⁰ The existence of pathological functions is one of the great unsettling features of mathematics. A function can be continuous everywhere and differentiable nowhere. A function can be zero everywhere except at one point. A function can oscillate infinitely many times in any interval, no matter how small. These functions are not common in nature, but they exist in mathematics, and their existence is why we prove things: because intuition, however good, is not reliable in a universe that contains the Weierstrass function.

³¹ Assuming the function can hold its breath. The River Ankh is, technically, not so much a body of water as a body of water's regrettable life choices.

³² I realize I have now compared mathematics to storytelling approximately forty-seven times in this textbook. I am not going to stop. I spent most of my twenties torn between mathematics and fiction, and while I chose mathematics — the proofs were more satisfying than the plots, and the characters, while less colorful, were infinitely more reliable — I have never stopped believing they are the same art practiced in different notation. A proof and a story both start somewhere, go somewhere, and arrive at a conclusion that feels both surprising and inevitable. The good ones, anyway. The bad ones just wander.

---

### Afterword

If you've reached this point, you can do real analysis.

Not because you've read this book — reading is necessary but not sufficient, as we mathematicians say about most things.³³ You can do real analysis because you've worked through it. You've done the proofs. You've made mistakes and caught them and made them again and caught them again and eventually, on the fourth or seventh or fifteenth attempt, written something correct and clean and true.

You've learned that "I don't understand" is not a confession of weakness but the beginning of understanding. You've learned that the gap between computation and proof is not a measure of your ability but a measure of what you were taught. You've learned that mathematics is not a gift. It is a skill. A difficult, beautiful, occasionally maddening skill that can be acquired by anyone willing to put in the time.

I wrote this book because I believe that. I believe it because I was once a student who nearly drowned in this material, and I survived not because I was talented but because I was stubborn, and because one kind woman told me that even chaotic things contain convergent subsequences.

She was right.

You are bounded. You are persistent. By Bolzano-Weierstrass, you converge.

To what? I don't know. The theorem doesn't specify. That's rather the point.

Good luck.

T. Pratchett
Cambridge, 2008

³³ "Necessary but not sufficient" is a phrase that, once learned, will improve approximately 40% of your arguments about everything, not just mathematics. "Exercise is necessary but not sufficient for good health." "An apology is necessary but not sufficient for forgiveness." "Reading a textbook is necessary but not sufficient for understanding real analysis." I gift you this phrase. Use it wisely and often.

---

*From the back cover:*

*"The best mathematics textbook I've ever read, and I've read all of them, including the ones that are good." — Dr. Helen Hayes, Cambridge*

*"He made me understand the Bolzano-Weierstrass theorem by comparing bounded sequences to people from small towns. I'm from a small town. I cried." — Student review, Cambridge Mathematical Tripos, 2009*

*"Pratchett's great tragedy is that he only ever wrote one novel. His great triumph is that he wrote this." — Times Literary Supplement*
