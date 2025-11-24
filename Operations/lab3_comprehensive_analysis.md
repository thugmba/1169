# Lab Session 3: Comprehensive Operations Analysis & Strategic Recommendations

## Duration: 120 minutes

## Learning Objectives
- Integrate multiple operations concepts (metrics, bottlenecks, inventory)
- Conduct end-to-end supply chain analysis using AI
- Synthesize data from multiple sources
- Present strategic recommendations to executive stakeholders
- Evaluate trade-offs and implementation priorities

---

## Scenario

**GlobalTech Distribution** is a regional distributor of technology products facing operational challenges across its entire supply chain. You've been hired as an Operations Consultant to conduct a comprehensive analysis and present recommendations to the executive team.

**Company Overview:**
- 3 distribution centers serving 150 retail customers
- 200+ SKUs across 5 product categories
- $85M annual revenue, but declining margins (from 22% to 17% over 2 years)
- Growing customer complaints about delivery delays and stockouts
- Recent warehouse expansion but throughput hasn't improved proportionally

**Your Mission:** Conduct a comprehensive operations analysis and present a strategic plan to improve operational efficiency, reduce costs, and enhance customer service.

---

## Part 1: Situation Assessment (30 minutes)

### Step 1: Multi-Source Data Analysis

You have three datasets to analyze:

1. **`lab3_warehouse_operations.csv`** - Distribution center performance
   - Receiving, storage, picking, packing, and shipping metrics
   - Equipment utilization
   - Labor productivity
   - Error rates

2. **`lab3_inventory_performance.csv`** - Inventory across all locations
   - Stock levels by DC and product category
   - Turnover rates
   - Stockout incidents
   - Excess inventory situations

3. **`lab3_customer_service.csv`** - Order fulfillment data
   - Order volumes by customer segment
   - On-time delivery rates
   - Perfect order percentages
   - Customer complaints

### Step 2: Calculate Baseline Metrics

Create a dashboard view with these key metrics:

**Operational Efficiency:**
- Overall system throughput (orders/day)
- Average order cycle time
- Capacity utilization by DC
- Labor productivity (orders/labor hour)

**Inventory Performance:**
- Total inventory value
- Days of inventory on hand
- Inventory turnover by category
- Stockout rate
- Excess inventory percentage

**Customer Service:**
- Overall fill rate
- On-time delivery rate
- Perfect order rate
- Average order-to-delivery time

### Step 3: Identify Critical Issues

**Prompt for AI analysis:**

```
I'm analyzing a technology distribution company with operational challenges. Here's the key data:

WAREHOUSE OPERATIONS:
- DC1 (Northeast): 85% capacity utilization, 1,250 orders/day, picking accuracy 97.2%
- DC2 (Southeast): 92% capacity utilization, 980 orders/day, picking accuracy 95.8%
- DC3 (Midwest): 78% capacity utilization, 1,100 orders/day, picking accuracy 98.1%

BOTTLENECK INDICATORS:
- Receiving docks at DC2 at 98% utilization (causing incoming shipment delays)
- Packing station at DC1 creating 2-hour average queue times
- Shipping capacity adequate at all locations

INVENTORY ISSUES:
- Overall inventory turnover: 4.2x (industry benchmark: 6-8x)
- High-value items (laptops, servers): 6.8x turnover, occasional stockouts
- Low-value items (accessories): 2.1x turnover, chronic overstock
- Total inventory value: $18.5M (up 35% year-over-year while revenue grew only 8%)

CUSTOMER SERVICE:
- Overall fill rate: 89% (target: 95%)
- On-time delivery: 82% (target: 95%)
- Perfect order rate: 76% (industry leader: 92%)
- Major complaints: late deliveries (45%), partial shipments (30%), damaged goods (15%)

Please analyze:
1. What are the top 3 critical operational issues?
2. How do these issues interconnect (what causes what)?
3. Prioritize by impact on profitability and customer satisfaction
4. For each issue, what's the root cause vs. symptoms?
```

---

## Part 2: Deep Dive Analysis (35 minutes)

### Step 4: Bottleneck & Capacity Analysis

**Select the most critical bottleneck identified in Step 3 and analyze in depth:**

```
[For example, if receiving dock at DC2 is the primary bottleneck]

The DC2 receiving dock processes:
- Average: 42 inbound shipments per day
- Capacity: 45 shipments per day (theoretical maximum)
- Current utilization: 93%
- Average unloading time: 45 minutes per truck
- Queue time during peak: 2-3 hours

Impact:
- Delays ripple through entire DC2 operation
- 15-20% of inbound shipments arrive during peak 3-hour window (9am-12pm)
- Limited dock doors (only 4) with current scheduling system causing conflicts

Please analyze:
1. Calculate the throughput loss and revenue impact
2. Model three improvement scenarios:
   a. Add 2 more dock doors ($180K investment)
   b. Implement time-slot scheduling system ($25K + change management)
   c. Negotiate staggered delivery windows with suppliers ($minimal cost)
3. For each scenario, estimate:
   - Capacity increase
   - Implementation timeline
   - ROI and payback period
   - Risk factors
4. Which scenario would you recommend and why?
```

