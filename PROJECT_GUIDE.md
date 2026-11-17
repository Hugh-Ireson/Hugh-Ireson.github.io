# Adding a project

Keep project summaries concise and link skills to evidence.

1. Add a card to `Project.html` and, if featured, `index.html`. Copy an existing `project-card` article.
2. Include a title, one-sentence purpose, three specific skill tags and a short tools line. Use an original project visual with descriptive alternative text.
3. Link each skill tag to `project-page.html#skill-id`. Create a matching section on the project page using the `evidence` class and that ID.
4. Each evidence section should explain what you did, why you chose the method and where the visitor can inspect it (code, chart, report or demo). State limitations rather than imply unsupported results.
5. Add a short delivered result and working demo/code/report links. Use the same shared header, footer and `assets/site.css` as existing pages.
6. Verify relative links and anchor IDs. Review keyboard navigation and narrow screens. Do not add personal data, client material or metrics without permission and evidence.

`assets/projects.json` records the existing card content as a reference. Pages are static HTML; changing the JSON does not regenerate them.

## Calculator

The browser implementation is in `assets/black-scholes.js`, with UI wiring in `assets/calculator.js`. No build step, API key or backend is required. The original external Python Gist remains linked on the calculator page; this browser implementation has not been compared with that unavailable source.

Run numerical checks with:

```sh
node --test tests/black-scholes.test.js
```

Inputs: prices in one consistent currency, time in calendar days (365-day basis), and annual rates/volatility/dividend yield as percentages. Output is per unit. Theta is per calendar day; vega and rho are per percentage point. The chart varies the underlying price from 50% to 150% of the current input and holds other parameters fixed.
