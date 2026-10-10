import type { Status } from '../config/site';

/* ---------- Opportunities ----------
 * Only genuine Startup Roof calls are published. The 10 "SAMPLE opportunity for illustration" rows in the database
 * (apply_url = example.com) are not shown. Deadlines are date-only and provisional until a timezone and time are confirmed;
 * calendar files are generated only when `dateStatus === 'confirmed'`.
 */
export interface Opportunity {
  slug: string; name: string; organiser: string; category: string; summary: string; benefit: string; eligibility: string;
  stages: string[]; country: string; deadline: string | null; deadlineTime: string | null; deadlineTz: string | null;
  dateStatus: 'confirmed' | 'provisional'; applyHref: string; status: Status;
}
export const OPPORTUNITIES: Opportunity[] = [
  { slug: 'founder-festival-pitch-studio-2027', name: 'Founder Festival Pitch Studio 2027', organiser: 'Startup Roof', category: 'Pitch competition',
    summary: 'Pitch live to investors at Founder Festival Dubai 2027. Shortlisted companies are offered investor meetings.',
    benefit: 'Live pitch slot and investor meetings for shortlisted companies', eligibility: 'Startups planning to raise within 12 months',
    stages: ['Pre-seed', 'Seed', 'Series A'], country: 'UAE', deadline: '2027-02-15', deadlineTime: null, deadlineTz: null,
    dateStatus: 'provisional', applyHref: '/pitch/', status: 'planned' },
  { slug: 'founder-festival-startup-market-2027', name: 'Founder Festival Startup Market 2027', organiser: 'Startup Roof', category: 'Exhibition',
    summary: 'Exhibit your product to attendees, investors and corporate buyers in the Startup Market at Founder Festival Dubai 2027.',
    benefit: 'Exhibition stand in the Startup Market (package details pending)', eligibility: 'Startups with a live product',
    stages: ['Pre-seed', 'Seed', 'Series A'], country: 'UAE', deadline: '2027-02-28', deadlineTime: null, deadlineTz: null,
    dateStatus: 'provisional', applyHref: '/exhibitors/', status: 'planned' },
];

/* ---------- Academy ---------- */
export interface Track { slug: string; number: number; title: string; level: string; description: string; outcome: string; guides: string[] }
export const TRACKS: Track[] = [
  { slug: 'idea-to-validation', number: 1, title: 'Idea → Validation', level: 'Beginner', description: 'Turn a hunch into evidence with structured customer discovery.', outcome: 'A validated problem statement, 20 interviews and a decision to build or pivot.', guides: ['customer-discovery-interviews'] },
  { slug: 'mvp-to-pmf', number: 2, title: 'MVP → Product-Market Fit', level: 'Beginner', description: 'Ship the smallest thing that proves value, then measure retention relentlessly.', outcome: 'An MVP in users\' hands with a retention baseline and a PMF scorecard.', guides: ['retention-baseline'] },
  { slug: 'go-to-market', number: 3, title: 'Go-to-Market', level: 'Intermediate', description: 'Pick a wedge, a channel and a message — then prove the motion.', outcome: 'A GTM plan with ICP, positioning and a tested first channel.', guides: [] },
  { slug: 'sales', number: 4, title: 'Sales', level: 'Intermediate', description: 'Founder-led sales from first outreach to repeatable pipeline.', outcome: 'A sales playbook, pipeline stages and a 90-day target.', guides: [] },
  { slug: 'finance-unit-economics', number: 5, title: 'Finance & Unit Economics', level: 'Intermediate', description: 'Understand your numbers before an investor asks.', outcome: 'A model and CAC / LTV / payback you can defend.', guides: ['unit-economics-basics'] },
  { slug: 'fundraising-readiness', number: 6, title: 'Fundraising Readiness', level: 'Intermediate', description: 'Prepare the narrative, the data room and the investor list.', outcome: 'A seed-ready deck, data room and target investor list.', guides: ['investor-pipeline', 'investor-updates'] },
  { slug: 'hiring-leadership', number: 7, title: 'Hiring & Leadership', level: 'Intermediate', description: 'Build the first ten hires without breaking culture.', outcome: 'A hiring plan, scorecards and operating cadence.', guides: [] },
  { slug: 'dubai-gcc-market-entry', number: 8, title: 'Dubai / GCC Market Entry', level: 'All levels', description: 'Licensing, free zones, banking and the first regional customers.', outcome: 'A market-entry checklist and an entity plan to discuss with qualified advisers.', guides: [] },
  { slug: 'scaling-internationally', number: 9, title: 'Scaling Internationally', level: 'Advanced', description: 'From one market to many without losing focus.', outcome: 'A market prioritisation framework and expansion playbook.', guides: [] },
];

