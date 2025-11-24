# Lab Session 1: Bottleneck Analysis and Operations Metrics

## Duration: 90 minutes

## Learning Objectives
- Calculate key operations metrics from production data
- Identify bottlenecks in a manufacturing process
- Use AI to analyze operational efficiency
- Recommend specific improvements with quantified impact

---

## Scenario

You are an operations analyst for **TechAssembly Inc.**, a company that manufactures consumer electronics. The production line has 5 workstations, and management is concerned about declining throughput and increasing cycle times.

Your task is to analyze the production data, identify bottlenecks, calculate key metrics, and provide recommendations.

---

## Part 1: Data Analysis (30 minutes)

### Step 1: Review the Dataset
Open the file `lab1_production_data.csv` which contains:
- Workstation capacities
- Actual output by workstation
- Processing times
- Daily production volumes over 20 days

### Step 2: Calculate Key Metrics

**Calculate manually (use spreadsheet):**

1. **Throughput** for each workstation
2. **Capacity Utilization** for each workstation
3. **Cycle Time** for the entire line
4. **Average Daily Output** across the 20-day period
5. **Bottleneck Impact** (how much throughput is limited)

**Questions to Answer:**
- Which workstation is the bottleneck?
- What is the system's theoretical maximum throughput?
- What is the actual throughput?
- What is the gap (lost capacity)?

---

## Part 2: AI-Assisted Analysis (30 minutes)

### Step 3: Prompt AI for Bottleneck Analysis

Use the following prompt structure with your AI tool (Claude, ChatGPT, etc.):

```
I'm analyzing a 5-station manufacturing process. Here is the production data:

[Paste the dataset or describe the key figures]

Workstation capacities (units/hour):
- Station 1 (Component Prep): 120
- Station 2 (Sub-Assembly): 95
- Station 3 (Main Assembly): 110
- Station 4 (Quality Check): 100
- Station 5 (Packaging): 130

Actual utilization over 20 days shows Station 2 consistently at 98-100% utilization while others range from 70-85%.

Please analyze:
1. Identify the bottleneck and explain your reasoning
2. Calculate the throughput loss due to the bottleneck
3. Estimate the financial impact if each unit has a profit margin of $15
4. Provide THREE specific recommendations to address this bottleneck, ranked by implementation difficulty and expected impact
5. For each recommendation, estimate the throughput improvement and ROI
```

### Step 4: Evaluate AI Response

**Review the AI's analysis and answer:**
1. Did the AI correctly identify the bottleneck?
2. Are the calculations accurate? (Verify at least 2 calculations)
3. Are the recommendations practical?
4. What assumptions did the AI make?
5. What additional information would you need to implement these recommendations?

---

## Part 3: Comparative Analysis (20 minutes)

### Step 5: Test Alternative Scenarios

Prompt the AI to analyze "what-if" scenarios:

```
Based on the previous analysis, model these three scenarios:

Scenario A: Increase Station 2 capacity by 20% (cost: $50,000)
Scenario B: Add a second parallel Station 2 (cost: $120,000)
Scenario C: Reduce incoming work to Station 2 by improving Station 1 efficiency by 15% (cost: $30,000)

For each scenario:
- Calculate new system throughput
- Estimate annual profit increase
- Calculate payback period
- Identify if a new bottleneck would emerge
```

### Step 6: Compare Results

Create a comparison table:

| Scenario | Investment | Throughput Increase | Annual Profit Increase | Payback Period | New Bottleneck? |
|----------|------------|---------------------|------------------------|----------------|-----------------|
| A        |            |                     |                        |                |                 |
| B        |            |                     |                        |                |                 |
| C        |            |                     |                        |                |                 |

---

## Part 4: Written Report (10 minutes)

### Deliverable: Executive Summary

Write a 1-page executive summary (300-400 words) that includes:

**Required Sections:**
1. **Current State:** Key metrics and identified bottleneck
2. **Impact:** Quantified cost of the bottleneck
3. **Recommendations:** Top 3 improvements with expected outcomes
4. **Implementation Priority:** Which to do first and why

**Format Requirements:**
- Use bullet points for recommendations
- Include specific numbers (throughput gains, costs, ROI)
- Write for a non-technical executive audience
- Be concise and action-oriented

**Example Opening:**
"Analysis of TechAssembly's production line reveals a critical bottleneck at Station 2 (Sub-Assembly) that limits system throughput to 95 units/hour, despite downstream capacity of 110+ units/hour. This constraint costs the company approximately $[X] annually in lost profit..."

---

## Evaluation Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Metric Calculations | 20 | Accuracy of throughput, utilization, and cycle time calculations |
| Bottleneck Identification | 15 | Correct identification with supporting data |
| AI Prompt Quality | 15 | Clear, specific prompts with necessary context |
| Critical Evaluation | 20 | Thoughtful assessment of AI recommendations |
| Scenario Analysis | 15 | Complete comparison with accurate projections |
| Written Report | 15 | Clear, concise, actionable recommendations |
| **Total** | **100** | |

---

## Discussion Questions

1. What are the limitations of using AI for bottleneck analysis?
2. How would you validate the AI's recommendations before implementation?
3. What additional data would improve the accuracy of this analysis?
4. How might the bottleneck shift if demand increases by 50%?
5. What are the risks of over-optimizing for a single bottleneck?

---

## Tips for Success

**Do:**
- Verify AI calculations manually for critical figures
- Consider practical constraints (budget, space, labor availability)
- Think about second-order effects (what happens after bottleneck is fixed?)
- Use specific numbers in your recommendations

**Don't:**
- Accept AI outputs without critical evaluation
- Ignore qualitative factors (employee morale, quality impacts)
- Recommend solutions without considering implementation feasibility
- Forget to quantify the financial impact

---

## Extension Activities

**For Advanced Students:**
1. Model the system using queuing theory
2. Simulate the production line with Python or simulation software
3. Design a monitoring dashboard to track bottleneck metrics in real-time
4. Analyze labor scheduling to support bottleneck optimization

---

## Key Takeaways

By the end of this lab, you should understand:
- How to systematically identify bottlenecks using data
- The relationship between capacity, utilization, and throughput
- How to leverage AI for operational analysis while maintaining critical thinking
- How to quantify and communicate the business impact of operational improvements
