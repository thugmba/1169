# Operations & Supply Chain: Leveraging AI for Business Optimization

## Course Module: AI-Driven Operations & Supply Chain Management

### Learning Objectives
By the end of this module, students will be able to:
1. Identify and calculate key operations metrics
2. Perform bottleneck analysis using AI-assisted methods
3. Apply AI tools to inventory optimization problems
4. Communicate operational recommendations effectively

---

## Part 1: Key Operations Metrics

### 1.1 Throughput Metrics
**Throughput** is the rate at which a system produces or processes output.

**Formula:** Throughput = Units Produced / Time Period

**Example:** A manufacturing line produces 480 units in an 8-hour shift.
- Throughput = 480 units / 8 hours = 60 units/hour

### 1.2 Cycle Time
**Cycle Time** measures how long it takes to complete one unit from start to finish.

**Formula:** Cycle Time = Total Production Time / Number of Units Produced

**Key Insight:** Lower cycle time generally means higher efficiency, but must be balanced with quality.

### 1.3 Capacity Utilization
**Capacity Utilization** shows what percentage of available capacity is being used.

**Formula:** Capacity Utilization = (Actual Output / Maximum Possible Output) × 100%

**Interpretation:**
- 85-90%: Optimal range for most operations
- >95%: Risk of bottlenecks and quality issues
- <70%: Underutilization, excess capacity costs

### 1.4 Lead Time
**Lead Time** is the total time from order placement to delivery.

**Components:**
- Order processing time
- Production/procurement time
- Transportation time
- Queue/waiting time

### 1.5 Inventory Turnover
**Inventory Turnover** measures how many times inventory is sold and replaced over a period.

**Formula:** Inventory Turnover = Cost of Goods Sold / Average Inventory Value

**Example:** 
- COGS = $1,200,000
- Average Inventory = $200,000
- Turnover = 6 times per year (inventory replaced every 2 months)

### 1.6 Fill Rate
**Fill Rate** measures the percentage of customer orders fulfilled immediately from stock.

**Formula:** Fill Rate = (Orders Fulfilled from Stock / Total Orders) × 100%

**Target:** Most businesses aim for 95-98% fill rate.

---

## Part 2: Bottleneck Analysis

### 2.1 What is a Bottleneck?
A **bottleneck** is any resource whose capacity is less than or equal to the demand placed upon it. It constrains the entire system's throughput.

### 2.2 Theory of Constraints (TOC)
Developed by Eliyahu Goldratt, TOC focuses on identifying and managing the constraint that limits system performance.

**The Five Focusing Steps:**
1. **Identify** the system's constraint
2. **Exploit** the constraint (maximize its efficiency)
3. **Subordinate** everything else to the constraint
4. **Elevate** the constraint (increase its capacity)
5. **Repeat** the process (find the next constraint)

### 2.3 Identifying Bottlenecks

**Method 1: Process Mapping**
- Map each step in the process
- Measure capacity at each step
- The step with lowest capacity is the bottleneck

**Method 2: Queue Analysis**
- Observe where work-in-process accumulates
- Long queues indicate bottlenecks upstream

**Method 3: Resource Utilization**
- Calculate utilization rates for all resources
- The resource at or near 100% utilization is likely the bottleneck

### 2.4 AI Applications in Bottleneck Analysis

**How AI Helps:**
1. **Pattern Recognition:** Identifies bottlenecks from historical data
2. **Predictive Analytics:** Forecasts future bottlenecks before they occur
3. **Simulation:** Tests "what-if" scenarios without disrupting operations
4. **Real-time Monitoring:** Alerts when bottlenecks are forming

**Example Prompt for AI:**
"Analyze this production data [dataset] and identify bottlenecks. For each bottleneck, calculate the impact on overall throughput and suggest three specific improvements."

---

## Part 3: Inventory Optimization

### 3.1 The Inventory Challenge
Businesses face a fundamental tension:
- **Too much inventory:** High carrying costs, obsolescence risk, cash tied up
- **Too little inventory:** Stockouts, lost sales, poor customer service

### 3.2 Key Inventory Concepts

**Safety Stock:** Buffer inventory to protect against uncertainty in demand and supply.

**Formula:** Safety Stock = Z × σ × √L
Where:
- Z = Service level factor (e.g., 1.65 for 95% service level)
- σ = Standard deviation of demand
- L = Lead time

**Reorder Point:** The inventory level that triggers a new order.

**Formula:** ROP = (Average Daily Demand × Lead Time) + Safety Stock

**Economic Order Quantity (EOQ):** The optimal order quantity that minimizes total inventory costs.

**Formula:** EOQ = √[(2 × D × S) / H]
Where:
- D = Annual demand
- S = Order cost per order
- H = Holding cost per unit per year

### 3.3 Inventory Classification: ABC Analysis

**Class A:** 20% of items, 80% of value → Tight control, frequent review
**Class B:** 30% of items, 15% of value → Moderate control
**Class C:** 50% of items, 5% of value → Simple controls, bulk orders

### 3.4 AI-Driven Inventory Optimization

**Traditional Approach Limitations:**
- Assumes constant demand
- Doesn't adapt to seasonality
- Ignores external factors (weather, trends, competition)

**AI Advantages:**
1. **Demand Forecasting:** Machine learning models predict demand more accurately
2. **Dynamic Optimization:** Adjusts reorder points and quantities in real-time
3. **Multi-variable Analysis:** Considers dozens of factors simultaneously
4. **Scenario Planning:** Tests thousands of inventory strategies instantly

