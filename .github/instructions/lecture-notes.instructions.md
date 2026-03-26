---
applyTo: "lectures/notes/week*.md"
description: "Use when creating or editing weekly lecture note templates. Enforces the 10-section fillable template structure, emoji hooks, and markdown conventions."
---
# Lecture Note Template Rules

Every lecture note in `lectures/notes/` follows a **fillable template** with exactly 10 sections in this order:

## Required Structure

1. **Title**: `# Week N — Topic Name`
2. **Metadata block** (blockquote): Date, Lecturer (`Heng Rathpisey`), Slides link (`[chN.pdf](../files/chN.pdf)`)
3. **Section 1 — Overview**: One-sentence summary prompt with empty blockquote
4. **Section 2 — Key Concepts & Definitions**: Table with `Term | Definition (in your own words)` columns, cells left blank
5. **Section 3 — Detailed Notes**: Subtopics as `### 3.X Title`. Each subtopic has:
   - A `🎣 Hook:` blockquote with an engaging question
   - `_Notes:_` placeholder
   - A `❓ Questions You Should Be Asking:` blockquote with 3–4 bullet questions
6. **Section 4 — Diagrams & Visuals**: Named diagram placeholders in code blocks
7. **Section 5 — Key Comparisons**: Pre-built comparison tables with empty cells
8. **Section 6 — Examples**: Bullet list of example prompts (Interrupt example, etc.)
9. **Section 7 — Review Questions**: Checkbox list (`- [ ]`) of 4–6 review questions
10. **Section 8 — Connections to Other Topics**: Bullet links to previous/next weeks
11. **Section 9 — Reflection**: Three reflection prompts with empty blockquotes
12. **Section 10 — Summary**: 3–5 sentence summary prompt with empty blockquote

## Formatting Rules

- Use `---` horizontal rules between major sections
- Section numbers are 1-indexed in headings (`## 1. Overview` through `## 10. Summary`)
- Subtopics in Detailed Notes use `### 3.X` numbering
- All content cells in tables are left **blank** — this is a fillable template
- Use emoji: 🎣 for hooks, ❓ for questions, 📝 for notes
- File naming: `week##-topic-slug.md` (zero-padded week number)
- Reference slides as `[chN.pdf](../files/chN.pdf)`

## Do NOT

- Fill in student answers — leave cells and blockquotes empty
- Skip any of the 10 sections
- Use non-standard section ordering
- Add sections not in the template
