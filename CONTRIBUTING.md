# Contributing

One recipe per pull request: a new recipe, or a revision of one.

## Write it

- Follow [FORMAT.md](FORMAT.md). The easiest way is the recipe-writer skill from [Fibery-inc/skills](https://github.com/Fibery-inc/skills): ask it for one ("make a recipe for our purchase approvals") and answer its questions.
- Write in your own words. A recipe can credit a method's originator and link one source, but never copies a source's sentences, tables or diagrams.
- Invent every example: no real people, customers or records.

## Put it in place

- Save it as `recipes/<domain>/<id>.md`, where `<domain>` is the header's `domain` and `<id>` is the recipe's name in lowercase with hyphens (`sales-pipeline`). The id is unique across the cookbook and never changes, because people link to recipes by it.
- A revision keeps the id and raises `version` by one when the model changes (a database, a field, a state, a rule), never for wording.

## Check it

```
pip install pyyaml
python scripts/check.py
python scripts/build_index.py
```

check.py checks the header, the place, the fixed texts and the section order. build_index.py rebuilds index.json, the domain lists and the table in the README; commit what it changes. CI runs both on every pull request.

## License

By contributing, you license your recipe under CC BY 4.0, like the rest of the cookbook.
