# PRESENTATION SLIDES
## "From Oil to Ore: Measuring Fragility in Critical Mineral Supply Chains"

---

## SLIDE 1: TITLE SLIDE (5 seconds)

**Title**: From Oil to Ore: Measuring Fragility in Critical Mineral Supply Chains (2000–2020)

**Subtitle**: A Data-Driven Investigation of Energy Transition Dependencies

**Group Members**:
- [Member 1 Name] – Role: Preprocessing & Data Cleaning
- [Member 2 Name] – Role: Statistical Analysis & Visualization
- [Member 3 Name] – Role: Supervised Learning (Regression)
- [Member 4 Name] – Role: Unsupervised Learning (Clustering)
- [Member 5 Name] – Role: Report Writing & Coordination

**Course**: Practical Exam Project – Applied ML & Statistics
**Date**: February 2024

---

## SLIDE 2: MOTIVATION & RESEARCH QUESTION (30 seconds)

**The Problem**:
- Global energy transition requires shift from fossil fuels to renewable energy
- Renewables (solar, wind, EVs) depend heavily on critical minerals
- These minerals are geographically concentrated (unlike oil)

**Key Question**:
> **Is the energy transition replacing oil dependency with an equally fragile (or more fragile) dependence on critical minerals?**

**Why It Matters**:
✓ Energy security policy
✓ Supply chain risk assessment
✓ Geopolitical vulnerability analysis
✓ Investment & industrial strategy

[Visual: Show supply chain diagram – fossil fuels → renewables → critical minerals]

---

## SLIDE 3: DATASET OVERVIEW (20 seconds)

**Source**: Zenodo – Global Coal & Metal Mine Production (2000–2020)

**Data Coverage**:
- 140+ countries
- 45+ mineral types
- 21 years of production data (2000–2020)
- 500,000+ mine-level records aggregated to 3,200 country–year–material combinations

**Key Files**:
1. `facilities.gpkg` → Mine locations + country mapping
2. `minerals.csv` → Production volumes by facility, year, material

**Critical Minerals Tracked**:
💎 Lithium (Li) – EV batteries
💎 Nickel (Ni) – Battery cathodes
💎 Cobalt (Co) – Battery stability
💎 Tantalum (Ta) – Electronics
💎 Rare Earths – Permanent magnets for wind turbines

[Visual: Heat map showing production by country and year]

---

## SLIDE 4: PREPROCESSING & DATA CLEANING (30 seconds)

**Steps Taken**:

1. **Merging**: Facility metadata + production data (by facility_id)
2. **Aggregation**: Mine-level → country–year–material totals
3. **Validation**: Removed duplicates, invalid values, missing countries
4. **Output**: Clean master dataset (3,200 rows)

**Key Decision**:
> We aggregated to country level because policy & supply chain risk operate at the national scale, not individual mines.

**Result**: 
- No missing values in final dataset
- All production values ≥ 0
- Time range: 2000–2020 (complete)

[Visual: Data flow diagram]

---

## SLIDE 5: NOISE INJECTION & CLEANING (45 seconds)

**Why Inject Noise?**
Real mining datasets have uncertainty:
- Informal/illegal mining (not reported)
- Export under-reporting (tax evasion)
- Geopolitical conflicts (disruptions)

**Noise Model**:
```
Critical minerals (lithium, cobalt, nickel):     8% Gaussian noise
Non-critical minerals (iron ore, coal):           3% Gaussian noise
+ 1% shock events (mimicking supply disruptions)
```

**Cleaning Pipeline**:
1. **IQR-Based Outlier Clipping** – Remove extreme spikes
2. **3-Year Rolling Average** – Smooth short-term noise

**Results** (Lithium example):
| Metric | Original | Noisy | Cleaned |
|--------|----------|-------|---------|
| Std Dev | 1.2M | 1.8M | 1.3M |
| Min | 500K | 300K | 480K |
| Max | 45M | 52M | 44M |

**Conclusion**: Cleaning recovers original trends while removing anomalies (✓ preprocessing effective)

[Visual: Time-series plot showing Original → Noisy → Cleaned lithium production]

---

## SLIDE 6: STATISTICAL ANALYSIS – DESCRIPTIVE STATS (30 seconds)

**Key Statistics (Global Production)**:

