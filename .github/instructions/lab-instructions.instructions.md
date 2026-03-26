---
applyTo: "labs/**/lab*-instruction.md"
description: "Use when creating or editing lab instruction files. Enforces the metadata table, objectives list, task structure, and submission conventions."
---
# Lab Instruction Rules

Every lab instruction file follows a consistent structure:

## Required Structure

1. **Title**: `# OS Lab N — Topic (Hands-on)`
2. **Metadata table** (immediately after title):
   ```
   | | |
   |---|---|
   | **Course** | Operating Systems |
   | **Lab Title** | <descriptive title> |
   | **Chapter** | <related lecture topic> |
   | **Duration** | <N> Hours |
   | **Lab Type** | Individual |
   ```
3. **Lab Objectives**: Numbered list starting with "After completing this lab, students will be able to:"
4. **Lab Setup**: Folder structure creation with `mkdir -p` using `<YourStudentID>` placeholder
5. **Documenting Your Work**: Screenshot instructions and workflow explanation
6. **Lab Workflow Overview**: ASCII diagram showing task flow from start to submission
7. **Tasks**: Each task as a `## Task N — Title` section with:
   - Brief intro explaining the purpose
   - Numbered steps with code blocks (language-tagged: `bash`, `c`, `python`)
   - Bash examples use `$` prefix
   - Expected output shown in separate blocks
8. **Submission instructions**: Git push steps and README documentation

## Formatting Rules

- Use `---` horizontal rules between major sections
- Code blocks always specify language
- Bash commands use `$` prefix: `$ uname -a`
- Student ID placeholder: `<YourStudentID>`
- Lab folder pattern: `os-se-<YourStudentID>/os-lab-<YourStudentID>/labN`
- Include ASCII workflow diagrams using box-drawing characters
- Screenshots referenced as `![description](path/to/image.png)`

## Do NOT

- Skip the metadata table
- Use code blocks without language identifiers
- Omit the folder structure setup section
- Write commands without `$` prefix in bash blocks