export interface Guide { slug: string; title: string; track: string; minutes: number; summary: string; body: string; download?: string }
export const GUIDES: Guide[] = [
  {
    slug: 'customer-discovery-interviews', track: 'idea-to-validation', minutes: 8,
    title: 'Run customer discovery interviews that produce evidence',
    summary: 'How to find interviewees, ask about past behaviour instead of opinions, and turn 20 conversations into a build-or-pivot decision.',
    download: 'customer-interview-script',
    body: `
<h2>What you are trying to learn</h2>
<p>Discovery interviews answer three questions: does the problem happen often, does it cost the person something they care about, and what do they do about it today? You are not testing your solution yet. If you pitch in the first conversation, people will be polite and you will learn nothing.</p>
<h2>Who to talk to</h2>
<ul>
<li><strong>Be specific.</strong> “Finance managers at 20–200 person logistics companies in Dubai” beats “SMEs”. A narrow segment makes patterns visible after ten interviews instead of fifty.</li>
<li><strong>Prefer people who had the problem recently.</strong> Memory of last week is reliable; memory of last year is a story.</li>
<li><strong>Avoid friends and family</strong> unless they are squarely in the segment — and even then, discount their enthusiasm.</li>
</ul>
<h2>Questions that work</h2>
<ol>
<li>“Tell me about the last time you had to [do the job].” Then stay quiet.</li>
<li>“What was the hardest part?” and “Why was that hard?”</li>
<li>“What did you try? What did it cost — in time, money or risk?”</li>
<li>“Who else was involved? Who signs off on spending to fix it?”</li>
<li>“If you could wave a wand, what would be different?” (Use sparingly — it invites opinions.)</li>
</ol>
<p>Avoid: “Would you use…?”, “How much would you pay for…?”, and any question that contains your idea. Future-tense answers are not evidence.</p>
<h2>Recording what you hear</h2>
<p>Within an hour of each call, write down: the trigger for the problem, its frequency, the workaround, the cost, the decision-maker, and one verbatim quote. Use the same sheet for every interview so you can compare.</p>
<h2>Making the decision</h2>
<p>After 15–20 interviews in one segment, count. If most people describe the same problem, in similar words, with a costly workaround and an identifiable budget owner, you have a candidate problem worth an MVP. If the answers scatter, narrow the segment or change the problem — not the interview script.</p>
<p>Signals that you should pivot: nobody has tried to solve it, the cost is trivial, or the person who feels the pain cannot buy.</p>`,
  },
  {
    slug: 'retention-baseline', track: 'mvp-to-pmf', minutes: 7,
    title: 'Set a retention baseline before you chase growth',
    summary: 'Define an active user, build a cohort table, and read the shape of the curve to know whether you have something worth scaling.',
    body: `
<h2>Define “active” honestly</h2>
<p>Pick the action that delivers the value your product promises — an invoice reconciled, a shipment booked, a lesson completed. Logins and page views are not value. Write the definition down and do not change it to make a chart look better.</p>
<h2>Build a cohort table</h2>
<p>Group users by the week (or month) they first did the core action. For each cohort, record the share who did it again in each following period. A spreadsheet is enough at this stage: one row per cohort, one column per period since start.</p>
<h2>Read the shape</h2>
<ul>
<li><strong>Falling to zero:</strong> people try it and leave. Do not spend on acquisition yet — talk to the users who left.</li>
<li><strong>Falling then flattening:</strong> a group of users keeps getting value. Find out what they have in common; that is your real segment.</li>
<li><strong>Flattening higher in newer cohorts:</strong> product changes are working. Keep shipping in that direction.</li>
</ul>
<h2>Pair numbers with conversations</h2>
<p>Each month, interview three retained users and three who churned. Ask the retained group what they would use if your product disappeared; ask the churned group what they used instead. The answers explain your curve better than another dashboard.</p>
<h2>When to scale</h2>
<p>There is no universal benchmark: a weekly-use workflow tool and an annual-purchase product retain differently. The useful test is whether the curve flattens at a level that makes your unit economics work — see the unit-economics guide.</p>`,
  },
  {
    slug: 'unit-economics-basics', track: 'finance-unit-economics', minutes: 9,
    title: 'Unit economics: CAC, contribution margin and payback',
    summary: 'Calculate what a customer costs to win, what they contribute each month, and how long it takes to earn the cost back.',
    download: 'unit-economics-worksheet',
    body: `
<h2>Customer acquisition cost (CAC)</h2>
<p>CAC = total sales and marketing spend in a period ÷ new customers won in that period. Include salaries, tools, agency fees and events — not only ad spend. Calculate it per channel when you can; a blended number hides the channel that is losing money.</p>
<h2>Contribution margin</h2>
<p>For each customer per month: revenue minus the costs that grow with that customer (payment fees, hosting, support time, delivery, third-party data). This is what each customer actually contributes towards fixed costs and growth.</p>
<h2>Payback period</h2>
<p>Payback (months) = CAC ÷ monthly contribution margin per customer. If CAC is AED 3,000 and a customer contributes AED 250 a month, payback is 12 months — and only if the customer stays that long. Check payback against your retention curve.</p>
<h2>Lifetime value (LTV) — use with care</h2>
<p>A common estimate is monthly contribution margin × expected customer lifetime in months. Early-stage lifetime is a guess; prefer observed cohort data and state your assumptions. Investors will discount an LTV built on a churn rate you have not yet seen.</p>
<h2>What to show an investor</h2>
<ul>
<li>CAC by channel for the last three to six months, with the inputs.</li>
<li>Contribution margin per customer, and what drives it up or down.</li>
<li>Payback, and the cohort data that supports the retention assumption.</li>
<li>What you will change to improve each number, and what new capital does to them.</li>
</ul>`,
  },
  {
    slug: 'investor-pipeline', track: 'fundraising-readiness', minutes: 8,
    title: 'Build and run an investor pipeline',
    summary: 'Treat a raise like a sales process: a qualified list, clear stages, a tight timeline and weekly review.',
    download: 'investor-pipeline-tracker',
    body: `
<h2>Qualify before you contact</h2>
<p>For each investor, record stage focus, sector focus, typical cheque size, geography and whether they lead or follow. Remove anyone who does not invest at your stage and size. A list of 60 qualified investors beats 300 names from a database.</p>
<h2>Prioritise warm routes</h2>
<p>Note who can introduce you: portfolio founders, angels, advisers, accelerator staff. A specific, forwardable introduction email — three lines on the company, the round and why this investor — gets more meetings than a deck attachment.</p>
<h2>Define stages</h2>
<ol>
<li>Researched</li><li>Introduction requested</li><li>First meeting</li><li>Partner meeting / deep dive</li><li>Diligence</li><li>Term sheet</li><li>Closed / Passed</li>
</ol>
<p>Record the date of every stage change and the next action with an owner. Silence for two weeks after a first meeting usually means a pass; ask directly.</p>
<h2>Run it in a tight window</h2>
<p>Batch first meetings into two or three weeks so conversations progress together. Momentum is easier to create than to restart.</p>
<h2>Review weekly</h2>
<p>Each week, look at conversion between stages. Many first meetings but no second meetings points to the pitch or the fit; few first meetings points to the list or the introductions.</p>`,
  },
  {
    slug: 'investor-updates', track: 'fundraising-readiness', minutes: 5,
    title: 'Write a monthly investor update people read',
    summary: 'A one-page format covering metrics, highlights, lowlights and specific asks — sent on the same day every month.',
    download: 'investor-update-template',
    body: `
<h2>Why send them</h2>
<p>Regular updates keep current investors able to help and turn prospective investors into warm leads for your next round. Consistency matters more than polish.</p>
<h2>A one-page format</h2>
<ol>
<li><strong>Headline</strong> — one sentence on the month.</li>
<li><strong>Key metrics</strong> — the same five every month, with the previous month alongside.</li>
<li><strong>Highlights</strong> — three bullets.</li>
<li><strong>Lowlights</strong> — what went wrong and what you are doing about it. Investors trust founders who report bad news early.</li>
<li><strong>Asks</strong> — specific: “Introductions to heads of finance at logistics companies in Riyadh”, not “any help appreciated”.</li>
<li><strong>Cash and runway</strong> — current cash and months of runway at the current burn.</li>
</ol>
<h2>Practical rules</h2>
<ul>
<li>Send on a fixed day; put it in your calendar.</li>
<li>Keep metric definitions stable; note any change.</li>
<li>Thank the people who helped last month, by name.</li>
</ul>`,
  },
];

