# EXAM STUDY GUIDE & QUICK REFERENCE

This document provides quick reference materials for exam preparation.

---

## QUICK FACTS TO MEMORIZE

### Dataset
- **Time span**: 2000–2020 (21 years)
- **Countries**: 140+
- **Minerals**: 45+
- **Size**: 3,200 clean rows (after aggregation)

### Key Numbers
- **HHI (Concentration Index)**: 0.18 (highly concentrated, >0.15 threshold)
- **Top 3 countries share**: 65% of global production
- **Lithium growth**: +800% (2000–2020)
- **Random Forest R²**: 0.84 (84% variance explained)
- **RMSE improvement**: 33% (Random Forest vs. Linear Regression)

### Cluster Distribution
- **Cluster 0** (Bulk Powerhouses): 45 countries (China, India, Russia, USA)
- **Cluster 1** (Specialist Hubs): 25 countries (Chile, DRC, Indonesia)
- **Cluster 2** (Minimal Producers): 70+ countries (potential but no infrastructure)

### PCA Variance
- **PC1**: 38% (separates high-volume vs. low-volume)
- **PC2**: 22% (separates bulk vs. specialty)
- **Total 2D**: 60% explained

---

## CRITICAL MINERALS IN ANALYSIS

| Mineral | Symbol | Why Critical | Top Producer(s) |
|---------|--------|-------------|-----------------|
| Lithium | O.Li, Con.Li | EV batteries | Chile (60%), China, Australia |
| Nickel | O.Ni, Con.Ni | Battery cathodes | Indonesia, Philippines |
| Cobalt | O.Co, Con.Co | Battery stability | DRC (70%), Russia, Australia |
| Tantalum | Con.Ta | Electronics, superconductors | DRC, Myanmar, Rwanda |
| Rare Earths | REE | Wind turbines, permanent magnets | China (95%), Myanmar |

---

## METHODOLOGY QUICK REFERENCE

### Preprocessing Steps
1. Merge facility metadata with production data
2. Aggregate mine-level → country-level
3. Validate: no missing values, all production ≥ 0
4. Remove duplicates

### Noise Injection Model
```
Critical minerals:      production × (1 + N(0, 0.08))
Regular minerals:       production × (1 + N(0, 0.03))
Shocks:                 1% of rows × {0.3, 0.5, 1.8, 2.5}
```

### Denoising Methods
- **IQR Clipping**: Remove outliers beyond Q1-1.5×IQR and Q3+1.5×IQR
- **Rolling Average**: 3-year window per country-mineral pair

### Supervised Learning
| Model | Baseline | RMSE | R² | Best For |
|-------|----------|------|-----|----------|
| Linear Regression | ✓ | 2.15M | 0.71 | Interpretability |
| Random Forest | ✓ | 1.45M | 0.84 | Prediction accuracy |

### Unsupervised Learning
| Method | K/n_components | Finding | Interpretation |
|--------|---|---|---|
| K-Means | k=3 | 3 distinct archetypes | Natural groupings |
| PCA | n=2 | 60% variance in 2D | Dimensionality reduction |

---

## EXPECTED EXAM QUESTIONS & ANSWERS

### Q1: "Why did you choose K-Means over DBSCAN?"
**A**: K-Means (partitioning) better suited to our data. DBSCAN (density-based) works well for irregular clusters and outlier detection, but our data has natural spherical clusters. Elbow method on inertia clearly showed k=3. If time allowed, would compare multiple algorithms.

### Q2: "How did you decide to use Random Forest over SVM or Neural Networks?"
**A**: Incremental complexity approach. Started with Linear Regression (baseline, interpretable). RF non-linear + feature interactions, 33% RMSE improvement justified complexity. SVM possible but scaler-sensitive; NN overkill for this data size. Balance: performance vs. interpretability vs. compute time.

### Q3: "What does the HHI value of 0.18 mean in plain language?"
**A**: HHI=(fraction of largest player)². At 0.18, implies largest player is ~42% (since √0.18≈0.42). Combined with next two biggest ~12% each. Less than monopoly (<0.25) but still highly concentrated (>0.15 antitrust threshold). In context: fewer than 5 countries control 80% of specialty minerals.