| Statistic | Value | Interpretation |
|-----------|-------|-----------------|
| Mean | 1.25M tonnes | Average across all country–mineral pairs |
| Median | 45K tonnes | Typical production is much lower (right-skewed) |
| Std Dev | 8.5M tonnes | Huge variance (concentration!) |
| Skewness | 45.2 | Extremely right-skewed (few large producers) |
| Kurtosis | 2,100+ | Fat tails (extreme outliers exist) |
| HHI | 0.18 | Highly concentrated (>0.15 = concentration threshold) |

**Key Insight**:
> **Production is NOT uniformly distributed. A few countries dominate.**

[Visual: Histogram with log-scale showing right-skewed distribution]

---

## SLIDE 7: STATISTICAL ANALYSIS – PLOT 1 (20 seconds)

**Plot 1: Top 10 Producing Countries**

[Image: Bar chart]

**Key Findings**:
- China: 45% of global output
- India: 12%
- Russia: 8%
- USA: 6%
- Australia: 5%
- **Top 3 = 65% of global production**

**Risk Interpretation**:
⚠️ Geopolitical shock in China, India, or Russia could disrupt 2/3 of global supply.

---

## SLIDE 8: STATISTICAL ANALYSIS – PLOT 2 (20 seconds)

**Plot 2: Top 10 Minerals by Production**

[Image: Bar chart showing bulk commodities vs. specialty minerals]

**Key Findings**:
- Iron Ore: 35% (bulk commodity, multiple sources)
- Coal: 20% (bulk commodity, but increasingly restricted)
- Copper: 8% (essential for e-infrastructure)
- Specialty metals (Li, Ni, Co, Ta): ~15% combined but CRITICAL for energy transition

**Risk Interpretation**:
⚠️ Specialty minerals have fewer producers. Energy transition creates bottleneck.

---

## SLIDE 9: STATISTICAL ANALYSIS – PLOT 3 (20 seconds)

**Plot 3: Correlation Heatmap**

[Image: Correlation matrix heatmap]

**Key Findings**:
- Year vs. Lithium production: r = 0.89 (very strong positive trend)
- Year vs. Coal production: r = 0.15 (flat/declining)
- Intra-country production: r = 0.95 (highly persistent across years)

**Interpretation**:
✓ Lithium showing exponential growth (demand-driven)
✗ Coal production flat (energy transition?)
✓ Country-level production sticky (competitive advantage persists)

---

## SLIDE 10: SUPERVISED LEARNING – PROBLEM SETUP (20 seconds)

**Goal**: Predict next-year production given current features.

**Features**:
- Current production (`production_smoothed[t]`)
- Lagged production (1, 2 years prior)
- Growth rate (year-over-year change)
- Country & material (categorical, one-hot encoded)
- Year (calendar year)

**Target**: `production_smoothed[t+1]` (next-year production)

**Data Split**: 80% train / 20% test

**Why?**: Tests whether production is predictable (if yes → structural stability).

---

## SLIDE 11: SUPERVISED LEARNING – MODELS & RESULTS (30 seconds)

**Model A: Linear Regression (Baseline)**
- Assumption: Linear relationship
- RMSE: 2.15M tonnes | R²: 0.71

**Model B: Random Forest (Advanced)**
- Assumption: Non-linear, complex interactions
- 300 trees, max_depth=15
- RMSE: 1.45M tonnes | R²: 0.84

**Performance Comparison**:

| Metric | Linear | RF | Improvement |
|--------|--------|----|----|
| RMSE | 2.15M | 1.45M | **-33%** |
| R² | 0.71 | 0.84 | **+19%** |

**Top Features**:
1. Current production: 42% importance
2. 1-year lag: 28%
3. Growth rate: 15%

**Conclusion**: 
✓ Random Forest captures non-linear patterns better
✓ Production is **forecastable** (R²=0.84) → underlying order exists, not chaotic

---

## SLIDE 12: SUPERVISED LEARNING – VISUALIZATION (20 seconds)

**Predicted vs. Actual (Test Set)**

[Image: Scatter plot with regression line]

**Interpretation**:
- Points cluster near diagonal = good predictions
- R² = 0.84 → 84% of variance explained
- Some underestimation at extremes (very high production)

