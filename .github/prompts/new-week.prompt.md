---
description: "Scaffold a new week's lecture note template pre-filled with the week number, topic, and subtopics"
argument-hint: "Week number and topic, e.g. 13 I/O Systems"
agent: "agent"
---
Create a new weekly lecture note template for this Operating Systems course.

**Input**: The user provides a week number and topic name.

## Steps

1. Read [lectures/notes/README.md](../../lectures/notes/README.md) for the template structure and existing week index.
2. Read an existing note (e.g., `lectures/notes/week01-introduction-to-os.md`) as a structural reference.
3. Check `lectures/notes/` to ensure the week file doesn't already exist.
4. Read [course-outline.md](../../course-outline.md) to find the subtopics and learning objectives for this week.
5. Create `lectures/notes/week##-topic-slug.md` following the exact 10-section template:
   - Title with week number and topic
   - Metadata block (Date blank, Lecturer: Heng Rathpisey, Slides: link to corresponding `chN.pdf`)
   - All 10 sections with appropriate subtopics from the course outline
   - Key Concepts table with relevant terms (cells left blank)
   - Detailed Notes subsections with 🎣 hooks and ❓ question blocks
   - Comparison tables relevant to the topic
   - Review questions as checkbox items
   - Connections linking to adjacent weeks
6. Update the Files table in `lectures/notes/README.md` to include the new week.

## Rules

- File name format: `week##-topic-slug.md` (zero-padded)
- All fill-in cells must be **empty** — this is a student template
- Use 🎣 for hooks, ❓ for questions
- Code blocks must specify language
- Match the exact section structure of existing notes
