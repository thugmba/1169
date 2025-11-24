# Lab Session 2: AI-Driven Inventory Optimization

## Duration: 90 minutes

## Learning Objectives
- Apply inventory management concepts (EOQ, ROP, safety stock)
- Use AI to analyze demand patterns and forecast future demand
- Optimize inventory levels considering lead times and service levels
- Balance inventory costs against stockout risks

---

## Scenario

You are the inventory manager for **ElectroMart**, a regional electronics retailer with 12 product categories. The company faces challenges:
- Frequent stockouts on popular items (losing sales)
- Excess inventory on slow-moving products (high carrying costs)
- Unpredictable seasonal demand patterns
- Variable supplier lead times

Your goal is to optimize inventory levels to achieve a 95% service level while minimizing total inventory costs.

---

## Part 1: Data Exploration and Baseline Analysis (25 minutes)

### Step 1: Review the Dataset

Open `lab2_inventory_data.csv` which contains:
- 12 months of sales data for 8 product categories
- Current inventory levels
- Supplier lead times
- Cost information (unit cost, ordering cost, holding cost %)
- Historical stockout incidents

### Step 2: Calculate Current Performance Metrics

**Calculate for each product category:**

1. **Average Monthly Demand**
2. **Demand Variability** (standard deviation)
3. **Current Inventory Turnover Ratio**
4. **Days of Inventory on Hand**
5. **Current Fill Rate**

**Create a summary table:**

| Product Category | Avg Monthly Demand | Std Dev | Current Inventory | Turnover | Days on Hand | Fill Rate |
|------------------|--------------------|---------|--------------------|----------|--------------|-----------|
| Smartphones      |                    |         |                    |          |              |           |
| Laptops          |                    |         |                    |          |              |           |
| ...              |                    |         |                    |          |              |           |

### Step 3: Identify Problem Areas

**Answer these questions:**
1. Which categories have the lowest fill rates (highest stockouts)?
2. Which categories have the highest days of inventory on hand (overstock)?
3. Which categories show the most demand variability?
4. What patterns do you notice in the seasonal data?

---

## Part 2: AI-Powered Demand Forecasting (25 minutes)

### Step 4: Forecast Future Demand

Use this prompt with your AI tool:

```
I'm managing inventory for an electronics retailer. I need to forecast demand for the next 3 months.

Historical Monthly Sales Data (units) for Smartphones:
Month 1: 245, Month 2: 267, Month 3: 298, Month 4: 231, Month 5: 256, Month 6: 312
Month 7: 289, Month 8: 278, Month 9: 334, Month 10: 401, Month 11: 478, Month 12: 523

Context:
- Strong holiday season demand in months 11-12
- Back-to-school boost in month 9
- Generally upward trend due to market growth
- New competitor entered market in month 6

Please provide:
1. Forecast for next 3 months (months 13, 14, 15) with confidence intervals
2. Identification of trend and seasonal components
3. Key factors influencing the forecast
4. Forecast accuracy assessment (if historical data were used for backtesting)
5. Recommended safety stock multiplier given demand variability
```

**Repeat for 2-3 other high-value product categories.**

### Step 5: Evaluate Forecast Quality

**For each forecast:**
1. Does the trend make business sense?
2. Are seasonal patterns properly accounted for?
3. Are the confidence intervals reasonable?
4. What are the key assumptions?
5. How would you validate this forecast?

---

## Part 3: Inventory Optimization (30 minutes)

### Step 6: Optimize Inventory Policies

Use this comprehensive prompt:

```
I need to optimize inventory for ElectroMart's electronics categories to achieve 95% service level while minimizing costs.

Product: Smartphones
- Average monthly demand: 320 units (from forecast)
- Demand standard deviation: 85 units
- Unit cost: $450
- Ordering cost: $150 per order
- Holding cost: 25% of unit cost per year
- Supplier lead time: 14 days (with 3-day standard deviation)
- Current reorder point: 150 units
- Current order quantity: 400 units
- Desired service level: 95% (Z = 1.65)

Please calculate and recommend:
1. Optimal Economic Order Quantity (EOQ)
2. Recommended Safety Stock level
3. Recommended Reorder Point
4. Expected annual ordering costs
5. Expected annual holding costs
6. Expected total inventory costs
7. Comparison with current policy (savings or additional costs)
8. Expected number of orders per year
9. Maximum inventory level
10. Average inventory level

Then provide a clear recommendation: Should we change the current policy? Why or why not?
```

**Complete this analysis for at least 4 product categories:**
- Smartphones (high-value, high-volume)
- Tablets (medium-value, medium-volume)
- Headphones (low-value, high-volume)
- Smart Home Devices (high-value, low-volume, high variability)

### Step 7: Create Optimization Summary

Build a comparison table:

| Category | Current Policy | | Optimized Policy | | Annual Savings | Implementation |
|----------|----------------|---|------------------|---|----------------|----------------|
|          | Order Qty | ROP | Order Qty | ROP | $ Amount | Priority |
| Smartphones | | | | | | |
| Tablets | | | | | | |
| Headphones | | | | | | |
| Smart Home | | | | | | |
| **Total** | | | | | | |