/* ---------- Toolkit (files in /public/downloads) ---------- */
export interface Tool { slug: string; title: string; summary: string; file: string; format: string; guide?: string; track: string }
export const TOOLS: Tool[] = [
  { slug: 'investor-pipeline-tracker', title: 'Investor pipeline tracker', summary: 'Spreadsheet with qualification fields, stage dates and next actions.', file: '/downloads/investor-pipeline-tracker.csv', format: 'CSV', guide: 'investor-pipeline', track: 'fundraising-readiness' },
  { slug: 'investor-update-template', title: 'Monthly investor update template', summary: 'One-page structure with metrics, highlights, lowlights and asks.', file: '/downloads/investor-update-template.md', format: 'Markdown', guide: 'investor-updates', track: 'fundraising-readiness' },
  { slug: 'customer-interview-script', title: 'Customer interview script and notes sheet', summary: 'Past-behaviour questions and a consistent note format for discovery calls.', file: '/downloads/customer-interview-script.md', format: 'Markdown', guide: 'customer-discovery-interviews', track: 'idea-to-validation' },
  { slug: 'unit-economics-worksheet', title: 'Unit economics worksheet', summary: 'CAC, contribution margin and payback inputs with worked formulas.', file: '/downloads/unit-economics-worksheet.csv', format: 'CSV', guide: 'unit-economics-basics', track: 'finance-unit-economics' },
  { slug: 'thirteen-week-cash-flow', title: '13-week cash-flow forecast', summary: 'Weekly cash in/out template for managing runway.', file: '/downloads/13-week-cash-flow.csv', format: 'CSV', track: 'finance-unit-economics' },
  { slug: 'data-room-checklist', title: 'Seed data-room checklist', summary: 'Documents investors commonly request during diligence, grouped by area.', file: '/downloads/data-room-checklist.md', format: 'Markdown', track: 'fundraising-readiness' },
  { slug: 'pitch-deck-outline', title: 'Pitch deck outline', summary: 'Twelve-slide structure with the question each slide must answer.', file: '/downloads/pitch-deck-outline.md', format: 'Markdown', track: 'fundraising-readiness' },
  { slug: 'hiring-scorecard', title: 'Hiring scorecard', summary: 'Outcome-based role scorecard and structured interview plan.', file: '/downloads/hiring-scorecard.md', format: 'Markdown', track: 'hiring-leadership' },
];

