# PROJECT SUBMISSION PACKAGE
## "From Oil to Ore: Measuring Fragility in Critical Mineral Supply Chains"

---

## WHAT'S INCLUDED IN THIS PACKAGE

This folder contains all materials needed for your **Practical Exam Project – Applied Machine Learning & Statistics**:

### Core Deliverables (REQUIRED)

1. **PROJECT_REPORT.md** ✓
   - 10-page written report matching practical exam requirements
   - Sections: Title, Dataset, Preprocessing, Noise Handling, Statistical Analysis, Supervised Learning, Unsupervised Learning, Discussion
   - Includes: Tables, methodology justification, findings, limitations
   - **Status**: Ready to submit (convert to .docx or .pdf as needed)

2. **PRESENTATION_SLIDES.md** ✓
   - 19 slides covering full project
   - Structured for 5-minute overview + 10-minute Q&A format
   - Speaker notes included
   - Pacing guide (timings per slide)
   - **Status**: Ready to present (convert to PowerPoint format)

3. **EXAM_STUDY_GUIDE.md** ✓
   - Quick reference for team members
   - 10 expected exam questions with answers
   - Talking points per team role
   - Time management guide
   - Exam day checklist
   - **Status**: Study material for all team members

4. **so_k-means_model.ipynb** ✓
   - Complete Jupyter notebook with all analyses
   - Code cells demonstrate:
     - Data preprocessing & loading
     - Noise injection & cleaning
     - Statistical analysis (5 plots)
     - Supervised learning (2 models)
     - Unsupervised learning (K-Means + PCA)
   - Output files generated:
     - CSV files with predictions
     - PNG files with visualizations
   - **Status**: Executable, all cells tested

---

## HOW TO USE THESE MATERIALS

### For Written Report Submission (Due in 5 days)

**Step 1**: Open `PROJECT_REPORT.md`
- Copy content to Word or Google Docs
- Insert header/footer with group names
- Upload visualizations as embedded images (where indicated)
- Export as .pdf (max 10 pages, excluding appendices)

**Step 2**: Add appendices (not counted toward page limit)
- Data dictionary
- Hyperparameters
- Computational environment

**Step 3**: Submit through course portal

### For In-Class Exam Presentation (15 minutes)

**Step 1**: Prepare with `PRESENTATION_SLIDES.md`
- Convert to PowerPoint (.pptx):
  - 1 slide per concept
  - Use suggested visual descriptions to source/place actual charts
  - Keep fonts large (Calibri 28pt minimum)
  - Dark background for contrast

**Step 2**: Practice with <code>EXAM_STUDY_GUIDE.md</code>
- Each team member reviews their role's talking points
- Practice transitions between presenters
- Do full 15-min run-through 2–3 times
- Time yourselves strictly

**Step 3**: Prepare for Q&A
- Read through "Expected Exam Questions" in study guide
- Designate someone to manage Q&A flow
- Have follow-up slides ready (detailed charts)

**Step 4**: Exam day
- Arrive 15 min early for AV setup
- Test projector + presenter laptop
- Have printed report copies as handouts
- Introduce team members and their roles

---

## KEY NUMBERS TO MEMORIZE (FOR Q&A)

| Fact | Number | Context |
|------|--------|---------|
| Dataset time span | 2000–2020 | 21 years |
| Number of countries | 140+ | Global coverage |
| Clean dataset size | 3,200 rows | After aggregation |
| Concentration (HHI) | 0.18 | >0.15 = highly concentrated |
| Top 3 countries share | 65% | of global production |
| Lithium growth | +800% | 2000–2020 |
| Random Forest R² | 0.84 | Supervised learning |
| RMSE improvement | 33% | RF vs. Linear Regression |
| PCA variance (2D) | 60% | Dimensionality reduction |
| K-Means clusters | 3 | Elbow method result |

---

## FILE OUTPUTS FROM NOTEBOOK

The `so_k-means_model.ipynb` notebook generates:

### CSV Files (Data)
- `unsupervised_models_evaluation.csv` – Clustering metrics
- `supervised_models_evaluation.csv` – Regression metrics
- `cross_validation_results.csv` – CV scores
- `random_forest_predictions.csv` – Test set predictions

### PNG Files (Visualizations)
- `unsupervised_silhouette_comparison.png` – Clustering quality
- `unsupervised_metrics_comparison.png` – K-Means vs. GMM vs. Hierarchical
- `unsupervised_pca_comparison.png` – 2D PCA clusters
- `supervised_confusion_matrices.png` – Model evaluation
- `supervised_metrics_comparison.png` – Accuracy, F1, Precision, Recall
- `supervised_radar_comparison.png` – Top 5 models
- `feature_importance_comparison.png` – Tree-based feature rankings
- `roc_curves_comparison.png` – ROC curves by model
- `cross_validation_analysis.png` – CV stability
- Plus all original plots (histograms, boxplots, correlations)

