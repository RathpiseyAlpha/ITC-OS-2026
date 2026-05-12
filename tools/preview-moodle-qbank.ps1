param(
    [string]$InputDir = "moodle-qbanks",
    [string]$OutputFile = "moodle-qbanks\preview.html"
)

function HtmlEncode($value) {
    if ($null -eq $value) { return "" }
    return [System.Net.WebUtility]::HtmlEncode([string]$value)
}

function NodeText($node) {
    if ($null -eq $node) { return "" }
    if ($node -is [string]) { return $node }
    return $node.InnerText
}

function RenderText($textNode, $format) {
    $text = NodeText $textNode
    if ([string]::IsNullOrWhiteSpace($text)) {
        return "<p class=`"muted`">No question text.</p>"
    }

    if ($format -eq "html") {
        return $text
    }

    return "<p>$((HtmlEncode $text) -replace "`r?`n", "<br>")</p>"
}

function RenderAnswerList($answers) {
    if ($null -eq $answers) { return "" }

    $items = @()
    foreach ($answer in $answers) {
        $fraction = 0
        if ($answer.fraction) {
            [void][double]::TryParse([string]$answer.fraction, [ref]$fraction)
        }

        $class = if ($fraction -gt 0) { "answer correct" } else { "answer" }
        $badge = if ($fraction -gt 0) { "<span class=`"badge correct-badge`">$fraction%</span>" } else { "<span class=`"badge`">$fraction%</span>" }
        $text = RenderText $answer.text $answer.format
        $items += "<li class=`"$class`">$badge<div class=`"answer-text`">$text</div></li>"
    }

    if ($items.Count -eq 0) { return "" }
    return "<ol class=`"answers`">$($items -join "`n")</ol>"
}

function RenderSubquestions($question) {
    if ($null -eq $question.subquestion) { return "" }

    $rows = @()
    foreach ($subquestion in $question.subquestion) {
        $prompt = HtmlEncode (NodeText $subquestion.text)
        $answer = HtmlEncode (NodeText $subquestion.answer.text)
        $rows += "<tr><td>$prompt</td><td>$answer</td></tr>"
    }

    if ($rows.Count -eq 0) { return "" }
    return @"
<table class="pairs">
  <thead><tr><th>Prompt</th><th>Correct match</th></tr></thead>
  <tbody>$($rows -join "`n")</tbody>
</table>
"@
}

function RenderDragboxes($question) {
    if ($null -eq $question.dragbox) { return "" }

    $items = @()
    $index = 1
    foreach ($dragbox in $question.dragbox) {
        $text = HtmlEncode (NodeText $dragbox.text)
        $group = HtmlEncode (NodeText $dragbox.group)
        $items += "<li><span class=`"choice-number`">$index</span> $text <span class=`"muted`">(group $group)</span></li>"
        $index++
    }

    if ($items.Count -eq 0) { return "" }
    return "<h4>Drag choices</h4><ul class=`"dragboxes`">$($items -join "`n")</ul>"
}

function RenderQuestion($question, $fileName, $index, $category) {
    $type = HtmlEncode $question.type
    $name = HtmlEncode (NodeText $question.name.text)
    $prompt = RenderText $question.questiontext.text $question.questiontext.format
    $answers = RenderAnswerList $question.answer
    $pairs = RenderSubquestions $question
    $dragboxes = RenderDragboxes $question
    $grade = HtmlEncode (NodeText $question.defaultgrade)

    return @"
<article class="question" data-type="$type">
  <header>
    <div>
      <h3>$index. $name</h3>
      <p class="meta">$type · grade $grade · $fileName</p>
    </div>
    <span class="type">$type</span>
  </header>
  <p class="category">$category</p>
  <section class="prompt">$prompt</section>
  $answers
  $pairs
  $dragboxes
</article>
"@
}

$inputPath = Resolve-Path -LiteralPath $InputDir
$files = Get-ChildItem -LiteralPath $inputPath -Filter "*.xml" | Sort-Object Name

$sections = @()
$total = 0
$typeCounts = @{}

