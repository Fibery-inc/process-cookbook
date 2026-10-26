import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
KEYS = ["title", "summary", "domain", "for", "roles", "needs", "keywords", "version", "license"]
FOR = {"solo", "team", "company", "community"}
SECTIONS = ["The idea", "How it runs", "What people look at", "The rules", "What must stay true",
            "Making it yours", "Details for building", "Sources", "Build it"]
ITALIC = "*A recipe from the Fibery Process Cookbook: the process in plain words, and the model to build it in any tool.*"
OPENERS = {
    "The rules": "These are all the automations; everything else in the story is done by people.",
    "What must stay true": "Whatever anyone edits, adapts or corrects, these hold; each says what keeps it so.",
    "Making it yours": "Decide these before you set it up; each has a default if you shrug.",
    "Details for building": "What follows is what the process is built from, in words any tool can follow; the story above is enough to run it.",
}
RULES_CLOSE = "No automations in your tool? Then a person does each of these at the same moment, and the promises they keep below become practices."
GLOSSARY = re.compile(
    r"Each kind of record \([^)]+\) is a database or a table, depending on the tool, or a tab in a spreadsheet\. "
    r"A relation links two kinds; its inverse is the name it has on the other side\. "
    r"A state is a step in a workflow, and a finished state ends it\. "
    r"A rule is an automation, a button is an automation someone presses, and a formula is a field the tool computes\. "
    r"A nested view shows each record's children beneath it; where a tool can't nest, group the children by their parent instead\."
)
BUILD = re.compile(
    r'In Fibery, open Claude with the Fibery plugin, attach this recipe and say "set up [^"]+"\. '
    r"Claude asks a few questions, then sets it up in about ten minutes\.\n\n"
    r"Anywhere else, give this recipe to your AI assistant and name your tool, or build it by hand from Details for building\."
)
CREDIT = "From the Fibery Process Cookbook (https://github.com/Fibery-inc/process-cookbook), licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/): copy, adapt and build it anywhere, crediting the cookbook.*"
TOOL_WORDS = re.compile(r"\bFibery\b|\b[Ww]orkspaces?\b|\bSpaces?\b")
ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NOT_DATABASES = {"Views", "App", "Reports", "Sample story"}
STEP = re.compile(r"^(\d+)\. (.*)")
PROMISE = re.compile(r"^- (.*)")
TITLE = re.compile(r"\*\*(.+?)\*\*(.*)", re.S)
SENTENCE_END = re.compile(r"[.!?][\"')\]*_]*(?=\s|$)")
KEEPER = re.compile(r"(?:^|[.!?][\"')\]*_]*\s+)(?:Kept by|Shown on|A practice)\b")


def domains():
    found = re.search(r"\*\*Domains\.\*\* (.+?)\. A process", (ROOT / "FORMAT.md").read_text(encoding="utf-8"))
    return set(found.group(1).split(", ")) if found else set()


def sections(body):
    preamble, parts, order, name, fence = [], {}, [], None, False
    for line in body.split("\n"):
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            name = line[3:].strip()
            order.append(name)
            parts[name] = []
            continue
        (parts[name] if name else preamble).append(line)
    return "\n".join(preamble), order, {k: "\n".join(v) for k, v in parts.items()}


def subsection(text, title):
    found = re.search(rf"^### {re.escape(title)}\n(.*?)(?=^### |\Z)", text, re.M | re.S)
    return found.group(1).strip() if found else None


def entries(text, pattern):
    found, open_item = [], False
    for line in text.split("\n"):
        head = pattern.match(line)
        if head:
            found.append(list(head.groups()))
            open_item = True
        elif open_item and line.strip():
            found[-1][-1] += " " + line.strip()
        else:
            open_item = False
    return found


def first_sentence(text):
    text = text.strip()
    end = SENTENCE_END.search(text)
    return text[:end.end()] if end else text


def words(text):
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return len([w for w in re.sub(r"[*_`]", "", text).split() if re.search(r"\w", w)])