**Tip**: Use these PNG files directly in your PowerPoint presentation for visual evidence.

---

## TEAM ROLE ASSIGNMENTS (SUGGESTED)

### Member 1: PREPROCESSING & DATA CLEANING
- Owns: Dataset loading, merging, aggregation
- Can explain: Data structure, why country-level aggregation, quality validation
- Presents: Slides 4–5, part of Slide 19 Q&A

### Member 2: STATISTICAL ANALYSIS
- Owns: Descriptive statistics, plots, correlation analysis
- Can explain: HHI calculation, skewness meaning, plot interpretation
- Presents: Slides 6–9, part of Slide 19 Q&A

### Member 3: SUPERVISED LEARNING
- Owns: Feature engineering, model training, evaluation
- Can explain: Linear vs. Random Forest, hyperparameter choices, RMSE/R²
- Presents: Slides 10–12, part of Slide 19 Q&A

### Member 4: UNSUPERVISED LEARNING
- Owns: Clustering, PCA, dimensionality reduction
- Can explain: Elbow method, K-Means algorithm, PCA interpretation
- Presents: Slides 13–14, part of Slide 19 Q&A

### Member 5: COORDINATION & DISCUSSION
- Owns: Report writing, tying findings together, policy implications
- Can explain: Research question, methodology justification, conclusions
- Presents: Slides 1–3, 15–18, manages Q&A session

**Flexibility**: All members should be able to answer basic questions about any section. Specialization helps with depth, not exclusivity.

---

## WORKFLOW CHECKLIST

### Before Exam (1–2 days)

- [ ] **Report is finalized**
  - [ ] All sections complete (8 sections per template)
  - [ ] References formatted
  - [ ] Appendices included
  - [ ] Spell-checked, grammar reviewed
  - [ ] Page count confirmed (≤10 pages main text)

- [ ] **Presentation is prepared**
  - [ ] 19 slides created in PowerPoint (.pptx)
  - [ ] All visualizations embedded
  - [ ] Fonts readable (28pt minimum)
  - [ ] Animations minimal (no distracting effects)
  - [ ] Backup slides with detailed charts ready

- [ ] **Team is prepared**
  - [ ] Each member knows their section
  - [ ] Transitions between speakers smooth
  - [ ] Full 15-min run-through completed 2+ times
  - [ ] Q&A strategy discussed (who answers what type of question)
  - [ ] Talking points memorized (not reading from slides)

- [ ] **Materials printed/backed up**
  - [ ] Report printed (3 copies for handouts)
  - [ ] Presentation saved as .pptx on laptop
  - [ ] Backup on USB drive
  - [ ] PDF copies of all materials (in case of corruption)

### Day of Exam (15 minutes scheduled)

- [ ] **Arrive early** (15 minutes before scheduled time)
  - [ ] Test laptop with projector
  - [ ] Load presentation (verify all slides visible)
  - [ ] Test audio/video if using (unlikely)
  - [ ] Have printer test slide ready

- [ ] **Introduction** (0:00–0:30)
  - [ ] State group members and roles clearly
  - [ ] Brief motivation for project

- [ ] **Overview presentation** (0:30–5:00)
  - [ ] Follow 5-minute pacing guide from study guide
  - [ ] Speak clearly, maintain eye contact
  - [ ] Avoid reading directly from slides
  - [ ] Highlight 2–3 key findings

- [ ] **Q&A session** (5:00–15:00, 10 minutes)
  - [ ] Listen carefully to each question
  - [ ] Pause before answering (not rushed)
  - [ ] Answer directly, not evasively
  - [ ] If unsure, redirect to what you *do* know
  - [ ] Examiners appreciate honest "we didn't model that" over made-up answers

---

## COMMON MISTAKES TO AVOID

❌ **In Report**:
- Too long (> 10 pages main text). Trim ruthlessly.
- Insufficient justification ("We chose RF because it's popular"). Explain trade-offs.
- No visualization for each section. Visualizations = proof.
- Vague conclusions ("More work needed"). Be specific ("3 concrete extensions...").

❌ **In Presentation**:
- Reading directly from slides. Practice fluency.
- Too many bullet points per slide (>5 per slide). Use one visual per slide.
- No speaker notes. Practice transitions beforehand.
- Forgetting to introduce team roles. Examiners need to know who did what.

❌ **In Q&A**:
- Saying "I don't know" flatly. Say "That's beyond our scope, but..."
- Making up numbers. If unsure, admit it: "I recall it was around X, but I'd verify..."
- Defensive tone. Examiners are curious, not attacking. Stay collaborative.
- Long-winded answers (>2 min per Q). Be concise.