**Key AI Techniques:**
- Time series forecasting (ARIMA, Prophet, LSTM)
- Regression analysis for demand drivers
- Reinforcement learning for policy optimization
- Natural language processing for market signals

### 3.5 Implementing AI for Inventory Management

**Step 1: Data Collection**
- Historical sales data
- Lead times from suppliers
- Carrying costs and ordering costs
- Seasonality patterns
- External factors (promotions, holidays, economic indicators)

**Step 2: Demand Forecasting**
Prompt AI to:
- Analyze historical patterns
- Identify seasonality and trends
- Generate probabilistic forecasts (not just point estimates)
- Quantify forecast uncertainty

**Step 3: Optimization**
Prompt AI to:
- Calculate optimal order quantities
- Determine reorder points considering lead time variability
- Set safety stock levels based on desired service level
- Balance costs against service level

**Step 4: Continuous Improvement**
- Monitor forecast accuracy
- Update models with new data
- Refine optimization parameters

---

## Part 4: Practical Framework for Using AI in Operations

### 4.1 The Prompt Engineering Process

**Effective AI Prompts Should Include:**
1. **Context:** "I'm managing inventory for a retail electronics store..."
2. **Objective:** "...to minimize total costs while maintaining 95% fill rate..."
3. **Data:** "...here is 24 months of sales data and supplier lead times..."
4. **Constraints:** "...budget is limited, storage capacity is 10,000 units..."
5. **Desired Output:** "...provide specific reorder points for each product category."

### 4.2 Sample Prompt Template

```
You are an operations consultant specializing in [AREA: inventory/bottleneck/capacity].

Context: [Describe the business situation]

Data: [Provide relevant data or describe dataset]

Objective: [What you want to achieve]

Constraints: [Limitations or requirements]

Analysis Request:
1. [Specific analysis needed]
2. [Additional calculations]
3. [Recommendations format]

Please structure your response as:
- Executive Summary
- Key Findings
- Detailed Analysis
- Specific Recommendations with expected impact
```

### 4.3 Validating AI Recommendations

**Critical Thinking Checklist:**
- Does the math check out?
- Are the assumptions reasonable?
- Does it align with industry standards?
- Can we implement this practically?
- What are the risks if the AI is wrong?

**Always:**
- Verify calculations manually for key decisions
- Test recommendations on small scale first
- Have domain experts review AI outputs
- Document assumptions and limitations

---

## Part 5: Integrating Metrics, Bottlenecks, and Inventory

### 5.1 The Interconnected System

Operations management requires holistic thinking:
- **Bottlenecks** limit throughput → affect **inventory** needs
- **Inventory** levels impact **lead times** and **cycle times**
- **Metrics** reveal where **bottlenecks** exist

### 5.2 End-to-End Optimization

**Example Scenario:**
A distribution center has:
- Receiving bottleneck (capacity: 500 units/hour)
- Storage capacity: 50,000 units
- 200 SKUs with varying demand
- 15 different suppliers with 3-14 day lead times

**AI-Assisted Approach:**
1. Use AI to identify receiving as the primary bottleneck
2. Calculate impact on inventory holding costs
3. Optimize ordering schedule to smooth receiving demand
4. Rebalance inventory across SKUs based on new constraints
5. Project cost savings and service level improvements

---

## Conclusion: AI as a Decision Support Tool

AI doesn't replace human judgment in operations management—it enhances it. The most successful operations managers:

1. **Understand the fundamentals** (metrics, bottlenecks, inventory theory)
2. **Leverage AI** for data analysis and optimization
3. **Apply critical thinking** to validate and refine AI recommendations
4. **Communicate effectively** to implement changes
5. **Monitor and iterate** continuously

---

## Key Takeaways

1. **Metrics provide visibility:** You can't manage what you don't measure
2. **Bottlenecks determine system capacity:** Focus improvement efforts where they matter most
3. **Inventory optimization balances trade-offs:** Cost vs. service level
4. **AI excels at pattern recognition and optimization:** But requires good data and clear objectives
5. **Human expertise remains essential:** For context, judgment, and implementation

---

## Additional Resources

**Books:**
- "The Goal" by Eliyahu Goldratt (Theory of Constraints)
- "Factory Physics" by Hopp & Spearman
- "The Toyota Way" by Jeffrey Liker

**Online Tools:**
- Inventory optimization calculators
- Process simulation software
- AI platforms (Claude, ChatGPT with data analysis)

**Metrics to Track:**
- On-time delivery rate
- Inventory carrying costs
- Capacity utilization by resource
- Lead time variability
- Forecast accuracy (MAPE, bias)

---

## Preparing for the Hands-On Labs

In the upcoming lab sessions, you will:

**Lab 1:** Analyze production data to identify bottlenecks and calculate operational metrics
- [Lab 1](lab1_bottleneck_analysis.html)
- [Dataset](lab1_production_data.csv)

**Lab 2:** Use AI to optimize inventory levels for a multi-product retail scenario with seasonal demand
- [Lab 2](lab2_inventory_optimization.html)
- [Dataset](lab2_inventory_data.csv)

**Lab 3:** Conduct comprehensive operations analysis and present recommendations
- [Lab 3](lab3_operations_analysis.html)
- [Dataset](lab3_customer_service.csv)

**What to Review:**
- Formulas for throughput, cycle time, and capacity utilization
- EOQ and reorder point calculations
- How to structure effective prompts for AI
- Critical evaluation of AI-generated recommendations