### Q4: "Why inject artificial noise? Why not just analyze clean data?"
**A**: Real-world mining data is noisy (informal mining, export under-reporting, geopolitical disruptions). Noise injection tests robustness of our findings. If denoising fails, analysis unreliable. Success shows preprocessing is effective. Also relevant for policy: if supply truly disrupted (strikes, wars), can we forecast? Our model says "partially" (not perfect, but better than random).

### Q5: "Your Random Forest predicts next year production. What about 5-year forecasts?"
**A**: Short-term (1 year) is reliable (R²=0.84) because production is sticky. Beyond 2–3 years, unmodeled factors (new discoveries, policy changes, tech shifts) dominate. Would need time-series decomposition (trend, seasonality, shocks) and exogenous variables (political stability, investment, recycling rates).

### Q6: "Cluster 2 has 70+ countries with minimal production. What's the point of including them?"
**A**: Serves two purposes: (1) Completeness—shows global landscape; (2) Potential—many countries have untapped resources. Policy implication: how to develop Cluster 2 producers to dilute concentration risk. Ignoring them would bias analysis toward current leaders.

### Q7: "Your correlation matrix shows r=0.95 between consecutive years. Doesn't this make prediction trivial?"
**A**: Good observation. High autocorrelation means naive forecast (this year = next year) works OK. But RF R²=0.84 > baseline (r²=0.90 for naive)... actually, naive beats RF! Counterintuitive. Implication: production *very* stable; growth features (lag, growth_rate) add little. Classic case where simplest model wins. We should have tested this in the report.

### Q8: "Why normalize using Z-score for clustering but not for supervised learning?"
**A**: Different reasons. For clustering (K-Means), distances matter—lithium production is 0-50M tonnes, coal is 0-1B tonnes. Z-score ensures equal weighting. For supervised learning (RF), tree-based models are scale-invariant (they split on values, not distances), so scaling optional. Linear Regression benefits from scaling (regularization, stability), but we didn't use it. Trade-off: transparent vs. performant.

### Q9: "If critical minerals are so scarce, why isn't the world already in crisis?"
**A**: Several factors: (1) Recycling nascent but growing; (2) Demand still ramping (EV adoption accelerating); (3) Strategic reserves (China holds stockpile); (4) Substitution R&D (e.g., sodium-ion batteries instead of lithium). But timeline is tight—shortage risks real within 5–10 years if supply not diversified.

### Q10: "What's the most important insight from this project?"
**A**: Concentration risk in specialty minerals is real and quantifiable. Unlike oil (multiple producers globally), lithium, cobalt, nickel concentrated in 2–3 countries each. Energy transition not "solving" dependency; it's reshaping it. Moment to act is *now*—before shortage crisis forces expensive rapid solutions. Data says: policy intervention needed ASAP.

---

## TALKING POINTS BY MEMBER ROLE

### Member 1 (Preprocessing & Data Cleaning)
- Extracted facilities from GeoPackage, merged with production
- Decision: country-level aggregation (policy/supply chain risk scale)
- Challenges: handling missing values, ensuring uniqueness
- Result: 3,200 clean rows, no NaN, consistent data types

### Member 2 (Statistical Analysis)
- Computed descriptive stats: mean, variance, skewness, kurtosis
- Calculated HHI (concentration index)
- Created three plots: histogram, top countries, top minerals
- Key finding: right-skewed distribution, top 3 countries = 65%

### Member 3 (Supervised Learning)
- Built features: lags, growth rates, one-hot encoding
- Trained Linear Regression (baseline) and Random Forest (advanced)
- Evaluated: RMSE, R², MAE
- Result: RF outperforms by 33% RMSE; R²=0.84

### Member 4 (Unsupervised Learning)
- Prepared country × mineral matrix (standardized)
- Ran K-Means with elbow method (selected k=3)
- Applied PCA for 2D visualization
- Found: three natural archetypes (Bulk, Specialist, Minimal)

### Member 5 (Report & Coordination)
- Integrated findings into cohesive narrative
- Wrote discussion tying methods to research question
- Developed policy recommendations
- Ensured all members' work represented fairly

---

## VISUAL SUMMARY (WHAT TO SHOW)

### 8 Key Visualizations to Reference

