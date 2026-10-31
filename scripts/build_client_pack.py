#!/usr/bin/env python3
"""Build ONE client-ready PDF from a client-pack markdown file.

Usage:
  python scripts/build_client_pack.py clients/<slug> --init     create the section files to fill in
  python scripts/build_client_pack.py clients/<slug> --status   show what is still missing
  python scripts/build_client_pack.py clients/<slug>            check everything, then build the PDF
  python scripts/build_client_pack.py path/to/client-pack.md [--out report.pdf] [--force]

The client pack is written as small section files in
clients/<slug>/outputs/client-pack/sections/ (copied from templates/client-pack/sections/).
The build joins them in order, refuses to run while any section is missing, empty or
still has [[placeholders]], and then makes the PDF.

On Windows use `py` instead of `python` if `python` is not found.

Needs only:
  - Python 3
  - the 'markdown' package   (pip install markdown)
  - Microsoft Edge or Google Chrome (already installed on most computers)

If no browser is found, an HTML file is written instead and the script tells
you how to save it as PDF (Ctrl+P, Save as PDF).
"""
import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("The 'markdown' package is missing. Run:  pip install markdown")

PLACEHOLDER_RE = re.compile(r"\[\[.*?\]\]|\bTODO\b|\bTBD\b|\bLorem ipsum\b", re.I)
INTERNAL_HINTS = ["clients/", "clients\\", ".agent", "shared/", "SKILL.md", "/new-client",
                  "/win-clients", "/growth-review", "decision-log.md", "outputs/"]


def parse_front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")
    return meta, text[m.end():]


def find_input(arg):
    p = Path(arg)
    if p.is_dir():
        p = p / "outputs" / "client-pack" / "client-pack.md"
    if not p.exists():
        sys.exit(f"Cannot find {p}. Write the client pack first (workflow /client-pack).")
    return p


def check_text(body, force):
    problems = PLACEHOLDER_RE.findall(body)
    warnings = sorted({h for h in INTERNAL_HINTS if h in body})
    if problems:
        print("Leftover placeholders found:", ", ".join(sorted(set(problems))))
        if not force:
            sys.exit("Fix these in client-pack.md (or use --force) and run again.")
    if warnings:
        print("Warning: the text mentions internal items a client should not see:",
              ", ".join(warnings))


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_SECTIONS = ROOT / "templates" / "client-pack" / "sections"
MIN_SECTION_CHARS = 150
DEFERRAL_RE = re.compile(
    r"(to be (determined|decided|provided|supplied)|please (provide|supply)|supply (the|your) (figures|numbers)|"
    r"you (should|must|need to) (choose|decide)|choose (the|your) (first )?(customer|target))", re.I)


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def sections_dir(client):
    return client / "outputs" / "client-pack" / "sections"


def template_names():
    if not TEMPLATE_SECTIONS.is_dir():
        sys.exit(f"Section templates not found: {TEMPLATE_SECTIONS}")
    return sorted(f.name for f in TEMPLATE_SECTIONS.glob("*.md"))


def init_sections(client):
    d = sections_dir(client)
    d.mkdir(parents=True, exist_ok=True)
    made, kept = [], []
    for name in template_names():
        dest = d / name
        if dest.exists():
            kept.append(name)
        else:
            dest.write_text((TEMPLATE_SECTIONS / name).read_text(encoding="utf-8"), encoding="utf-8")
            made.append(name)
    print(f"Sections folder: {d}")
    print(f"Created {len(made)} section file(s); kept {len(kept)} that already existed.")
    print("Now write each file, one at a time, replacing every [[...]] item. Then run with --status.")


def section_report(client):
    """Return a list of (name, state, detail) for every required section."""
    d = sections_dir(client)
    rows = []
    for name in template_names():
        f = d / name
        if not f.exists():
            rows.append((name, "MISSING", "file not created (run --init)"))
            continue
        raw = f.read_text(encoding="utf-8")
        body = strip_comments(raw)
        ph = sorted(set(PLACEHOLDER_RE.findall(body)))
        if ph:
            rows.append((name, "UNFINISHED", f"{len(ph)} placeholder(s), e.g. {ph[0][:60]}"))
            continue
        if not name.startswith("00-"):
            content = re.sub(r"(?m)^#.*$", "", body).strip()
            if len(content) < MIN_SECTION_CHARS:
                rows.append((name, "EMPTY", f"only {len(content)} characters of content"))
                continue
        rows.append((name, "OK", ""))
    return rows


def status(client):
    rows = section_report(client)
    bad = [r for r in rows if r[1] != "OK"]
    for name, state, detail in rows:
        print(f"  {state:<10} {name}  {detail}".rstrip())
    if bad:
        print(f"\n{len(bad)} of {len(rows)} sections still need work. Write them, then run --status again.")
        return False
    print(f"\nAll {len(rows)} sections are complete. Run the build without --status to make the PDF.")
    return True


