# Success Academies – Market Analysis Strategy Notes (Aligned to Case Prompt)

These notes are written so you can talk through your workbook and notebook in the interview, explicitly mapped to the Success Academies case prompt:

1. Overall Market
2. Projections
3. Data Visualization / Dashboard

Everything below is simple enough to explain line‑by‑line, but still looks strategic and forward‑looking.

---
## 1) Overall Market – What I See and What I’d Add

### 1.1 What I notice in the 5‑year enrollment data

When you walk through the workbook, you can frame the story like this:

- **City‑wide trend (all schools):**
  - Look at total enrollment by year (summing `Total Enrollment`). This gives a quick view of whether NYC K–12 demand is broadly flat, growing, or declining over the 5‑year period.
  - Call out any obvious inflection around the pandemic years (e.g., 2020–2021) and whether the last year or two show recovery or continued softness.

- **By borough:**
  - Compare total enrollment by borough over time. This highlights where the **underlying student base is shifting** (e.g., stronger growth in the Bronx or Queens vs. declines in Manhattan or Staten Island).
  - This directly supports a narrative around **where the market is structurally growing vs. shrinking.**

- **Charter vs. non‑charter:**
  - Using the charter flag and school names, you can segment Success Academies vs. other schools.
  - This allows you to comment on **share of enrollment** in key areas (e.g., “In these zips, Success Academies accounts for roughly X% of enrollment and the share is rising/flat.”)

- **School‑level patterns:**
  - Identify schools with consistent year‑over‑year growth vs. those that are flat or declining.
  - This gives you examples to discuss **micro‑markets** that are clearly healthy versus ones that might be saturated or less attractive.

You can keep the language high‑level in the meeting (e.g., “Overall, I see modest growth city‑wide, with stronger pockets in boroughs A and B, and clear differences at the school level in terms of trajectory.”)

### 1.2 Additional attributes that make the market view more useful

The raw workbook is enrollment‑only. For actual siting and growth decisions, you want a **richer market view**. In your code and enrichment steps you effectively add:

- **School‑age population by ZIP (ACS):**
  - `School_Age_Pop_2019–2023` by ZIP gives a view of the **total addressable market** around each school, not just current enrollment.
  - This lets you define **Market_Momentum** as % change in school‑age population (2019→2023).

- **Economic Need:**
  - `Economic Need Index` summarises socioeconomic conditions. Higher values may indicate **greater need and impact potential**, but also potential constraints (e.g., resource needs, family mobility).

- **Housing pipeline (future supply):**
  - `Planned_Housing_Units` from DOB NOW acts as a proxy for **where future families will live**.
  - This is the core of your “future supply” axis.

- **Competitor density:**
  - `Private_School_Count` per ZIP captures **non‑public competitor concentration**.
  - High counts suggest more **fragmented demand** and more options for families; low counts suggest more white space.

- **Location (lat/lon, zip):**
  - School coordinates allow for **maps, drive‑time thinking, and spatial clustering** (e.g., are we over‑ or under‑represented in certain corridors?).

If given more time, you could also propose:

- **Travel time / transit access** from target neighborhoods.
- **Building/facility constraints** (vacancy, lease expirations, facility quality).
- **Birth and early‑childhood cohorts** to anticipate K entry volumes.

You can frame this as: “The workbook is a good starting point, but to really understand ‘market’, I enrich it with demographics, housing pipeline, and competitor density so we’re not just looking in the rear‑view mirror.”

---
## 2) Projections – Rough 5‑Year Outlook for Success Academy

This section answers: “How would you project enrollment for Success Academy charter schools over the next five years, using a method you can fully explain?”

### 2.1 Forecasting method: 3‑year average growth in school‑age population

Instead of a regression over the full 2018–2023 period (which spans pandemic disruption), you use a **3‑year average growth rate** based on 2021, 2022, and 2023 school‑age population in each ZIP.

**Logic:**

1. Focus on the **last 3 years** of school‑age population: 2021, 2022, 2023.
2. Compute **year‑over‑year growth rates**:
   - g1 = (Pop_2022 − Pop_2021) / Pop_2021
   - g2 = (Pop_2023 − Pop_2022) / Pop_2022
3. Take the **average annual growth rate**:
   - avg_growth = (g1 + g2) / 2
4. Use **Pop_2023 as the starting point**, and roll forward 5 years by applying the same percentage change each year (compound growth):
   - Proj_2024 = Pop_2023 × (1 + avg_growth)
   - Proj_2025 = Proj_2024 × (1 + avg_growth)
   - … up to Proj_2028.
5. **Safeguard:** if any of Pop_2021, Pop_2022, Pop_2023 is missing or non‑positive, fall back to a **flat forecast** at Pop_2023.

**Why this is defensible in an interview:**

- **Pandemic‑aware:** Uses the post‑shock period (2021–2023) rather than mixing pre‑ and mid‑pandemic years into a single line.
- **Simple math only:** Growth rates, averages, and compounding – no black‑box model.
- **Stable but responsive:** It smooths out a single noisy year but still reacts to the most recent trend.