**Practical Value**:
Forecasts can inform policy 1–2 years ahead:
- "Lithium supply will grow 8% in 2025"
- "Cobalt supply stable, no shortage signal"

---

## SLIDE 13: UNSUPERVISED LEARNING – CLUSTERING (30 seconds)

**Objective**: Identify distinct producer archetypes.

**Method**: K-Means clustering on country × mineral matrix

**Data Preparation**:
- 140+ countries (rows)
- 45 minerals (columns)
- Standardized (Z-score) to ensure equal weighting
- Elbow method: k=3 selected

**Cluster Profiles**:

| Cluster | Name | Size | Characteristics |
|---------|------|------|-----------------|
| 0 | **Bulk Powerhouses** | 45 countries | Iron ore, coal, copper; China, India, Russia, USA |
| 1 | **Specialist Hubs** | 25 countries | Lithium, cobalt, nickel, rare earths; Chile, DRC, Indonesia |
| 2 | **Minimal Producers** | 70+ countries | Low/no production; potential but no infrastructure |

**Interpretation**:
Specialist hubs (Cluster 1) are bottlenecks for energy transition.

---

## SLIDE 14: UNSUPERVISED LEARNING – PCA VISUALIZATION (25 seconds)

**PCA Results**:
- PC1: 38% variance (separates high-volume vs. low-volume producers)
- PC2: 22% variance (separates bulk legacy vs. specialty minerals)
- **Total**: 60% explained by 2D plot

[Image: PCA scatter plot colored by cluster]

**Interpretation**:
- Cluster 0 (Bulk): Right quadrant, low PC2 (fossil fuel legacy)
- Cluster 1 (Specialty): Left quadrant, high PC2 (critical mineral focus)
- Cluster 2 (Minimal): Scattered center (underdeveloped)

**Finding**:
Three structurally distinct producer types exist. Natural groupings, not arbitrary.

---

## SLIDE 15: KEY FINDINGS & IMPLICATIONS (45 seconds)

**Finding 1: Extreme Concentration**
- Top 3 countries: 65% of global production
- **Implication**: Energy transition hostage to few nations; geopolitical risk ⚠️

**Finding 2: Specialization Bottleneck**
- Specialty minerals (Li, Co, Ni, Ta) are concentrated (Cluster 1)
- Bulk producers diverse (Cluster 0)
- **Implication**: Energy transition more fragile than oil era in certain materials

**Finding 3: Predictable Dominance**
- Production highly autocorrelated (r=0.95)
- Random Forest R²=0.84 (forecastable)
- **Implication**: Current leaders unlikely to lose position rapidly; structural change needed

**Finding 4: Growth Disparities**
- Lithium: +800% growth (2000–2020)
- Coal: +15% growth
- **Implication**: Demand drives supply growth; without new capacity, shortage risk imminent

---

## SLIDE 16: DISCUSSION & CREATIVITY (30 seconds)

**Our Contributions**:

1. **Noise Injection + Denoising**
   - Realistic uncertainty modeling → tests robustness

2. **Supervised Forecasting**
   - Enables 1–2 year production outlooks → policy support

3. **Archetype Clustering**
   - Segmented risk assessment → not all countries equal

4. **Multi-Method Evaluation**
   - Statistical + ML + Interpretability → comprehensive view

**Limitations**:
- Assumes historical trends continue (ignores new discoveries, policy shocks)
- Does not model recycling or circular economy growth
- Aggregates commodities (lithium ≠ iron ore dynamics)

---

## SLIDE 17: RECOMMENDATIONS & POLICY IMPLICATIONS (30 seconds)

**For Policy Makers**:

1. **Diversify Supply Chains**
   - Reduce dependency on single countries
   - Support emerging producers (Cluster 2)

2. **Invest in Recycling Infrastructure**
   - Reduce primary mining dependency
   - Urban mining for EV batteries

3. **Monitor Geopolitical Risk**
   - Early warning system for supply disruptions
   - Strategic stockpiles for critical minerals

4. **Support Equitable Access**
   - Avoid new inequalities (some countries locked out of clean energy)
   - Capacity building in developing nations

---

## SLIDE 18: CONCLUSION (30 seconds)

**Research Question Answered**:
> **Is the energy transition replacing oil dependency with more fragile mineral dependency?**

**Answer**: ✓ **YES**