### Step 5: Inventory Optimization Analysis

**Focus on the inventory category with the most significant issues:**

```
Accessories category analysis:
- 85 SKUs in this category
- Combined inventory value: $2.8M
- Average turnover: 2.1x (should be 8-10x for this category)
- Carrying cost: 28% annually = $784K/year in holding costs
- Analysis shows 60% of accessories have >180 days of stock on hand
- Yet 12% of accessories had stockouts in past quarter

The paradox: Too much inventory overall, but still having stockouts.

Please analyze:
1. Explain this paradox - what's causing it?
2. Segment the 85 SKUs into:
   - Fast movers (optimize for flow)
   - Steady movers (standard EOQ approach)
   - Slow movers (reduce or eliminate)
3. Calculate the potential inventory reduction without harming service level
4. Estimate the cash freed up and annual savings
5. Provide specific recommendations for:
   - Optimal stock levels for top 20 SKUs
   - SKUs to discontinue or reduce dramatically
   - How to handle the excess inventory
```

### Step 6: Customer Service Root Cause Analysis

**Investigate why perfect order rate is only 76%:**

```
Perfect order rate breakdown (order must meet ALL criteria):
- Complete (no partial shipments): 88% ✓
- On-time delivery: 82% ✗
- Damage-free: 94% ✓
- Documentation accurate: 97% ✓
- Invoiced correctly: 99% ✓

The primary culprit is on-time delivery at 82%.

Late delivery root causes (from sample of 200 late orders):
- Warehouse bottleneck/processing delay: 38%
- Carrier performance issues: 28%
- Stockouts requiring backorder: 22%
- Inaccurate inventory (picked wrong item, had to re-ship): 8%
- Order processing errors: 4%

Please analyze:
1. Which root causes are within our control vs. external?
2. How do these interconnect with the earlier bottleneck and inventory issues?
3. Create a cause-and-effect diagram showing relationships
4. If we fix the warehouse bottleneck and inventory issues, estimate the improvement in on-time delivery
5. What additional actions are needed to reach 95% on-time delivery?
```

---

## Part 3: Strategic Recommendations (30 minutes)

### Step 7: Integrated Solution Development

Now synthesize your analysis into an integrated solution:

```
Based on all previous analyses, I need to develop an integrated operations improvement plan.

The issues are interconnected:
- [Summarize the key connections you've identified]

Budget constraints:
- Capital investment budget: $500K for this fiscal year
- Additional operational expense budget: $200K annually
- Headcount: Can add up to 5 FTEs across all locations

Goals:
- Improve perfect order rate from 76% to 92% within 12 months
- Reduce inventory value by $3M+ while improving fill rate
- Increase overall system throughput by 20%
- Generate positive ROI within 18 months

Please develop:
1. A comprehensive implementation plan with 6-8 specific initiatives
2. Sequence the initiatives (what to do first, second, etc.) with timeline
3. Estimate total investment and expected returns for each initiative
4. Identify quick wins (0-3 months) vs. structural improvements (6-12 months)
5. Quantify the expected impact on key metrics
6. Identify implementation risks and mitigation strategies
7. Resource allocation plan (budget and people)
```

### Step 8: Executive Summary Development

Transform the AI analysis into a polished executive presentation.

---

## Part 4: Executive Presentation (Required Deliverable)

### Deliverable: Written Report (3-4 pages)

**Structure:**

**PAGE 1: EXECUTIVE SUMMARY**
- Current situation (2-3 sentences)
- Key findings (3 bullet points)
- Recommended plan (2-3 sentences)
- Expected outcomes (financial and operational)

**PAGE 2: SITUATION ANALYSIS**
- Current state metrics dashboard
- Critical issues identified (top 3)
- Root cause analysis summary
- Financial impact of current issues

**PAGE 3: RECOMMENDED SOLUTIONS**

For each of your **top 3 operational improvements:**

**Improvement #1: [Descriptive Title]**
- Problem statement
- Proposed solution
- Expected impact (with specific metrics)
- Investment required
- Implementation timeline
- Priority: Quick Win / Medium-term / Strategic