> “I didn’t want to fit a regression across the pandemic years. Instead, I built a very transparent 3‑year growth model based on 2021–2023 school‑age population, then compounded that forward for five years. If the data are unstable or missing, I default to a flat projection.”

### 2.2 Translating market projections into Success Academy enrollment

The prompt is specifically about **Success Academy** enrollment, not just market size. Your simple, explainable approach:

1. **Estimate a capture rate for Success Academy** in each relevant ZIP:
   - capture_rate_zip = Success_Academy_Enrollment_2023 (in that ZIP or catchment) ÷ School_Age_Pop_2023.
2. **Assume a stable or slightly improving capture rate** over the next five years:
   - In “Prime Expansion” or “Protect & Deepen” zips, you might assume capture improves modestly.
   - In “Maintain / Deprioritize” zips, you might hold the capture rate flat or even haircut it.
3. **Apply capture rates to the projected school‑age population:**
   - SA_Proj_Enroll_2024 = capture_rate_zip × Proj_Pop_2024.
   - … similarly for 2025–2028.

This yields a **rough but attributable** forecast of Success Academy enrollment:
- Every number can be traced back to: market size × capture assumption.
- You can easily walk a stakeholder through the inputs and levers (growth rates, capture %).

### 2.3 Additional data sources you would want with more time

If you had more time and data access, you could refine the projection by incorporating:

- **Applicant and offer funnel data** (applications, offers, acceptances, yield by grade and site).
- **Grade‑level cohort progression** (retention/attrition from K→1, 1→2, etc.).
- **Waitlist depth** as a leading indicator of unmet demand.
- **Program changes or new campus openings/closures** already planned internally.
- **More granular housing and migration data** (e.g., building‑level or tract‑level moves, not just ZIP).

In the interview, you can phrase it as: “Given the constraints of the case, I use a clean 3‑year market growth model plus capture rates. In a real project, I’d bring in applicant funnel data, cohort retention, and internal seat plans to tighten those projections.”

---
## 3) Data Visualization – Dashboard Requirements and Design

This section addresses: “If you were to visualize key insights via Looker or a similar tool, what would the dashboard need to do?”

### 3.1 Users and primary questions

**Primary users:**

- **Central growth / strategy team:** Where should we open, expand, or consolidate over the next 3–5 years?
- **Regional / network leaders:** How is my region performing relative to market? Where are my biggest opportunities and risks?
- **Senior leadership (C‑level / Board):** High‑level view of **where growth is coming from** and whether current plans align with that.

**Core questions the dashboard should answer:**

1. Where is the **school‑age population growing or shrinking** over time?
2. Where is **Success Academy already strong** (high capture, good growth)?
3. Where does the **housing pipeline** suggest future demand that we are not yet serving?
4. How does **competitor density** interact with our current and projected presence?
5. Which zips fall into each **strategic quadrant** (Prime Expansion, Protect & Deepen, Emerging Bets, Maintain / Deprioritize)?

### 3.2 Key metrics and views

You can propose the dashboard as a set of linked tiles / tabs:

- **Market Overview (City / Borough):**
  - Total enrollment by year and borough.
  - School‑age population trends by ZIP.
  - Average Economic Need Index by borough.

- **Market Viability Matrix:**
  - Scatter plot of Market_Momentum (x‑axis) vs. Planned_Housing_Units (y‑axis).
  - Points colored by `Strategic_Quadrant`.
  - Point size representing projected school‑age population (e.g., Proj_Pop_2024).

- **Success Academy Footprint:**
  - Map of NYC with each SA school as a marker.
  - Marker size = current enrollment; color = growth trajectory or quadrant of its ZIP.
  - Optional overlay of housing pipeline intensity.

- **Ranked Tables / Drill‑downs:**
  - Zips ranked by Market_Momentum, Planned_Housing_Units, Economic Need, SA capture rate.
  - Ability to click a row and see a mini‑profile: historical enrollments, projections, competitor count, quadrant.

### 3.3 Filters, interactions, and UX considerations

- **Filters:** borough, ZIP, school network (Success Academy vs. others), quadrant, year.
- **Interactivity:**
  - Clicking a point on the scatter or a zip on the map opens its detail view.
  - Tooltips show key metrics (momentum, housing units, SA enrollment, capture rate, Economic Need Index).
- **UX principles:**
  - Use consistent color coding for quadrants across all charts.
  - Keep each view focused on a small set of metrics (no clutter, no dense tables on the main page).
  - Provide short, plain‑language captions explaining what each visual is showing and why it matters.

In the interview, you can summarize:

> “I’d build a simple, quadrant‑driven dashboard: a market overview tab, a matrix view of momentum vs. housing, and a Success Academy footprint map. Filters by borough, ZIP, and quadrant let leaders drill from city‑wide view down to individual schools. Behind each number is a clean 3‑year growth model plus a capture‑rate translation to Future SA enrollment.”

