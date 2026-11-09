# Init Prompt — Shopify Dev Tool

Copy and paste this as your first message when starting a Shopify theme session.

---

## For Claude Code (recommended)

Place `AGENTS.md` and `identity.md` in your Shopify theme project root. Claude Code loads them automatically on project open.

Then start with:

```
I'm working on a Shopify Online Store 2.0 theme for [client name].
Theme: [Dawn / custom / other]
Shopify plan: [Standard / Plus]
Task: [what you need built]
```

---

## For any LLM chat (Claude, ChatGPT, etc.)

Upload both files before sending this prompt:

> Upload: `identity.md` + `AGENTS.md`

```
I'm uploading 2 files for a Shopify theme development session.

- identity.md — your role, Coalition standards, hard rules, output format, QA checklist
- AGENTS.md — complete Shopify theme reference: architecture, Liquid, schema, CSS/JS, translation standards, and working examples

Read both files fully. Apply all rules from identity.md. Use AGENTS.md as your technical reference — treat it as ground truth for Shopify Liquid patterns.

Do not invent Liquid filters, objects, or schema properties — if unsure, flag it.

Ready when you are.
```

---

## Giving context (always include these)

After the init prompt, tell the agent:

- **Theme base**: Dawn, custom, or other (affects what's already available)
- **Shopify plan**: Standard or Plus (affects what features are available natively)
- **What to build**: be specific — "a featured collection section with heading, description, product grid (4 cols desktop / 2 mobile), and a CTA button"
- **Design reference**: Figma link, screenshot, or reference site if available

---

## Tips

- The more specific your request, the better the output — include layout, columns, settings you want in the customizer, and any conditional logic
- Ask for one component at a time — sections, blocks, and snippets separately if they're large
- After each output, verify the schema JSON before pasting into your theme — schema bugs are silent until the theme editor breaks
- If the agent hallucinates a Liquid filter, cross-check against Shopify Liquid reference docs
