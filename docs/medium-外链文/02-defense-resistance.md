# Why Your Genshin Damage Isn't What You Think: The Defense & Resistance Tax

*You've pulled the right artifacts, stacked your crits, and picked your best weapon. Your DPS still doesn't hit like it should. The reason is almost always two numbers you've never looked at: enemy defense and enemy elemental resistance.*

---

Genshin Impact's damage formula has a quiet multiplier that most players skip: the **defense multiplier**. And right next to it sits **elemental resistance** — a second tax that eats more damage than you'd think. Here's the full picture, with the actual math.

## The defense tax: why "same level" isn't actually equal

The defense multiplier is its own independent block in the damage formula. The full equation looks intimidating, but the result is surprisingly simple:

> **DEF multiplier ≈ (your level + 100) ÷ [(your level + 100) + (enemy level + 100) × k]**

where **k = (1 − DEF shred) × (1 − DEF ignore)**.

Enemy defense values scale linearly: **DEF = 5 × enemy level + 500**. A level-90 enemy has roughly **950 DEF**.

Now do the math for a level-90 character fighting a level-90 enemy with zero DEF shred:

> 190 ÷ (190 + 950) ≈ **16.7%**

That's not "a small penalty." That's your damage being cut to **less than one-sixth of its raw value** before any other stat even enters the calculation. This is why level-pressured content (late Spiral Abyss, higher world levels) makes the same build feel dramatically weaker even though your own numbers haven't changed.

## DEF shred: the 90% hard cap

DEF shred sources **add** together, then the total is hard-capped at **90%**. No amount of additional shred pushes past that.

| Source | Shred | Type |
|---|---|---|
| Lisa A4 passive | −15% | DEF shred |
| Razor C4 | −15% | DEF shred |
| Skirk C2 | −23% | DEF shred |
| Ayaka C4 | −30% | DEF shred |
| Nahida C2 | −30% | DEF shred |
| Some weapons / artifacts | flat amount | DEF shred or DEF ignore |

Example: Lisa + Skirk + Razor = 15% + 23% + 15% = **53% DEF shred** — well below the cap. At that point, adding another source has diminishing returns. The more meaningful move is usually adding DEF *ignore*, which is a **separate multiplicative layer**: it multiplies *after* DEF shred, not in place of it.

## Elemental resistance: the three-tier formula that trips everyone up

Resistance (RES) is calculated **per damage type** (physical, Pyro, Hydro, Electro, Cryo, Geo, Anemo, Dendro). The multiplier has three tiers:

| RES range | Damage multiplier | What it means |
|---|---|---|
| RES < 0 (negative) | 1 − RES/2 | Still adds damage, but only at **half the face value** |
| 0 ≤ RES < 75% | 1 − RES | One-for-one: 10% RES = 90% damage |
| RES ≥ 75% | 1 ÷ (4×RES + 1) | Severe diminishing returns; further RES is almost worthless |

**The classic example that surprises people:**

An enemy with **10% physical RES** normally takes 90% of your physical damage. Now your team triggers Superconduct (−40% physical RES):

> 10% − 40% = **−30% RES** → multiplier = 1 − (−0.30/2) = **1.15**

That's a jump from 0.90 to 1.15 — a **+27.8%** damage boost. Not the "40% more damage" the face value suggests. The negative-RES penalty is only half-weighted. This is the "negative RES only counts half" rule, and it's the single most common source of confusion when planning physical teams.

## Where the good RES shred actually comes from

| Source | RES shred | Scope |
|---|---|---|
| Viridescent Venerer 4pc | −40% | The element that triggered Swirl, 10s — **the single best RES shred in the game** |
| Zhongli jade shield | −20% | All elements + physical, passive, permanent |
| Superconduct | −40% | Physical only (Cryo + Electro) |
| Anemo sub DPS / supports | −40% | The element that triggered Swirl |

A physical team with **Superconduct (−40%) + Zhongli shield (−20%)** hits **−50% physical RES** on a 10% physical-resistance enemy:

> 10% − 50% = **−40% RES** → multiplier = 1.20

That's why physical DPS teams almost always include a Cryo + Electro duo *and* Zhongli. The combo is cheap, reliable, and the single biggest damage swing available to a free-to-play player.

## DEF shred vs. RES shred: which one to build?

They're **independent multiplicative zones** — they don't stack against each other; each multiplies the final damage separately.

- **DEF shred** is universal. It helps against everything. But it's hard-capped at 90%, and the meaningful sources are locked to specific characters.
- **RES shred** is targeted. One good source (VV 4pc or Zhongli) can swing a single element's damage by 30–40%. For reaction teams (Overloaded, Bloom, Super-Bloom), RES matters more than DEF because those reactions **ignore DEF entirely** — they only take RES.

**Practical rule of thumb:**
- General team: **one strong RES source** (VV or Zhongli) is enough.
- Single-element main DPS team: **VV 4pc** is the highest-value free RES shred available.
- Physical team: **Superconduct + Zhongli** to hit −50% physical.
- Reaction team: RES > DEF, period.
- Late Spiral Abyss: both zones are high on the enemy side; stacking both types gives the biggest ceiling.

---

*This is the digest. The full breakdown — per-character DEF shred table, all RES sources by element, DEF-ignoring vs DEF-shreding distinction, and a worked damage example with real numbers — lives at [Teyvat Starter Guide's Defense & Resistance Mechanics page](https://genshin-guide-one-five.vercel.app/guides/defense-guide-en.html). If you're building a physical team specifically, their [Superconduct reaction guide](https://genshin-guide-one-five.vercel.app/guides/superconduct-guide-en.html) covers the Cryo + Electro physical-team math in more detail.*
