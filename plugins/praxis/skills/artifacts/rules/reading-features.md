# Reading features

A reader moves around a documentation site by its ids, its tabs and its views. These features let them do it without losing their place, take a brief to a meeting, and ask what a chart means. A page has every feature with scripts on, and reads complete without any. (basis: maintainer, 2026-11-19, the reading features of the visual-library design)

## What every page carries

**Cards.** One card per item in the store. The cards are embedded in the page, so it needs no fetch and works opened from disk. Restricted items are held apart here as in every view, and search says how many. A card holds:
- the item's id, kind, title and state;
- who decides it, or else who owns it;
- its due point, its `decide_by` as written;
- the first 200 characters of its body;
- how many items it waits on and how many it unlocks;
- the tab it lives on.

**The tab an item lives on.** The tab whose instrument holds the item's kind and the fewest other kinds, the earlier in the navigation on a tie. A record is never a home. A kind lives elsewhere only when that tab can't select it: a gate lives on the cutover tab, where its card is.

## Features

- **Hover previews.** Every id on the page, in prose, in a list or on a chart, opens its card in place on hover, focus or tap, without moving the page.
  - The card links to the tab the item lives on, selected there.
  - It stays while the pointer crosses into it, and closes 180 ms after the pointer leaves both, long enough to cross the gap.
  - Escape closes it, and closes nothing else.
  - An id that is itself a control, such as a map node, keeps its own action on a click, and shows its card on hover or focus.
- **Search.** The top bar's search button or ⌘K (Ctrl+K) opens it. It reads the cards, so a body is searched only in its excerpt, which keeps every page's cards small. An item matches when every word typed appears in its id, title, kind or excerpt. It ranks:
  1. an exact id;
  2. a title holding every word, the first of them at its start;
  3. a title holding every word, in any order;
  4. any other match.

  Within a rank, results keep the store's order. It shows eight, each with the tab it lives on. The arrow keys move, Enter opens and closes the search, and Escape closes it alone.
- **Deep links.** The address holds what the reader sees: `view`, the map's `mode` and `owner`, each tab filter as `f-<filter>`, the selection as `sel`, the `lens`, and the map's day as `at`. It changes as the reader changes them, so a copied address opens the same view. A value left at its default is left out. A selection in a view not shown opens that view first, unless the link names its view. The older bare `#<id>` still selects that item. The top bar's "Copy link to this view" control copies the address.
- **Theme.** System, Dark or Light, from a small menu button at the end of the top bar, beside Sources and Codes, its icon the current mode: a half-filled circle, a moon or a sun. The menu marks the current choice, takes arrow keys, and closes on Escape or a click outside, returning focus to its button. The theme follows the reader's system until they choose, and the choice is kept on their device. Both palettes are the site stylesheet's tokens, and the accent stays for content choices.
- **Keyboard.**
  - Everything a keyboard reaches shows a focus ring, map nodes included.
  - The keys 1 to 9 open the tabs in the bar's order.
  - V shows the tab's next view.
  - On the map, → moves to the first item the focused one unlocks and ← to the first it waits on. ↑ and ↓ step through the items linked to the one the walk came from, or before any walk, to the focused one, starting at the first for ↓ and the last for ↑.
  - Keys typed into a field are left alone.
- **Motion.** A view the picker shows fades in over a quarter of a second. A reader whose system asks for reduced motion gets none.
- **Reader lenses.** The status tab's "Reading as" control re-ranks the tab for one reader: Everyone (the whole tab), Decider, Engineer, Reviewer or Newcomer. A lens leads with its own headline, counted from what it shows, then its blocks, and says what it leaves out, with a control back to everything. Every lens holds restricted items apart, as every view does. The deep link holds the lens as `lens`, and a link without one shows Everyone. The lens is not kept on the device: it hides most of the tab, so a visit without a link starts at Everyone.
  - **Decider:** the waiting questions and decisions grouped by decider. The four deciders holding the most come first, most first, then by name. Items with nobody named follow as a group of their own. Each group shows four items, by tier, then due date, then id. Each card says what its answer unlocks on the map, and a past-due one is marked. Then the three items settled most recently by an agreement, each once. It leaves out the work, risks, review requests and the design.
  - **Engineer:** four of the pieces of work not merged that can start now, a piece with no waits among them. Then four that are blocked, each naming up to three unfinished items it waits on, gates aside. Then the three biggest open risks, ranked as the RAID tab ranks them. It leaves out decisions already made, deciders, the glossary and the gates.
  - **Reviewer:** six merged pieces, newest merge first, each with what it serves; merged is what the status tab counts as merged, work whose review request is named. Then four requirements built but not yet verified. It leaves out gates, deciders and forecasts.
  - **Newcomer:** the overview's title and opening. Then the three agreed or recorded decisions that the most items directly rest on or are blocked by, ties in the store's order, and the first two terms by id. Then whom to ask: the four deciders holding the most waiting items, each with their first five ids. It leaves out the work list, review requests and risks.
- **Time travel.** On the map, an "As it stood on" control steps through every day the store dates something, from the earliest to today, and redraws the map as it stood. A set with fewer than two such days gets no control. Only the map travels: other tabs count today's states, since stores filed before `state_changes` existed don't date them.
  - An item appears on the day it was first filed. An item with no filed date, or held apart as restricted, is taken as always there.
  - An item done today turns done on its kind's own event: a question or decision on the day an agreement first settled it or its `state_changes` first record it agreed, whichever is earlier, a piece of work on its merge date, a gate on its first run that held. An item done today with no such date stays done throughout.
  - A link that carries `since` is drawn from that day; one without is drawn on every day.
  - An item not done today never shows done on an earlier day: the map takes today's done items back in time rather than replaying each item's changes.
  - The map draws each day afresh, so its filters, sizes and labels follow that day's states. Wording and places on the map are today's, so an item filed later leaves a gap. The control says all this, naming undated links as today's when the map has any, and on a day before anything on the map was filed it says so and names the first filing day.
  - The deep link holds the day as `at`. A day the store doesn't date opens the latest dated day before it, or the earliest when it comes before them all.
- **The one-page brief.** The status tab offers "Print the one-page brief", and printing the status tab by any means gives the same page. It holds:
  - the tab's headline;
  - three numbers: the pieces of work merged, the tier-1 answers waiting with how many of those are past due, counted as the status tab's own tile counts them, and the next gate with how many things it waits on;
  - what needs an answer: the first five waiting questions and decisions that aren't restricted, by tier, then by due date, then by id, each with its decider;
  - the risk the RAID tab's lead names as the biggest, with its response, so the two never disagree.

  It is always in the light palette, whatever the reader's theme.
- **Explain this.** Where the page's backend can ask a model on the reader's behalf, a button on each tab's instrument asks it to explain what the reader sees, in plain prose citing item ids.
  - It sends the instrument's text in the view shown, the tab, headline and view names, and for each id that text names its id, kind, title, state, decider or owner and due date. It sends nothing else.
  - The prompt asks for plain prose of at most 150 words, every item cited by its id, using only that data. It is kept under the backend's request-size limit: the cards are halved down to 20, then the text is cut. The prompt says what was cut.
  - It asks the backend's quickest model tier, since the answer reads data it is handed.
  - The answer streams in under the instrument, only for that reader, and runs on the reader's own account. The first ask in a view asks their consent, and the button turns to Stop while it runs.
  - A reader who declines, or a view that can't ask, sees no button. The adapter of each backend that offers this says how it asks and its limits.

Cited by the [claude-artifacts](../adapters/claude-artifacts.md) adapter.