def assemble(client, force):
    rows = section_report(client)
    bad = [r for r in rows if r[1] != "OK"]
    if bad and not force:
        print("Cannot build yet. These sections need work:")
        for name, state, detail in bad:
            print(f"  {state:<10} {name}  {detail}".rstrip())
        sys.exit("Fix them (see --status) and run again.")
    d = sections_dir(client)
    texts = [strip_comments((d / n).read_text(encoding="utf-8")).strip() for n in template_names()]
    meta, first_body = parse_front_matter(texts[0] + "\n")
    body_md = "\n\n".join([first_body.strip()] + texts[1:] if first_body.strip() else texts[1:])
    pack = client / "outputs" / "client-pack"
    src = pack / "client-pack.md"
    fm = "\n".join(f"{k}: {v}" for k, v in meta.items())
    src.write_text(f"---\n{fm}\n---\n\n{body_md}\n", encoding="utf-8")
    scan = re.sub(r"\]\(https?://[^)]*\)", "]", body_md)  # ignore web addresses
    warn = sorted({h for h in INTERNAL_HINTS if h in scan})
    if warn:
        print("Warning: the text mentions internal items a client should not see:", ", ".join(warn))
    for line in sorted({m.group(0) for m in DEFERRAL_RE.finditer(body_md)}):
        print(f"Warning: wording that hands work back to the client: '{line}'. Replace it with an answer.")
    prospects = [f for f in template_names() if "prospects" in f]
    if prospects:
        txt = strip_comments((d / prospects[0]).read_text(encoding="utf-8"))
        n = len(re.findall(r"(?m)^\|\s*\d+\s*\|", txt))
        if n < 30:
            print(f"Warning: only {n} numbered prospect rows found; the standard is 30 or more named, sourced prospects.")
    return src, meta, body_md


def tag_labels(html_text):
    """Turn VERIFIED / ESTIMATE / ASSUMPTION words into small coloured tags (text only)."""
    def repl(m):
        w = m.group(1)
        return f'<span class="tag {w.lower()}">{w}</span>'
    parts = re.split(r"(<[^>]+>)", html_text)
    for i, part in enumerate(parts):
        if not part.startswith("<"):
            parts[i] = re.sub(r"\b(VERIFIED|ESTIMATE|ASSUMPTION)\b", repl, part)
    return "".join(parts)


def keep_together(html_text):
    """Stop dates (2027-01-23) and IDs (D-001) from breaking across lines in narrow table cells."""
    pat = re.compile(r"\b(\d{4}-\d{2}-\d{2}|[A-Z]-\d{2,3})\b")
    parts = re.split(r"(<[^>]+>)", html_text)
    for i, part in enumerate(parts):
        if not part.startswith("<"):
            parts[i] = pat.sub(r'<span class="nb">\1</span>', part)
    return "".join(parts)