/* ---------- TV ----------
 * No licensed or original episodes are published. The previous catalogue used third-party sample streams and concept art;
 * those are not carried over. Shows below are working titles with planned outlines, clearly marked.
 */
export interface Show { slug: string; title: string; category: string; summary: string; track?: string; episodes: { n: number; slug: string; title: string }[] }
export const TV_CATEGORIES = [
  { slug: 'build', title: 'Build', summary: 'Product, customers and early traction.' },
  { slug: 'raise', title: 'Raise', summary: 'Fundraising, investors and financial readiness.' },
  { slug: 'scale', title: 'Scale', summary: 'Hiring, markets and expansion.' },
  { slug: 'ecosystem', title: 'Ecosystem', summary: 'News, events and the regional startup scene.' },
];
export const SHOWS: Show[] = [
  { slug: 'office-hours', title: 'Office Hours', category: 'build', track: 'idea-to-validation', summary: 'A founder brings one real problem; an operator works through it with them.',
    episodes: [{ n: 1, slug: 'e1-first-customers', title: 'Finding the first ten customers' }, { n: 2, slug: 'e2-pricing', title: 'Setting a first price' }, { n: 3, slug: 'e3-retention', title: 'Reading a retention curve' }] },
  { slug: 'the-raise', title: 'The Raise', category: 'raise', track: 'fundraising-readiness', summary: 'How a round actually came together — pipeline, pitch, terms — told by the founder.',
    episodes: [{ n: 1, slug: 'e1-building-the-list', title: 'Building the investor list' }, { n: 2, slug: 'e2-first-meetings', title: 'From introduction to second meeting' }, { n: 3, slug: 'e3-term-sheet', title: 'Reading a term sheet' }] },
  { slug: 'market-entry', title: 'Market Entry', category: 'scale', track: 'dubai-gcc-market-entry', summary: 'Founders who expanded into the GCC on licensing, banking and first customers.',
    episodes: [{ n: 1, slug: 'e1-choosing-a-base', title: 'Choosing where to set up' }, { n: 2, slug: 'e2-banking', title: 'Opening a business bank account' }] },
  { slug: 'radar-weekly', title: 'Radar Weekly', category: 'ecosystem', summary: 'A short recap of verified Radar stories: rounds, funds and open calls.',
    episodes: [{ n: 1, slug: 'e1-pilot', title: 'Pilot episode' }] },
];