def check(path, known, errors, warnings):
    rel = path.relative_to(ROOT).as_posix()

    def err(message):
        errors.append(f"{rel}: {message}")

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---") < 2:
        err("no YAML header")
        return
    _, head, body = text.split("---", 2)
    try:
        meta = yaml.safe_load(head) or {}
    except yaml.YAMLError as e:
        err(f"the header isn't valid YAML: {e}")
        return
    missing, extra = [k for k in KEYS if k not in meta], [str(k) for k in meta if k not in KEYS]
    if missing:
        err("the header lacks " + ", ".join(missing))
    if extra:
        err("the header has keys the format doesn't: " + ", ".join(extra))
    title = meta.get("title")
    if not isinstance(title, str) or not title:
        err("title must be text")
    summary = meta.get("summary")
    if not isinstance(summary, str) or not summary or len(summary) >= 160:
        err("summary must be one sentence under 160 characters")
    if meta.get("domain") not in known:
        err(f"domain {meta.get('domain')!r} isn't in FORMAT.md's list")
    elif path.parent.name != meta["domain"]:
        err(f"it's in recipes/{path.parent.name}/ but its domain is {meta['domain']}")
    if meta.get("for") not in FOR:
        err("for must be solo, team, company or community")
    for key in ("roles", "needs"):
        value = meta.get(key)
        if key in meta and (not isinstance(value, str) or not value.strip() or len(value) >= 160):
            err(f"{key} must be one sentence under 160 characters")
    keywords = meta.get("keywords")
    if not isinstance(keywords, list) or not keywords or not all(isinstance(k, str) for k in keywords):
        err("keywords must be a list of words")
    version = meta.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        err("version must be a whole number from 1")
    if meta.get("license") != "CC-BY-4.0":
        err("license must be CC-BY-4.0")

    preamble, order, secs = sections(body)
    if preamble.strip().split("\n")[0] != f"# {title}":
        err("the first line after the header must be '# <title>'")
    if ITALIC not in preamble:
        err("the fixed italic line under the title is missing")
    if order != SECTIONS:
        err("the sections must be, in order: " + "; ".join(SECTIONS) + ". Found: " + "; ".join(order))
    for name, opener in OPENERS.items():
        if name in secs and opener not in secs[name]:
            err(f"{name} lacks its fixed opening line")
    if "The rules" in secs and RULES_CLOSE not in secs["The rules"]:
        err("The rules lacks its fixed closing line")
    if "The idea" in secs and "In any work tool, this becomes" not in secs["The idea"]:
        err("The idea lacks its 'In any work tool, this becomes…' paragraph")
    for number, step in entries(secs.get("How it runs", ""), STEP):
        opening = TITLE.match(step)
        if not opening or not opening.group(1).rstrip().endswith((".", "!", "?")):
            err(f"How it runs, step {number}: it must open with a bold title that is a sentence, ending in a period")
            continue
        count = words(first_sentence(opening.group(2)))
        if count >= 25:
            warnings.append(f"{rel}: How it runs, step {number}: the first sentence after the title has {count} words;"
                            " the format asks for under 25")
    for (promise,) in entries(secs.get("What must stay true", ""), PROMISE):
        promise = promise.lstrip("★ ")
        if not KEEPER.search(promise):
            warnings.append(f"{rel}: What must stay true: no sentence starts with Kept by, Shown on or A practice"
                            f" in '{promise[:60]}…'")
    details = secs.get("Details for building", "")
    if details:
        for name, content in re.findall(r"^### ([^\n]+)\n(.*?)(?=^### |\Z)", details, re.M | re.S):
            if name.strip() in NOT_DATABASES:
                continue
            count = words(first_sentence(content.strip().split("\n\n")[0]))
            if count >= 12:
                warnings.append(f"{rel}: Details for building, {name.strip()}: the first sentence has {count} words;"
                                " the format asks for under twelve, saying what one record is")
        if not GLOSSARY.search(details):
            err("Details for building lacks its fixed paragraph")
        if not re.search(r"```mermaid\s*\nerDiagram", details):
            err("Details for building lacks the Mermaid erDiagram")
        story = subsection(details, "Sample story")
        if not story:
            err("Details for building lacks the Sample story")
        elif any(line.lstrip().startswith(("|", "- ", "* ")) for line in story.split("\n")):
            err("the sample story is a table or a list; the format asks for one paragraph")
        elif len([p for p in story.split("\n\n") if p.strip()]) != 1:
            err("the sample story must be one paragraph")
        elif len(story.split()) >= 120:
            warnings.append(f"{rel}: the sample story has {len(story.split())} words; the format asks for under 120")
    if "Build it" in secs and not BUILD.search(secs["Build it"]):
        err("Build it lacks its two fixed paragraphs")
    if "Sources" in secs:
        items = [line for line in secs["Sources"].split("\n") if line.startswith("- ")]
        if not 1 <= len(items) <= 3:
            err(f"Sources lists {len(items)} sources; the format asks for one to three")
        for item in items:
            if not re.search(r"\]\(https?://", item):
                err(f"a source has no link: {item[:60]}")
    if re.search(r"\bSource: ", preamble):
        err("the promise line names a source; sources go in Sources")
    if not text.rstrip().endswith(CREDIT):
        err("the file must end with the cookbook's credit line")
    neutral = "\n".join([head, preamble.replace(ITALIC, "")] + [secs[n] for n in order if n not in ("Build it", "Sources")])
    for word in sorted(set(TOOL_WORDS.findall(neutral))):
        err(f"names {word!r} outside the fixed texts; a recipe names no tool")


def main():
    known = domains()
    errors, warnings, seen = [], [], {}
    if not known:
        errors.append("FORMAT.md: no **Domains.** line to read the domain list from")
    for path in sorted(RECIPES.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if path.parent.parent != RECIPES:
            errors.append(f"{rel}: a recipe lives at recipes/<domain>/<id>.md")
            continue
        if path.name == "README.md":
            continue
        if not ID.match(path.stem):
            errors.append(f"{rel}: the file name is the id, in lowercase letters, digits and hyphens")
        if path.stem in seen:
            errors.append(f"{rel}: the id {path.stem} is taken by {seen[path.stem]}")
        seen[path.stem] = rel
        check(path, known, errors, warnings)
    for line in warnings:
        print("warning: " + line)
    for line in errors:
        print(line)
    print(f"{len(seen)} recipes, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