def css_string(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_html(meta, body_md):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    body = md.convert(body_md)
    # section titles for the contents list on the cover
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    # page break before the first section and before appendices
    first = [True]
    appendix_seen = [False]

    def h1_class(m):
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        cls = ""
        is_appendix = bool(re.match(r"(appendix|appendices)\b", title, re.I))
        # new page before the first section and before the first appendix only
        if first[0] or (is_appendix and not appendix_seen[0]):
            cls = ' class="pb"'
        if is_appendix:
            appendix_seen[0] = True
        first[0] = False
        return f"<h1{cls}>{m.group(1)}</h1>"
    body = re.sub(r"<h1[^>]*>(.*?)</h1>", h1_class, body, flags=re.S)
    body = tag_labels(body)
    body = keep_together(body)

    title = meta.get("title", "Business Growth Plan")
    client = meta.get("client", "")
    prepared_for = meta.get("prepared_for", "")
    prepared_by = meta.get("prepared_by", "")
    d = meta.get("date", date.today().isoformat())
    version = meta.get("version", "1.0")
    conf = meta.get("confidential", "true").lower() != "false"
    footer_left = f"{client} - {'Confidential' if conf else title}".strip(" -")

    contents = "".join(f"<li>{re.sub(r'<[^>]+>', '', t).strip()}</li>" for t in h1s)
    meta_rows = ""
    for label, val in (("Prepared for", prepared_for), ("Prepared by", prepared_by),
                       ("Date", d), ("Version", version)):
        if val:
            meta_rows += f"<tr><th>{html.escape(label)}</th><td>{html.escape(val)}</td></tr>"

    css = """
    :root { --accent:#1F4E79; --ink:#1b1f24; --muted:#5b6670; --line:#d0d7de; --soft:#f3f6f9; }
    @page { size: A4; margin: 20mm 17mm 22mm 17mm;
            @bottom-left { content: "__FOOTER__"; font: 8pt 'Segoe UI', Arial, sans-serif; color:#5b6670; }
            @bottom-right { content: "Page " counter(page) " of " counter(pages);
                            font: 8pt 'Segoe UI', Arial, sans-serif; color:#5b6670; } }
    @page :first { margin: 0; @bottom-left { content: none; } @bottom-right { content: none; } }
    * { box-sizing: border-box; }
    html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    body { font: 10.5pt/1.5 'Segoe UI','Helvetica Neue',Arial,'Noto Sans',sans-serif; color: var(--ink); margin:0; }
    .cover { height: 297mm; padding: 38mm 22mm 20mm 22mm; page-break-after: always; border-top: 14mm solid var(--accent); }
    .cover .kicker { color: var(--accent); font-weight: 600; letter-spacing: .08em; text-transform: uppercase; font-size: 10pt; }
    .cover h1.title { font-size: 30pt; line-height: 1.15; margin: 6mm 0 3mm; color: var(--ink); border:0; padding:0; }
    .cover .client { font-size: 15pt; color: var(--muted); margin-bottom: 14mm; }
    .cover table { width: auto; border: 0; margin: 0 0 14mm; font-size: 10.5pt; }
    .cover th { background: none; color: var(--muted); font-weight: 600; text-align:left; border:0; padding: 1.5mm 8mm 1.5mm 0; }
    .cover td { border:0; padding: 1.5mm 0; background:none; }
    .cover h2.toc { font-size: 11pt; color: var(--accent); margin: 0 0 2mm; border:0; text-transform: uppercase; letter-spacing:.06em; }
    .cover ol { margin: 0; padding-left: 0; list-style: none; color: var(--ink); columns: 2; column-gap: 12mm; font-size: 10pt; }
    .cover li { break-inside: avoid; }
    .nb { white-space: nowrap; }
    .cover .conf { position:absolute; left:22mm; right:22mm; bottom:16mm; font-size: 8.5pt; color: var(--muted); border-top:1px solid var(--line); padding-top:3mm; }
    h1 { font-size: 18pt; color: var(--accent); margin: 10mm 0 3mm; padding-bottom: 2mm; border-bottom: 2px solid var(--accent); break-after: avoid; }
    h1.pb { break-before: page; margin-top: 0; }
    h2 { font-size: 13pt; color: var(--ink); margin: 7mm 0 2mm; break-after: avoid; }
    h3 { font-size: 11pt; color: var(--accent); margin: 5mm 0 1.5mm; break-after: avoid; }
    p { margin: 0 0 3mm; orphans: 3; widows: 3; }
    ul, ol { margin: 0 0 3mm; padding-left: 6mm; }
    li { margin-bottom: 1mm; }
    table { border-collapse: collapse; width: 100%; margin: 2mm 0 5mm; font-size: 9pt; }
    thead { display: table-header-group; }
    tr { break-inside: avoid; }
    th { background: var(--accent); color: #fff; text-align: left; padding: 2mm 2.5mm; font-weight: 600; border: 1px solid var(--accent); }
    td { padding: 1.8mm 2.5mm; border: 1px solid var(--line); vertical-align: top; }
    tbody tr:nth-child(even) td { background: var(--soft); }
    blockquote { margin: 3mm 0; padding: 2.5mm 4mm; background: var(--soft); border-left: 3px solid var(--accent); color: var(--ink); }
    blockquote p { margin: 0; }
    code, pre { font-family: Consolas, 'Courier New', monospace; font-size: 9pt; background: var(--soft); }
    pre { padding: 3mm; border: 1px solid var(--line); white-space: pre-wrap; }
    a { color: var(--accent); word-break: break-word; }
    hr { border: 0; border-top: 1px solid var(--line); margin: 5mm 0; }
    .tag { display:inline-block; font-size: 7.5pt; font-weight: 700; padding: 0 1.6mm; border-radius: 2mm; letter-spacing: .03em; white-space: nowrap; }
    .tag.verified { background:#dff3e4; color:#14532d; }
    .tag.estimate { background:#fdf0cf; color:#7a4b00; }
    .tag.assumption { background:#fde2e0; color:#8a1c14; }
    """.replace("__FOOTER__", css_string(footer_left))

    conf_note = ("This document is confidential and prepared only for the named recipient. "
                 "It is decision support, not legal, tax, or financial advice. Have a qualified "
                 "professional confirm any legal, tax, or financial point before you act on it."
                 if conf else "")
    cover = f"""
    <section class="cover">
      <div class="kicker">{html.escape(client or 'Business plan')}</div>
      <h1 class="title">{html.escape(title)}</h1>
      <div class="client">{html.escape(client)}</div>
      <table>{meta_rows}</table>
      <h2 class="toc">Contents</h2>
      <ol>{contents}</ol>
      <div class="conf">{html.escape(conf_note)}</div>
    </section>"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)} - {html.escape(client)}</title>
<style>{css}</style></head><body>{cover}{body}</body></html>"""


def find_browser(explicit=None):
    cands = []
    if explicit:
        cands.append(explicit)
    if os.environ.get("BROWSER_PATH"):
        cands.append(os.environ["BROWSER_PATH"])
    local = os.environ.get("LOCALAPPDATA", "")
    cands += [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.join(local, r"Google\Chrome\Application\chrome.exe") if local else "",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "microsoft-edge", "microsoft-edge-stable", "msedge", "chrome"):
        w = shutil.which(name)
        if w:
            cands.append(w)
    for c in cands:
        if c and Path(c).exists():
            return c
    return None


def page_count(pdf):
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf)).pages)
    except Exception:
        data = Path(pdf).read_bytes()
        return len(re.findall(rb"/Type\s*/Page[^s]", data)) or None


