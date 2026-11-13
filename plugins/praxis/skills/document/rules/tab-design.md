# Tab design

Which of a tab's hosted sections show where, by the heading its type file's Sections list gives it ([reader-tabs](reader-tabs.md) says what each placement means). A heading a tab doesn't list here has no place on that tab, and the site's checks flag it as unplaced. A backend that renders reader tabs draws each tab from this design; it holds no copy of its own. (routed to maintainer: the per-tab design, 2026-11-13)

## Tabs

### Status

- **Under the head:**
  - Status
  - Verdict
  - What was wrong
- **In the instrument:**
  - What changed since you last looked?
  - What changes and why
  - What does each review request carry?
  - Open
- **After the instrument:**
  - Impact
  - Where it stands
  - Cause
  - What was changed
  - Follow-ups
  - The answer
  - What it means for us
  - How we know
  - Still open
  - Findings by severity
  - Fix first
  - Not covered
- **Only as filed:**
  - How it works
  - Depends on
  - Verification
  - Rollout and rollback
  - Iterations
  - Timeline
  - Where do I read next?

### Questions & decisions

- **In the instrument:**
  - What is paused?
- **Only as filed:**
  - What needs deciding, and by when?
  - What has been decided?
  - What was replaced or dropped?
  - What are you being asked to decide?
  - What is true today?
  - What waits on it?
  - What are the options?
  - What happens if nobody decides?
  - Who has been asked?
  - What was decided?
  - any heading that starts `Brief:`

### RAID

- **Only as filed:**
  - What is going wrong now?
  - What could stop us?
  - Whom are we waiting on?
  - What are we taking for granted?
  - What could go better than planned?
  - What has closed?

### Trace

- **In the instrument:**
  - Do old and new versions work together?
  - Have we rehearsed undoing it?
  - Where did a check fail?
  - What does a changed requirement reach?
  - What carries no requirement?
  - What must hold before each stage?
- **Only as filed:**
  - Is every requirement carried and verified?
  - What carries each requirement?
  - How is each requirement checked?
  - Where does each test run?

### FAQ

- **In the instrument:**
  - How could this fail?
- **Only as filed:**
  - What have people asked?
  - Which answers wait on an open question?
  - What must hold for this to work?

### Design

- **Only as filed:**
  - Why this, and what is out of scope?
  - What must the design be good at?
  - How does it work?
  - Which requirement does each part meet?
  - What about security, privacy and observability?
  - What happens while old and new run side by side?
  - What else did we weigh, and why not?
  - Why might we not do this?
  - What is still unresolved?
  - Where does this description disagree with itself or the code?
  - What do these words mean here?

### Requirements

- **In the instrument:**
  - What is this for?
  - What is out of scope?
- **Only as filed:**
  - How binding is each requirement?
  - What must be true?
  - How will we know each holds?
  - In what slices does it ship?
  - What is still unsettled?
  - Which decisions shape these requirements?
  - What did we decide?
  - Why did this need deciding?
  - What did we weigh?
  - What does it buy, and what does it cost?
  - How do we check the work follows it?
  - When should it be reopened?
  - any heading that starts `DEC-`

### ADRs

- **In the instrument:**
  - any heading that starts `DEC-`
- **Only as filed:**
  - What did we decide?
  - Why did this need deciding?
  - What did we weigh?
  - What does it buy, and what does it cost?
  - How do we check the work follows it?
  - When should it be reopened?

### Threats

- **In the instrument:**
  - Where do security and privacy pull apart?
  - What didn't this cover, and who checked it?
  - What didn't this cover?
  - What's left after our responses?
  - What's left for the people affected?
- **Only as filed:**
  - What are we working on?
  - What can reach what?
  - What do we rely on that others run?
  - What can go wrong, element by element?
  - What could it reveal, element by element?
  - What are we doing about each?
  - What could it reveal about people?

### Data

- **In the instrument:**
  - Must the regulator be consulted first?
  - Which libraries does it add?
  - What do we process, and why?
  - Could we use less?
  - What did the people affected say?
  - How would we leave?
  - What are we taking on?
  - Where are we near a limit?
  - What could change under us?
  - How do we restore it?
  - Does this change need a DPIA?
  - What can't we get back?
- **Only as filed:**
  - Which criteria does it meet?
  - What could it do to people, and what will we do about it?
  - What do they receive and keep?
  - Can we get our data back?
  - What would we lose, and how long would it take?

### Cutover

- **In the instrument:**
  - What do I change?
  - What does support say when asked?
  - Where does a case go when support can't solve it?
  - What fails?
- **Only as filed:**
  - What happens, in what order?
  - What decides each gate?
  - What do we measure?
  - What could go wrong at each gate?
  - What stands between the change and its users?
  - What was checked?
  - What breaks, and for whom?
  - By when?
  - Who hears what, and when?
  - Can everyone use what changed?
  - What was checked, and how?

### Runbook

- **In the instrument:**
  - Who answers, and who is next?
- **Only as filed:**
  - This alert fired: what do I do?
  - Which alerts can fire?
  - How do I run each procedure?
  - What do we hold the service to?
  - How is each measured?
  - What happens when the budget runs out?

### Glossary

- **Only as filed:**
  - What do these words mean here?

## Kept on its own tab

A section listed only as filed above stays on its own tab, after the instrument, when the site has no tab that shows what it says:

- Status, *How it works*: when the site has no Design tab
- Status, *Depends on*: when the site has no RAID tab
- Status, *Verification*: when the site has no Trace tab
- Status, *Rollout and rollback*: when the site has no Cutover tab
- Data, *What could it do to people, and what will we do about it?*: when the site has no Threats tab
- Questions & decisions, *What has been decided?*: when the site has no ADRs tab
- FAQ, *What must hold for this to work?*: when the site has no RAID tab
- Design, *What is still unresolved?*: when the site has no Questions & decisions tab
- Design, *What do these words mean here?*: when the site has no Glossary tab
- Requirements, *In what slices does it ship?*: when the site has no Design tab
- Requirements, *What is still unsettled?*: when the site has no Questions & decisions tab
- Requirements, *Which decisions shape these requirements?*: when the site has no ADRs tab
- Threats, *What do we rely on that others run?*: when the site has no Data tab