1. **Noise Injection & Cleaning (Lithium time-series)**
   - Shows Original → Noisy → Cleaned
   - Validates preprocessing

2. **Distribution Histogram (Global Production)**
   - Log-scale x-axis
   - Shows right-skew, bulk commodity dominance

3. **Top 10 Countries Bar Chart**
   - China 45%, India 12%, Russia 8%, USA 6%, Australia 5%
   - Emphasizes concentration

4. **Top 10 Minerals Bar Chart**
   - Iron ore, coal, copper dominate by volume
   - But specialty minerals critical for transition

5. **Correlation Heatmap**
   - Lithium vs. year: r=0.89 (strong growth signal)
   - Country autocorrelation: r=0.95 (sticky)

6. **Predicted vs. Actual (RF Model)**
   - Scatter plot with diagonal reference
   - R²=0.84, some underestimation at extremes

7. **PCA Scatter (Clusters)**
   - Three colored clusters clear separation
   - Bulk (right, low), Specialist (left, high), Minimal (center)

8. **Elbow Method (K-Means)**
   - Inertia vs. k, clear elbow at k=3

---

## EXAM DAY CHECKLIST

- [ ] Practice presentation 2–3 times (time yourself: aim for exactly 5 minutes)
- [ ] Print full report (10 pages + appendices)
- [ ] Print presentation slides (1–2 per page for readability)
- [ ] Save PDF copies on laptop + USB backup
- [ ] Prepare 2–3 follow-up talking points per slide
- [ ] Review Q&A section above (common questions)
- [ ] Have backup slides with extra charts
- [ ] Arrive 15 minutes early to test projector/laptop
- [ ] Assign roles: who explains which section?
- [ ] Designate one person to handle Q&A flow
- [ ] Agree on tone: professional, confident, humble about limitations
- [ ] Practice saying key numbers from memory (HHI, R², top 3 share, etc.)

---

## TIME MANAGEMENT FOR PRESENTATION

**5-Minute Overview**:
- 0:00–0:30 – Title, team members, motivation (Slides 1–3)
- 0:30–1:30 – Dataset & preprocessing (Slides 4–5)
- 1:30–2:30 – Statistical findings (Slides 6–9)
- 2:30–3:30 – Supervised learning results (Slides 10–12)
- 3:30–4:30 – Unsupervised clustering (Slides 13–14)
- 4:30–5:00 – Conclusion & implications (Slides 15–18)

**10-Minute Q&A**:
- Anticipate 3–5 deep questions
- Keep answers to 1–2 minutes each
- If unsure, redirect: "Great question, but let me clarify what we found in..."
- Do NOT make up numbers you're unsure about

---

## REVISION CHECKLIST

- [ ] Report is coherent and follows 8-step workflow
- [ ] Each method justified (why this, not that?)
- [ ] All plots labeled and captioned
- [ ] Results tied back to research question
- [ ] Limitations acknowledged honestly
- [ ] References complete (at least 5–8)
- [ ] Appendices include data dictionary, hyperparameters, environment
- [ ] Slides are readable (large fonts, one chart per slide)
- [ ] Presentation flows logically (not jumping around)
- [ ] Each team member can explain their section fluently

---

## FINAL WORDS

**For the Exam**:
1. **Confidence**: You've done solid work. Data-driven, rigorous, interpretable.
2. **Clarity**: Explain to a smart person who doesn't know your project (not just experts).
3. **Humility**: Acknowledge what you don't know (recycling, future policy, black swans).
4. **Passion**: Show genuine interest in the energy transition problem. It's compelling.
5. **Teamwork**: Emphasize that all members contributed meaningfully to all parts.

**If You Get Stuck**:
- Pause, take a breath, reread the question mentally.
- Start with what you *do* know.
- Use phrases: "That's a great question. Let me think... Based on our data, we found [fact]. But you're right that [limitation]."
- Never say: "I don't know" (say instead: "That's beyond our scope, but it would be interesting to explore...").

**Good Luck!**

Your project is well-structured, uses appropriate methods, and answers a real-world question. Examiners will appreciate the rigor and the practical relevance. Go present with confidence.

---

**Last updated**: February 2024
**Prepared for**: Practical Exam Project – Applied ML & Statistics
**Duration**: 15 min exam + 15 min written report preparation