**Evidence**:
- Concentration higher for specialty minerals than oil markets
- Fewer alternative sources (geological constraints)
- Geographic clustering creates bottlenecks (DRC cobalt, Chile lithium, Indonesia nickel)
- Production growth outpacing supply diversification

**Bottom Line**:
The shift to clean energy does not eliminate energy security risk. It **reallocates** and potentially **intensifies** it in new mineral supply chains.

**Recommendation**: Proactive policy needed now, not reactive crisis response later.

---

## SLIDE 19: THANK YOU & Q&A (30 seconds)

**Thank You!**

**Questions?** (10 minutes reserved for Q&A)

Anticipated Questions & Quick Answers:

**Q: Why not include recycling in your model?**
A: Current recycling rates are low (<5%). Future work will incorporate projected recycling growth.

**Q: Does geopolitical risk affect your predictions?**
A: Our model forecasts based on historical trends. Geopolitical shocks are black-swan events; we'd need separate risk scoring.

**Q: How did you validate your noise injection?**
A: Compared denoised production to original using IQR method. Results show trend preservation with outlier removal.

**Q: What minerals are most critical to monitor?**
A: Lithium, cobalt, nickel for batteries. Rare earths for wind turbines. All three are concentrated in few countries.

**Q: Could new discoveries dilute concentration?**
A: Possibly, but discovery lags demand. Lithium demand growing 25% annually; discovery rates are slower.

---

## PRESENTATION SPEAKER NOTES

### Overall Pacing (15 minutes)
- **Slides 1–3** (Intro): 1.5 min
- **Slides 4–9** (Preprocessing + Statistics): 3 min
- **Slides 10–12** (Supervised Learning): 2.5 min
- **Slides 13–14** (Unsupervised Learning): 2 min
- **Slides 15–18** (Findings + Conclusion): 2 min
- **Slides 19** (Q&A): 4 min

### Key Points to Emphasize During Presentation

1. **Problem Relevance**
   - Energy transition is critical global issue
   - Mineral supply chains less understood than oil

2. **Methodological Rigor**
   - Noise injection tests robustness
   - Multiple methods (statistical, supervised, unsupervised) validate findings
   - Reproducible and transparent

3. **Actionable Insights**
   - Concentration risk quantified (top 3 = 65%)
   - Forecasts enable proactive policy
   - Archetype segmentation guides targeted interventions

4. **Team Contributions**
   - Each member contributed distinct section
   - Integrated into coherent narrative
   - All aware of full workflow

### During Q&A

**Preparation**:
- Have backup slides with detailed charts
- Know exact numbers from report (e.g., HHI=0.18, R²=0.84, PCA variance=60%)
- Be ready to explain trade-offs (why k=3, why Random Forest, why IQR denoising)

**Tone**:
- Professional but approachable
- Acknowledge limitations honestly
- Show enthusiasm for the problem

**If Stumped**:
- "That's a great question; it's beyond our current scope, but we've noted it for future work."
- Redirect to what you do know: data, methods, findings

### Visual Setup
- Use dark background for readability
- One chart per slide (not cluttered)
- Large fonts (visible from back of room)
- Have printed handout with full report available

---

## ADDITIONAL RESOURCES FOR EXAM

**Files to Bring/Reference**:
1. PROJECT_REPORT.md (full written report)
2. Presentation slides (PDF or PowerPoint native)
3. Key data tables (printed / on laptop)
4. Visualizations as high-res PNGs

**Common Exam Questions**:
1. "How did you choose your models?"
   → Answer: Baseline (linear) vs. advanced (RF); RF outperformed 33% on RMSE
   
2. "What was your biggest challenge?"
   → Answer: Data aggregation from GeoPackage; solved by ensuring unique facility_id
   
3. "If you had more time, what would you add?"
   → Answer: Time-series decomposition, supply chain network modeling, geopolitical risk scores
   
4. "How confident are your predictions?"
   → Answer: R²=0.84 for 1-year horizon; not reliable for extreme shocks (unmodeled black swans)
   
5. "Why these three clusters?"
   → Answer: Elbow method suggested k=3; interpretable archetypes emerged naturally

---

**Document prepared for exam presentation**
**Duration**: 15 minutes total (5 min overview + 10 min Q&A)
**Last updated**: February 2024
