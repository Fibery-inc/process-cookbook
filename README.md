# Fibery Process Cookbook

Open recipes for how teams, companies and communities run their work, from Shape Up and OKRs to a phone repair shop or a CS2 team. A recipe is a process in plain words that a person can run from, with the model a builder needs to set it up in any tool. Copy, adapt and build any of them, crediting the cookbook.

## Use a recipe

- **In Fibery:** add the Fibery plugin from [Fibery-inc/skills](https://github.com/Fibery-inc/skills) to your AI agent and name the process ("set up OKRs"): it finds the recipe here by itself, or uses one you attach or link. It asks a few questions, then sets it up in your workspace in about ten minutes.
- **Anywhere else:** give the recipe to your AI assistant and name your tool, or build it by hand from its Details for building.

## Find a recipe

- **On the web:** [processcookbook.org](https://processcookbook.org) has every recipe, with search in your own words and in any language.
- **From an AI agent:** add `https://processcookbook.org/mcp` as a custom connector in Claude, or to any MCP client. Its tools: `find_recipes`, `get_recipe` and `list_domains`. No sign-in.
- **Over HTTP:** `GET https://processcookbook.org/api/search?q=volunteer+cats` returns ranked matches as JSON, `https://processcookbook.org/r/<id>.md` returns one recipe as Markdown, and [processcookbook.org/agents](https://processcookbook.org/agents) has the rest.

## Recipes

<!-- recipes:start -->
18 recipes in 13 domains.

| Domain | Recipes |
|---|---|
| [Arts](recipes/arts/) | [Film study club](recipes/arts/film-study-club.md) |
| [Compliance](recipes/compliance/) | [DORA compliance](recipes/compliance/dora-compliance.md), [NIS2 compliance](recipes/compliance/nis2-compliance.md), [SOC 2 compliance](recipes/compliance/soc-2-compliance.md) |
| [Esports](recipes/esports/) | [CS2 team practice](recipes/esports/cs2-team-practice.md) |
| [Finance](recipes/finance/) | [Purchase requests](recipes/finance/purchase-requests.md), [Venture fund](recipes/finance/venture-fund.md) |
| [Gamedev](recipes/gamedev/) | [Game design docs](recipes/gamedev/game-design-docs.md) |
| [Management](recipes/management/) | [OKRs](recipes/management/okrs.md) |
| [Manufacturing](recipes/manufacturing/) | [Custom fiber mill](recipes/manufacturing/fiber-mill.md), [Custom guitar shop](recipes/manufacturing/custom-guitar-shop.md) |
| [Marketing](recipes/marketing/) | [Content calendar](recipes/marketing/content-calendar.md) |
| [Nonprofit](recipes/nonprofit/) | [TNR program](recipes/nonprofit/tnr-program.md) |
| [Retail](recipes/retail/) | [Phone repair shop](recipes/retail/phone-repair-shop.md) |
| [Sales](recipes/sales/) | [Sales pipeline](recipes/sales/sales-pipeline.md) |
| [Software](recipes/software/) | [Incident management](recipes/software/incident-management.md), [Shape Up](recipes/software/shape-up.md) |
| [Sports](recipes/sports/) | [Grassroots rugby club](recipes/sports/rugby-club.md) |
<!-- recipes:end -->

[index.json](index.json) lists every recipe's header with a raw link to its file here, for agents that read the repository directly.

## What's in a recipe

The first half is for the people who run the process: the idea, one example followed through its whole life, what people look at and when, the rules that run by themselves, what must stay true and what keeps it so, and the questions to decide before setting it up. The second half, Details for building, is for the builder: the records with their fields, states and formulas, the views, any app or reports, and a sample story. It builds on the first half, where the rules and promises are, so a builder reads both. Sources lists the one to three published sources the recipe was written from. [FORMAT.md](FORMAT.md) is the full format.

## Contribute

New recipes and fixes are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[CC BY 4.0](LICENSE). When you reuse a recipe, keep its footer: the credit line names and links the cookbook.
