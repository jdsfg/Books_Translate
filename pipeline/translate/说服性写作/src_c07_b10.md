#### Application Problems

**Q1. Diagnose this opening.**

> Throughout my undergraduate career, I have developed a deep passion for understanding the complex dynamics of climate science. From my freshman year, when I took my first introductory course on climate change, I have been captivated by the urgent questions our planet faces, and I have pursued these questions through coursework, internships, and research opportunities.

Run the 6 Moves and identify the pitfalls.

Hint

The opening commits multiple pitfalls of the undergraduate-register type.

**Answer:** Move 1 failed (faculty reader registers undergraduate-register). Move 2 failed (no specific research direction; _climate science_ is a topic). Move 3 failed (the _deep passion_ and _captivated by urgent questions_ register is wrong-genre). Move 4 failed (zero specifics — no projects, no methods, no findings). Move 6 failed (an AI given the prompt _write a PhD SOP for a climate science applicant_ would produce this).

Pitfalls: undergraduate-register; CV-in-prose (the _coursework, internships, research opportunities_ enumeration); inflated-language (_deep passion, urgent questions our planet faces_).

**Q2. Rewrite using the four-sentence template.**

The candidate has worked on a senior thesis using machine learning to predict regional precipitation patterns under different emissions scenarios, working with Professor Chen's lab. They produced a model that improved on baseline accuracy by 14% in the U.S. Southwest. Rewrite the opening paragraph using the four-sentence template.

Hint

Lead with the research direction. Anchor to the senior thesis. Name the next question. Sketch the methodological approach.

**Answer:**

> The research direction I propose to pursue is the integration of machine-learning regional climate models with land-surface process modeling to improve precipitation prediction at the basin scale, with attention to model performance under emissions scenarios outside the training distribution. The direction emerged from my senior thesis, completed last spring, in which I built a transformer-based regional precipitation model that improved baseline RMSE by 14% in the U.S. Southwest under RCP 4.5 but degraded substantially (RMSE +21% over baseline) under RCP 8.5 in the same region — a degradation that suggests the model is learning patterns specific to the training-distribution forcing rather than generalizable physical relationships. The next question this raises is whether physics-informed constraints on the model's hidden representations can recover generalization to high-warming scenarios while preserving the basin-scale accuracy gains, and the proposed dissertation would test this through a series of architectural ablations and out-of-distribution evaluations on the CMIP6 ensemble. Methodologically, this requires expertise I am beginning to develop in physics-informed neural networks (I have implemented a basic version for a course project; not yet at research scale) combined with the regional-modeling background I have built in Professor Chen's lab.

The rewrite states the research direction, anchors to the senior thesis with specific findings (14% improvement; RMSE +21% under RCP 8.5), articulates the next question, and sketches the methodological approach with honest acknowledgment of methodological gaps.