---

## BACKUP PLAN (IF THINGS GO WRONG)

**Laptop fails**:
- Have USB with .pptx backup
- Have printed slides (A3, 4 per page)
- Can present from paper if needed
- PDF on phone as last resort

**Projector unavailable**:
- Use large printed posters/charts
- Discuss findings directly without slides
- Examiners care about content & understanding, not fancy visuals

**Forgot to run notebook**:
- Key CSV/PNG files already generated (save them!)
- Can discuss results from memory (you've practiced)
- Worst case: show code on screen, explain what outputs would be

**Someone gets sick**:
- Any team member can cover another's section (you've all learned it all)
- Redistribute Q&A assignments
- Inform instructor before exam starts

---

## FINAL CHECKLIST (24 HOURS BEFORE EXAM)

✅ **Hard copies**:
- [ ] Report printed (3 copies, bound or clipped)
- [ ] Presentation slides printed (4 per page, 1 copy per team member)
- [ ] Study guide printed (for reference during Q&A prep)

✅ **Digital backups**:
- [ ] Presentation .pptx on laptop
- [ ] Presentation .pptx on USB
- [ ] Report .pdf on laptop
- [ ] All CSV/PNG outputs saved locally
- [ ] Notebook .ipynb with all cells executable

✅ **Team prep**:
- [ ] All members have read report fully
- [ ] All members familiar with all sections (not just theirs)
- [ ] Presentation practiced 2–3 times, timed to 5 min
- [ ] Q&A strategy finalized (who handles which questions)
- [ ] Group has met at least once to sync

✅ **Logistics**:
- [ ] Scheduled room/time confirmed
- [ ] Know how to get to exam location
- [ ] Plan arrival 20 min early
- [ ] Know instructor's name and contact info (in case rescheduling)

---

## CONTACT & SUPPORT

**If technical issues arise**:
- Python/Jupyter: Recommend rerunning all cells from scratch
- PowerPoint: Save as .pdf as backup
- Data files: Ensure all CSVs in working directory

**If content questions arise**:
- Review relevant sections of PROJECT_REPORT.md
- Check EXAM_STUDY_GUIDE.md for expected questions
- Consult original notebook (so_k-means_model.ipynb) for method details

**If timing issues arise**:
- Cut slides if needed (prioritize: findings > methods > background)
- Practice condensed 3-min version as backup
- Examiners often extend if discussion is rich

---

## POST-EXAM REFLECTION (For Improvement)

After exam, complete brief reflection:

**What went well**:
- Which slides resonated with examiners (based on questions)?
- Which team member's explanation was clearest?
- What data point/finding surprised them most?

**What could be better**:
- Did any section feel rushed? Could it be tightened?
- Were there questions you couldn't answer? (For next project)
- Was the 5-min time achievable, or too tight?

**For future projects**:
- Start earlier (began at 11th hour? Start at week 1)
- Practice presentation more (did 2 run-throughs? Do 5–10)
- Get feedback from peers/mentor before final (improves quality)

---

## DOCUMENT MANIFEST

**This folder contains**:

| File | Type | Purpose |
|------|------|---------|
| PROJECT_REPORT.md | Markdown | Full written report (convert to .docx/.pdf) |
| PRESENTATION_SLIDES.md | Markdown | Slide outline + speaker notes |
| EXAM_STUDY_GUIDE.md | Markdown | Q&A prep + talking points |
| PROJECT_SUBMISSION_PACKAGE.md | Markdown | This file (orientation guide) |
| so_k-means_model.ipynb | Jupyter | Executable code with all analyses |
| *.csv | Data | Model outputs & predictions |
| *.png | Images | Visualizations & plots |

**Total estimated size**: ~50 MB (mostly PNG visualizations)

---

## FINAL THOUGHTS

You have a **compelling project** with:
- Clear research question (energy transition dependencies)
- Rigorous methodology (stats + 2 ML approaches)
- Real-world implications (policy-relevant findings)
- Well-documented work (code + report + presentation)

**Examiners will be looking for**:
1. **Understanding**: Can you explain *why* you made each choice?
2. **Rigor**: Are methods appropriate for the problem?
3. **Communication**: Can you translate analysis into plain English?
4. **Awareness**: Do you know limitations? Honest about what you don't know?

**You've got this.** Trust your preparation, speak clearly, and let your data tell its story.

---

**Project prepared for**: Practical Exam Project – Applied Machine Learning & Statistics  
**Submission deadline**: 5 days after exam  
**Presentation time**: 15 minutes (5 min overview + 10 min Q&A)  
**Report length**: Max 10 pages (excluding appendices)  
**Good luck!**
