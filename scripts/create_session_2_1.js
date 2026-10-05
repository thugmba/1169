const fs = require('fs');
const path = require('path');

const out = path.join(process.cwd(), 'slides', 'session_2_1_lecture.html');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const bullets = xs => `<ul>${xs.map(x => `<li>${x}</li>`).join('')}</ul>`;
const cards = xs => `<div class="cards cards-${xs.length}">${xs.map(([tag, title, body]) => `<section class="card"><p class="tag">${tag}</p><h2>${title}</h2>${Array.isArray(body) ? bullets(body) : `<p>${body}</p>`}</section>`).join('')}</div>`;
const prompt = (label, value, kind = '') => `<section class="prompt ${kind}"><p class="tag">${label}</p><pre>${esc(value)}</pre></section>`;
const slide = (n, kicker, title, subtitle, body) => `<section class="slide"><header><div class="meta"><span>${kicker}</span><span>Session 2.1</span></div><div class="rule"></div><h1>${title}</h1><p class="subtitle">${subtitle}</p></header><main>${body}</main><footer><span>Business AI Tools: Effective ChatGPT Communication</span><span>Making Sense of Business Data</span><strong>${String(n).padStart(2, '0')} / 12</strong></footer></section>`;

const slides = [];
slides.push(`<section class="image-slide"><img src="../images/session_2_1_problem_illustration.png" alt="Restaurant owner reviewing sales data before making an operating decision."></section>`);
slides.push(slide(2, 'Module 2 | Business Data', 'The business problem comes first', 'How can a restaurant improve lunch service when the sales table is full of numbers but the decision is unclear?', cards([
  ['The problem', 'Raw rows do not answer the decision.', ['Which item sells most?', 'Which item earns the most gross profit?', 'What service problem appears in customer notes?']],
  ['The risk', 'A quick AI answer can be wrong.', ['Rows can be read incorrectly.', 'Totals can be calculated incorrectly.', 'A confident summary is not an audit.']],
  ['The goal', 'Turn data into a checked decision.', ['Organize the table.', 'Verify the calculations.', 'Use evidence to choose one action.']]
])));
slides.push(slide(3, '1 | Core Concept', 'What "making sense of data" means', 'AI can help describe patterns. A spreadsheet or calculator must verify the arithmetic.', cards([
  ['What', 'Read columns before drawing conclusions.', ['Units sold shows demand.', 'Price and cost show gross profit.', 'Customer notes explain context.']],
  ['Why', 'A single number is not enough.', ['High sales can still mean low profit.', 'A comment can reveal a service problem.', 'A total needs a checkable formula.']],
  ['Without it', 'The decision can be misleading.', ['Wrong totals lead to wrong priorities.', 'AI may fill gaps with guesses.', 'The team cannot explain the recommendation.']]
])));
slides.push(slide(4, '2 | Operating Method', 'Use a five-step data audit', 'Do the calculation in a spreadsheet first. Then ask AI to explain the verified results.', `<div class="flow"><div><b>1. Inspect</b><span>Read each column and unit.</span></div><div><b>2. Calculate</b><span>Revenue and gross profit.</span></div><div><b>3. Verify</b><span>Check totals in a spreadsheet.</span></div><div><b>4. Explain</b><span>Ask AI for patterns.</span></div><div><b>5. Act</b><span>Choose one measurable action.</span></div></div>`));
slides.push(slide(5, '3 | Bad Example 1 of 2', 'Bad prompt: ask for a conclusion without data rules', 'The prompt does not tell AI which numbers matter or how to treat arithmetic.', `<div class="two-col">${prompt('Prompt to avoid', 'Here is our restaurant data.\nWhat should we improve?', 'bad')}<section class="card danger"><p class="tag">Why it fails</p>${bullets(['No columns or decision criterion are named.', 'The answer can become generic advice.', 'There is no request to verify totals.'])}</section></div>`));
slides.push(slide(6, '3 | Bad Example 2 of 2', 'Bad prompt: ask AI to guarantee the math', 'A language-model answer is not a substitute for a calculation check.', `<div class="two-col">${prompt('Prompt to avoid', 'Add all sales rows, tell us the exact profit, and guarantee that your total is correct.', 'bad')}<section class="card danger"><p class="tag">Why it fails</p>${bullets(['It asks for certainty without an audit.', 'It gives no formula or cross-check.', 'A polished number can still be wrong.'])}</section></div>`));
slides.push(slide(7, '4 | Good Example 1 of 2', 'Good prompt: inspect the data before analysis', 'Use this prompt before making any recommendation.', prompt('Copy and adapt', 'You are a restaurant operations analyst.\nUse only the Session 2.1 dataset.\n\nFirst, create three lists:\n1. Columns and what each measures\n2. Facts visible in the rows\n3. Information missing for a full decision\n\nDo not calculate or invent totals.\nEnd with three questions for the owner.', 'good')));
slides.push(slide(8, '5 | Practice Data', 'Session 2.1 restaurant sales data', 'This fictional instructional CSV is complete enough for the exercises. Use a spreadsheet to verify each calculation.', cards([
  ['Sales', 'What sold?', ['Burger: 58 units.', 'Wrap: 32 units.', 'Salad: 18 units.', 'Soup: 12 units.']],
  ['Verified totals', 'What did the spreadsheet calculate?', ['Revenue: $1,016.00.', 'Gross profit: $633.60.', 'Burger gross profit: $313.20.']],
  ['Customer notes', 'What needs attention?', ['Two notes mention a lunch queue.', 'One item sold out at 1 PM.', 'Pickup speed is a possible issue.']]
])));
slides.push(slide(9, '4 | Good Example 2 of 2', 'Good prompt: explain verified results', 'AI explains patterns after the spreadsheet supplies the checked totals.', prompt('Copy and adapt', 'You are a restaurant operations analyst.\nUse the Session 2.1 dataset and\nthese verified spreadsheet totals:\n- Revenue: $1,016.00\n- Gross profit: $633.60\n- Burger gross profit: $313.20\n\nWrite three bullets:\n1. One demand pattern\n2. One profit pattern\n3. One service issue in the notes\n\nRecommend one two-week action.\nName one metric to track.\nDo not recalculate the totals.', 'good')));
slides.push(slide(10, '6 | Guided Practice', 'Exercise 1: Verify, then explain', 'Students work in pairs with `data/session_2_1_restaurant_sales.csv`.', cards([
  ['Step 1', 'Calculate', ['Revenue = units sold x unit price.', 'Gross profit = units sold x (price - food cost).']],
  ['Step 2', 'Verify', ['Check the total revenue.', 'Check the total gross profit.', 'Compare with Slide 8.']],
  ['Step 3', 'Explain', ['Run Good Example 2.', 'Mark every claim as fact or interpretation.']]
])));
slides.push(slide(11, '7 | Applied Challenge', 'Exercise 2: Choose one small improvement', 'The data show a long lunch queue and strong burger demand. Choose one action to test for two weeks.', cards([
  ['Problem', 'State one observation', ['Lunch queue notes appear twice.', 'Burger demand is highest.']],
  ['Action', 'Choose one response', ['Prepare burger ingredients before noon.', 'Add one pickup sign.', 'Assign one staff member to lunch pickup.']],
  ['Measure', 'Check whether it worked', ['Track average lunch wait time.', 'Target: reduce it by one minute.', 'State the result after two weeks.']]
])));
slides.push(slide(12, '8 | Takeaway', 'A reliable data-to-decision checklist', 'Use AI for explanation and drafting. Use a spreadsheet for arithmetic and verification.', cards([
  ['1', 'Inspect', ['Know what every column measures.']],
  ['2', 'Verify', ['Use formulas and check totals.']],
  ['3', 'Explain', ['Ask AI for patterns in verified results.']],
  ['4', 'Act', ['Choose one measurable improvement.']]
])));

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Session 2.1: Making Sense of Business Data</title><style>
@page{size:16in 9in;margin:0}*{box-sizing:border-box}body{margin:0;background:#334155;color:#292524;font-family:"Times New Roman",Times,serif;line-height:1.34}.image-slide{width:16in;height:9in;margin:18px auto;page-break-after:always;overflow:hidden;background:#fff}.image-slide img{width:100%;height:100%;object-fit:cover;display:block}.slide{width:16in;height:9in;margin:18px auto;background:#fff;padding:.42in .72in .34in;display:flex;flex-direction:column;overflow:hidden;page-break-after:always}header{flex-shrink:0;margin-bottom:.16in}.meta{display:flex;justify-content:space-between;color:#64748b;font-size:16px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}.meta span:first-child{color:#c2410c}.rule{height:5px;background:#c2410c;margin:7px 0 8px}h1{font-size:52px;line-height:1.1;margin:0;letter-spacing:-.6px}.subtitle{margin:6px 0 0;color:#475569;font-size:26px}main{flex:1;min-height:0;display:flex;flex-direction:column;margin-bottom:.18in}.cards{display:grid;gap:16px;flex:1;min-height:0}.cards-3{grid-template-columns:repeat(3,1fr)}.cards-4{grid-template-columns:repeat(4,1fr)}.card,.prompt{border:1px solid #cbd5e1;border-radius:18px;padding:18px 20px;background:#fff;overflow:hidden}.cards .card{background:#fff7ed}.card h2{font-size:28px;line-height:1.15;margin:3px 0 10px}.card p,.card li{font-size:24px}.tag{margin:0;color:#c2410c;font-size:16px!important;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.card ul{padding-left:22px;margin:8px 0 0}.card li{margin:0 0 8px}.two-col{display:grid;grid-template-columns:1.15fr .85fr;gap:20px;flex:1;min-height:0}.prompt{background:#172033;color:#edf2f7;border-color:#172033}.prompt pre{white-space:pre-wrap;margin:8px 0 0;font:24px/1.36 "Courier New",monospace;overflow-wrap:anywhere}.prompt .tag{color:#cbd5e1}.prompt.bad{background:#fff1f2;color:#3f0c15;border-color:#fecdd3}.prompt.bad .tag{color:#b91c1c}.prompt.good{background:#ecfdf5;color:#153d2d;border-color:#86efac}.prompt.good .tag{color:#166534}.danger{background:#fff1f2!important;border-color:#fecdd3}.flow{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;flex:1;align-items:center}.flow div{min-height:175px;padding:18px;border-radius:18px;background:#fff7ed;border:1px solid #cbd5e1;display:flex;flex-direction:column;justify-content:center}.flow b{font-size:28px;margin-bottom:9px}.flow span{font-size:23px}footer{height:.36in;flex-shrink:0;border-top:1px solid #cbd5e1;display:flex;justify-content:space-between;align-items:end;color:#64748b;font-size:15px}footer strong{color:#c2410c}@media print{body{background:#fff}.image-slide,.slide{margin:0;break-after:page}}
</style></head><body>${slides.join('\n')}</body></html>`;
fs.writeFileSync(out, html);