---

## Part 4: Advanced Optimization Scenarios (10 minutes)

### Step 8: Multi-Constraint Optimization

Add complexity to your analysis:

```
ElectroMart faces these additional constraints:
- Maximum total inventory value allowed: $850,000
- Warehouse space: 15,000 cubic feet
- Minimum order quantities from suppliers (varies by category)
- Some products are bundled (buying smartphones increases accessory demand by 30%)

Given these constraints and the optimized inventory policies from Step 6, please:
1. Identify which constraints are binding (limiting)
2. Recommend how to allocate limited resources across categories
3. Suggest which products to prioritize for optimization
4. Calculate the opportunity cost of warehouse space constraint
```

---

## Part 5: Written Report (Required Deliverable)

### Executive Summary: Top 3 Operational Improvements

**Length:** 1.5-2 pages (500-700 words)

**Required Structure:**

**1. Executive Summary (2-3 sentences)**
- Current situation and opportunity identified

**2. Improvement #1: [Title]**
- **Current State:** What's happening now?
- **Recommendation:** Specific change to implement
- **Expected Impact:** Quantified benefits
  - Cost savings: $X annually
  - Service level improvement: X%
  - Inventory reduction: X units or $X
- **Implementation:** How to execute (2-3 key steps)
- **Timeline:** When results expected
- **Risk/Considerations:** What could go wrong?

**3. Improvement #2: [Title]**
[Same structure as #1]

**4. Improvement #3: [Title]**
[Same structure as #1]

**5. Summary and Priorities**
- Total expected impact across all improvements
- Recommended implementation sequence
- Quick wins vs. long-term initiatives

**Example of Well-Written Recommendation:**

"**Improvement #1: Optimize Smartphone Inventory Policy**

*Current State:* Smartphones represent 35% of revenue but experience 8-12% stockout rate during peak periods, costing an estimated $47,000 in lost sales annually. Current policy orders 400 units when inventory drops to 150 units.

*Recommendation:* Adjust to EOQ of 285 units with reorder point of 215 units (including 95 units safety stock). This requires ordering more frequently (8.5 times vs. 6 times per year) but with smaller order sizes.

*Expected Impact:*
- Reduce average inventory by $36,000 (18% reduction)
- Decrease holding costs by $9,000 annually
- Reduce stockout rate to <2%, capturing additional $39,000 in sales
- Net annual benefit: $42,500
- Improve smartphone category fill rate from 88% to 98%

*Implementation:*
1. Update inventory management system with new parameters (Week 1)
2. Negotiate more frequent delivery schedule with supplier (Week 2)
3. Monitor stockout rates for first 60 days and adjust if needed

*Timeline:* 2 months to full implementation, benefits realized within 90 days

*Risks:* Supplier may charge premium for more frequent deliveries (estimated +$200/order, included in calculations). Higher order frequency increases administrative workload."

---

## Evaluation Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Baseline Metrics | 15 | Accurate calculation of current performance |
| Demand Forecasting | 15 | Thoughtful use of AI, critical evaluation of forecasts |
| EOQ & ROP Calculations | 20 | Correct optimization formulas and logic |
| Cost-Benefit Analysis | 15 | Accurate quantification of improvements |
| Written Report - Content | 20 | Clear, specific, actionable recommendations |
| Written Report - Quality | 10 | Professional formatting, no errors, concise |
| Critical Thinking | 5 | Questions assumptions, considers trade-offs |
| **Total** | **100** | |

---

## Discussion Questions

1. How do you balance service level targets with inventory cost objectives?
2. What are the risks of relying too heavily on AI forecasts?
3. How would you handle products with very low demand (e.g., 5 units/year)?
4. What other factors might influence inventory decisions beyond the quantitative analysis?
5. How would you implement a continuous improvement process for inventory management?

---

## Tips for Success

**Do:**
- Show your calculations (don't just report AI outputs)
- Consider practical constraints (e.g., minimum order quantities)
- Quantify everything in financial terms
- Acknowledge uncertainty and forecast errors
- Recommend implementation priorities

**Don't:**
- Ignore holding costs or ordering costs
- Assume perfect forecasts
- Recommend changes without cost justification
- Forget about warehouse space or cash flow constraints
- Overcomplicate with too many decimal places

---

## Extension Activities

**For Advanced Students:**
1. Model multi-echelon inventory (distribution center + retail stores)
2. Incorporate price elasticity (sales respond to promotions)
3. Design a dynamic pricing strategy to clear excess inventory
4. Build a Monte Carlo simulation to test inventory policy under uncertainty
5. Analyze supplier diversification vs. consolidation trade-offs

---

## Key Takeaways

After completing this lab, you should be able to:
- Use AI effectively for demand forecasting while understanding limitations
- Calculate and optimize key inventory parameters (EOQ, ROP, safety stock)
- Quantify the financial impact of inventory decisions
- Balance competing objectives (service level vs. costs)
- Communicate complex analytical recommendations to business stakeholders
- Think critically about AI-generated optimization suggestions