**[Repeat for Improvements #2 and #3]**

**PAGE 4: IMPLEMENTATION PLAN & SUMMARY**
- 12-month roadmap (visual timeline)
- Resource requirements
- Risk assessment and mitigation
- Key milestones and success metrics
- Total expected ROI and payback period

---

## Evaluation Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Data Analysis Quality | 15 | Thorough analysis of all datasets; accurate calculations |
| Problem Identification | 15 | Correctly identifies root causes, not just symptoms |
| AI Prompt Engineering | 10 | Effective prompts that yield actionable insights |
| Critical Evaluation | 10 | Questions AI outputs, validates recommendations |
| Solutions Quality | 20 | Practical, specific, well-justified recommendations |
| Integration & Synthesis | 10 | Shows how improvements work together |
| Financial Analysis | 10 | Accurate ROI calculations and cost-benefit analysis |
| Presentation Quality | 10 | Clear, professional, executive-appropriate |
| **Total** | **100** | |

---

## Presentation Guidelines (If Oral Presentation Required)

**Format:** 10-minute presentation + 5 minutes Q&A

**Required Slides:**
1. Title slide
2. Executive summary (1 slide)
3. Current state & key metrics (1 slide)
4. Critical issues identified (1 slide)
5. Recommended solution overview (1 slide)
6. Improvement #1 details (1 slide)
7. Improvement #2 details (1 slide)
8. Improvement #3 details (1 slide)
9. Implementation roadmap (1 slide)
10. Expected ROI and summary (1 slide)

**Presentation Tips:**
- Start with the bottom line (what you recommend)
- Use visuals (charts, graphs, timelines)
- Speak in business terms (ROI, customer satisfaction, competitive advantage)
- Anticipate questions about feasibility and risk
- Be prepared to defend your priorities

---

## Common Mistakes to Avoid

**Analytical Mistakes:**
- Treating symptoms rather than root causes
- Overlooking interconnections between issues
- Ignoring practical implementation constraints
- Accepting AI recommendations without validation
- Failing to quantify financial impacts

**Presentation Mistakes:**
- Too much detail (executives want summary)
- Technical jargon without context
- Vague recommendations ("improve efficiency")
- Missing the "so what?" (business impact)
- No clear prioritization or sequencing

---

## Discussion Questions

1. How do you balance quick wins vs. structural improvements?
2. What should you do when data contradicts your hypothesis?
3. How do you handle stakeholder resistance to change?
4. What metrics would you monitor post-implementation?
5. How would you scale this analysis approach to a larger organization?
6. What are the limitations of AI in strategic decision-making?

---

## Extension Activities

**Advanced Challenges:**

1. **Multi-Objective Optimization:**
   - Simultaneously optimize for cost, service, and cash flow
   - Model trade-offs using Pareto frontier

2. **Uncertainty Analysis:**
   - Run Monte Carlo simulation on projected outcomes
   - Quantify risk-adjusted ROI

3. **Change Management Plan:**
   - Develop stakeholder communication strategy
   - Design training program for new processes
   - Create change resistance mitigation plan

4. **Competitive Analysis:**
   - Compare your recommendations to industry best practices
   - Identify competitive advantages from operations excellence

5. **Sustainability Integration:**
   - Add environmental impact metrics
   - Balance operational efficiency with sustainability goals

---

## Tips for Success

**Analysis Phase:**
✓ Start with data visualization to spot patterns
✓ Look for contradictions in the data (signals of deeper issues)
✓ Always ask "why?" five times to find root causes
✓ Validate AI calculations with manual spot-checks
✓ Consider both quantitative and qualitative factors

**Recommendation Phase:**
✓ Ensure recommendations are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
✓ Sequence initiatives logically (some may depend on others)
✓ Include both operational and financial metrics
✓ Address "how" not just "what"
✓ Acknowledge risks and mitigation plans

**Presentation Phase:**
✓ Lead with conclusions, not with analysis
✓ Use the "pyramid principle" (main point first, supporting details after)
✓ Tell a story (current state → problem → solution → future state)
✓ Make it visual (charts > tables > text)
✓ Practice defending your recommendations

---

## Key Takeaways

By completing this comprehensive lab, you should be able to:

1. **Integrate multiple operational analyses** into a coherent strategic view
2. **Identify root causes** rather than just addressing symptoms
3. **Leverage AI effectively** for complex, multi-dimensional problems
4. **Quantify business impact** of operational improvements
5. **Prioritize initiatives** based on ROI, feasibility, and strategic fit
6. **Communicate complex analysis** to executive audiences
7. **Think critically** about AI recommendations and validate outputs
8. **Develop actionable implementation plans** not just theoretical recommendations

This lab simulates real-world consulting scenarios where you must synthesize large amounts of data, identify key issues, and present compelling recommendations under time pressure.

---

## Submission Requirements

**Required Files:**
1. Written report (PDF, 3-4 pages)
2. Supporting calculations (Excel or CSV)
3. Data analysis scripts or AI prompts used (document your process)

**Optional:**
4. Presentation slides (if oral presentation component)
5. Executive summary memo (1 page max)

**Due:** [Instructor to specify]

**Submission Format:** [Instructor to specify]