def main():
    ap = argparse.ArgumentParser(description="Build one client-ready PDF from client-pack.md")
    ap.add_argument("source", nargs="?", help="client folder (clients/<slug>) or a client-pack .md file; leave out to use the active client")
    ap.add_argument("--out", help="output PDF path")
    ap.add_argument("--browser", help="path to Edge or Chrome")
    ap.add_argument("--force", action="store_true", help="build even if placeholders remain")
    ap.add_argument("--init", action="store_true", help="create the section files for this client")
    ap.add_argument("--status", action="store_true", help="show which sections still need work")
    args = ap.parse_args()

    if not args.source:
        active_file = ROOT / "clients" / "ACTIVE"
        if not active_file.exists() or not active_file.read_text(encoding="utf-8").strip():
            sys.exit("No active client. Give the client folder, for example: clients/my-client")
        args.source = str(ROOT / "clients" / active_file.read_text(encoding="utf-8").strip())
        print(f"Using the active client: {args.source}")
    target = Path(args.source)
    if args.init:
        if not target.is_dir():
            sys.exit("--init needs a client folder, for example clients/my-client")
        init_sections(target)
        return
    if args.status:
        if not target.is_dir():
            sys.exit("--status needs a client folder, for example clients/my-client")
        sys.exit(0 if status(target) else 1)
    if target.is_dir() and sections_dir(target).is_dir():
        src, meta, body_md = assemble(target, args.force)
    else:
        src = find_input(args.source)
        meta, body_md = parse_front_matter(strip_comments(src.read_text(encoding="utf-8")))
        check_text(body_md, args.force)

    slug = re.sub(r"[^a-z0-9]+", "-", (meta.get("client") or src.parent.parent.parent.name).lower()).strip("-")
    stamp = meta.get("date", date.today().isoformat())
    out = Path(args.out) if args.out else src.parent / f"{slug}-client-pack-{stamp}.pdf"
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    page_html = build_html(meta, body_md)
    html_path = src.parent / "client-pack.html"
    html_path.write_text(page_html, encoding="utf-8")

    browser = find_browser(args.browser)
    if not browser:
        print(f"No Edge or Chrome found. A web page was saved instead:\n  {html_path}\n"
              "Open it in any browser, press Ctrl+P, choose 'Save as PDF', and tick 'Background graphics'.")
        sys.exit(2)

    prof = tempfile.mkdtemp(prefix="client-pack-")  # removed in the finally block; Edge can hold it briefly on Windows
    try:
        cmd = [browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
               "--disable-background-networking", "--disable-component-update", "--disable-sync",
               "--disable-extensions", "--no-first-run", "--no-default-browser-check",
               "--disable-features=OptimizationHints,MediaRouter,Translate",
               f"--user-data-dir={prof}", f"--print-to-pdf={out}",
               "--run-all-compositor-stages-before-draw", html_path.resolve().as_uri()]
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            cmd.insert(2, "--no-sandbox")
        try:
            subprocess.run(cmd, check=True, timeout=180, capture_output=True)
        except subprocess.CalledProcessError as e:
            sys.exit(f"The browser could not make the PDF:\n{e.stderr.decode(errors='ignore')[-600:]}")
        except subprocess.TimeoutExpired:
            sys.exit("The browser took too long. Close other Edge/Chrome windows and try again.")
    finally:
        shutil.rmtree(prof, ignore_errors=True)

    if not out.exists() or out.stat().st_size == 0:
        sys.exit("No PDF was created. Try --browser <path to Edge or Chrome>.")
    try:
        html_path.unlink()
    except OSError:
        pass
    n = page_count(out)
    print(f"PDF ready: {out}" + (f"  ({n} pages)" if n else ""))


if __name__ == "__main__":
    main()