/* ---------- Stories (Startup Roof editorial) ---------- */
export interface Story { slug: string; title: string; date: string; summary: string; body: string }
export const STORIES: Story[] = [
  { slug: 'radar-editorial-standards', title: 'How Radar decides what to publish', date: '2026-10-10',
    summary: 'Radar now applies explicit rules on relevance, geography and financing type. Here is what changed and why.',
    body: `<p>Radar exists to help founders and investors see what is happening in startup financing and programmes across the region. An automated feed alone was not good enough: it published sport and political stories, filed an energy-policy article as a funding round, and tagged stories by the publisher's country rather than the story's.</p>
<h2>Relevance</h2><p>A Radar item must involve a startup, a startup investor, a fund, a programme, or data about startup activity. General news is excluded even when it comes from a source we otherwise use.</p>
<h2>Geography</h2><p>Each item records where the story actually happens. An item appears in a country edition only if the story is about that country, or if there is a documented connection — for example a UAE-based investor in a US round — and that connection is stated on the item.</p>
<h2>Financing type</h2><p>We distinguish equity rounds, undisclosed investments, debt, acquisitions, investment plans, fund launches with targets, fund closes, secondary sales and market data. A planned spend is not capital raised, and a fund target is not a close.</p>
<h2>Dates</h2><p>We show the date an item was collected. A publication date is shown only after it has been checked against the source.</p>
<h2>Summaries</h2><p>Items are short summaries in our own words with a link to the original publisher. We do not republish articles.</p>
<p>You can <a href="/radar/submit/">submit a story or correction</a>; submissions are reviewed before publication.</p>` },
  { slug: 'why-profiles-are-labelled-demo', title: 'Why directory profiles are labelled “demo” for now', date: '2026-10-10',
    summary: 'The startup, investor and mentor directories currently show illustrative profiles. Verified member profiles replace them as onboarding completes.',
    body: `<p>The directories show how Startup Roof will work: searchable profiles of startups, investors and mentors, with more detail available to members and sensitive information limited to verified investors.</p>
<p>Today the profiles you see are illustrative. They are marked <strong>Demo</strong> everywhere they appear, they never carry a verification badge, and they are excluded from search engines. Real profiles will appear only after the person or company has joined, completed their profile and — for investors — passed verification.</p>
<h2>What verification means</h2><p>Choosing “investor” when you sign up does not make you a verified investor. Verification is a separate review, and only verified investors can see information founders have restricted to investors.</p>` },
  { slug: 'founder-festival-2027-planning-update', title: 'Founder Festival 2027: planning update', date: '2026-10-10',
    summary: 'What is planned, what is still to be confirmed, and how founders, investors and partners can take part.',
    body: `<p>Founder Festival is the live gathering of the Startup Roof community. Planning is under way for Dubai in late March 2027.</p>
<h2>Confirmed so far</h2><ul><li>City: Dubai.</li><li>Format: three days — Discover + Connect, Build + Raise, Scale + Celebrate.</li></ul>
<h2>Still to be confirmed</h2><ul><li>Exact dates (provisionally 26–28 March 2027).</li><li>Venue.</li><li>Number of zones, ticket prices, speakers and sponsors.</li></ul>
<p>We will not publish speakers, sponsors or venue details until they are agreed. You can <a href="/festival/#interest">register interest</a>, <a href="/pitch/">apply to pitch</a> or <a href="/exhibitors/">ask about exhibiting</a> now.</p>` },
];