foreach ($file in $files) {
    [xml]$xml = Get-Content -Raw -LiteralPath $file.FullName
    $category = "Uncategorized"
    $questionsHtml = @()
    $fileQuestionCount = 0

    foreach ($question in $xml.quiz.question) {
        if ($question.type -eq "category") {
            $category = HtmlEncode (NodeText $question.category.text)
            continue
        }

        $fileQuestionCount++
        $total++
        $type = [string]$question.type
        if (-not $typeCounts.ContainsKey($type)) { $typeCounts[$type] = 0 }
        $typeCounts[$type]++
        $questionsHtml += RenderQuestion $question (HtmlEncode $file.Name) $fileQuestionCount $category
    }

    $sections += @"
<section class="file-section">
  <h2>$((HtmlEncode $file.Name)) <span>$fileQuestionCount questions</span></h2>
  $($questionsHtml -join "`n")
</section>
"@
}

$typeSummary = ($typeCounts.GetEnumerator() | Sort-Object Name | ForEach-Object {
    "<span class=`"summary-pill`">$((HtmlEncode $_.Key)): $($_.Value)</span>"
}) -join "`n"

$generatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$html = @"
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Moodle Question Bank Preview</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #172026;
      --muted: #66717a;
      --line: #d9e1e7;
      --surface: #ffffff;
      --band: #f3f6f8;
      --accent: #145c6b;
      --good: #18743a;
      --good-bg: #e9f7ee;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: var(--band);
      line-height: 1.45;
    }
    .topbar {
      position: sticky;
      top: 0;
      z-index: 5;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
      padding: 14px 24px;
    }
    .topbar h1 {
      margin: 0 0 8px;
      font-size: 22px;
    }
    .summary {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      color: var(--muted);
      font-size: 14px;
    }
    .summary-pill, .type, .badge {
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 3px 8px;
      background: #fff;
      white-space: nowrap;
    }
    main {
      max-width: 1120px;
      margin: 0 auto;
      padding: 20px;
    }
    .file-section {
      margin: 0 0 28px;
    }
    .file-section h2 {
      font-size: 18px;
      margin: 22px 0 12px;
      color: var(--accent);
    }
    .file-section h2 span {
      font-size: 13px;
      font-weight: normal;
      color: var(--muted);
    }
    .question {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      margin: 12px 0;
    }
    .question header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
      border-bottom: 1px solid var(--line);
      padding-bottom: 10px;
      margin-bottom: 10px;
    }
    .question h3 {
      margin: 0;
      font-size: 17px;
    }
    .meta, .category, .muted {
      color: var(--muted);
      font-size: 13px;
    }
    .category {
      margin: 0 0 10px;
      word-break: break-word;
    }
    .prompt {
      margin: 10px 0;
    }
    .prompt table {
      width: 100%;
      border-collapse: collapse;
    }
    .prompt td, .prompt th, .pairs td, .pairs th {
      border: 1px solid var(--line);
      padding: 8px;
      vertical-align: top;
    }
    .answers {
      padding-left: 22px;
      margin: 12px 0 0;
    }
    .answer {
      margin: 8px 0;
      padding: 8px;
      border: 1px solid var(--line);
      border-radius: 6px;
    }
    .answer.correct {
      border-color: #9bd5ad;
      background: var(--good-bg);
    }
    .correct-badge {
      color: #fff;
      background: var(--good);
      border-color: var(--good);
    }
    .answer-text {
      display: inline-block;
      margin-left: 8px;
      max-width: calc(100% - 72px);
      vertical-align: top;
    }
    .answer-text p {
      margin: 0;
    }
    .pairs {
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      background: #fff;
    }
    .dragboxes {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px;
      list-style: none;
      padding: 0;
    }
    .dragboxes li {
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 8px;
      background: #fff;
    }
    .choice-number {
      display: inline-block;
      min-width: 24px;
      color: var(--accent);
      font-weight: bold;
    }
    pre {
      white-space: pre-wrap;
    }
    @media print {
      .topbar { position: static; }
      .question { break-inside: avoid; }
    }
  </style>
</head>
<body>
  <div class="topbar">
    <h1>Moodle Question Bank Preview</h1>
    <div class="summary">
      <span>$total questions</span>
      <span>Generated $generatedAt</span>
      $typeSummary
    </div>
  </div>
  <main>
    $($sections -join "`n")
  </main>
</body>
</html>
"@

$outputPath = Join-Path (Get-Location) $OutputFile
Set-Content -LiteralPath $outputPath -Value $html -Encoding UTF8
Write-Output "Wrote $outputPath"
Write-Output "Questions: $total"
