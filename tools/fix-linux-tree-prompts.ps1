function Set-NodeHtmlText($node, [string]$html) {
    if ($null -eq $node) { return }
    while ($node.HasChildNodes) {
        [void]$node.RemoveChild($node.FirstChild)
    }
    $cdata = $node.OwnerDocument.CreateCDataSection($html)
    [void]$node.AppendChild($cdata)
}

function Get-Question($xml, [string]$name) {
    return $xml.quiz.question | Where-Object { $_.type -ne "category" -and $_.name.text -eq $name } | Select-Object -First 1
}

$tree = @"
<p><code>/home/user/</code><br>
<code>|-- Documents/</code><br>
<code>|   |-- Work/</code><br>
<code>|   |   |-- Projects/</code><br>
<code>|   |   |   |-- ProjectA/</code><br>
<code>|   |   |   |   |-- src/</code><br>
<code>|   |   |   |   `-- README.md</code><br>
<code>|   |   |   `-- ProjectB/</code><br>
<code>|   |   |       |-- docs/</code><br>
<code>|   |   |       `-- data/</code><br>
<code>|   |   `-- Reports/</code><br>
<code>|   |       |-- Q1/</code><br>
<code>|   |       `-- Q2/</code><br>
<code>|   `-- Personal/</code><br>
<code>|       |-- Photos/</code><br>
<code>|       `-- Finance/</code><br>
<code>|-- Downloads/</code><br>
<code>|   |-- temp/</code><br>
<code>|   `-- archive/</code><br>
<code>|-- Pictures/</code><br>
<code>|   |-- Vacation/</code><br>
<code>|   `-- Family/</code><br>
<code>`-- Music/</code><br>
<code>    |-- Playlists/</code><br>
<code>    `-- Albums/</code></p>
"@

$matchingPath = "moodle-qbanks/questions-OS-Matching-20260507-1323.xml"
[xml]$matchingXml = Get-Content -Raw -LiteralPath $matchingPath

$q = Get-Question $matchingXml "linux-mtch-ff1-tree"
Set-NodeHtmlText ($q.questiontext.text) "<h3><strong>Match File and Folder Management Commands to Real-World Scenarios with tree structure:</strong></h3>$tree"
$ff1TreePrompts = @(
    "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. Create a new directory named <code>bin</code> inside the <code>src</code> folder.",
    "You are in <code>/home/user/Downloads</code>. Delete the <code>temp</code> directory and all its contents.",
    "You are in <code>/home/user/Documents/Work/Reports</code>. Copy the <code>Q1</code> folder to the <code>Q2</code> folder.",
    "You are in <code>/home/user/Pictures/Vacation</code>. Move all files from the <code>Vacation</code> folder to the <code>Family</code> folder.",
    "You are in <code>/home/user/Music/Playlists</code>. Create an empty file named <code>favorites.txt</code>.",
    "You are in <code>/home/user/Documents/Work/Projects</code>. Move the <code>ProjectA</code> folder to the <code>Reports</code> folder.",
    "You are in <code>/home/user/Documents/Personal</code>. Create a new file named <code>budget.txt</code> inside the <code>Finance</code> folder.",
    "You are in <code>/home/user/Pictures/Family</code>. Rename the <code>Family</code> folder to <code>Relatives</code>.",
    "You are in <code>/home/user/Music</code>. Delete the <code>Albums</code> folder and all its contents.",
    "You are in <code>/home/user/Documents/Work/Reports/Q1</code>. Copy all files from <code>Q1</code> to <code>Q2</code>."
)
for ($i = 0; $i -lt $q.subquestion.Count; $i++) {
    Set-NodeHtmlText ($q.subquestion[$i].text) "<p><strong>$($ff1TreePrompts[$i])</strong></p>"
}

$q = Get-Question $matchingXml "linux-mtch-navigation2-tree"
Set-NodeHtmlText ($q.questiontext.text) "<p><strong>Match Linux Navigation Commands with Real-World Examples with this tree structure:</strong></p>$tree"
$navTreePrompts = @(
    "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. Navigate to the <code>Reports</code> folder using a relative path.",
    "You are in <code>/home/user/Downloads</code>. Navigate to the <code>Finance</code> folder inside <code>Documents/Personal</code> using an absolute path.",
    "You are in <code>/home/user/Pictures/Vacation</code>. Navigate to the <code>src</code> folder inside <code>ProjectA</code> using a relative path.",
    "You are in <code>/home/user/Music/Playlists</code>. Navigate to the <code>temp</code> folder inside <code>Downloads</code> using an absolute path.",
    "You are in <code>/home/user/Documents/Work/Reports/Q1</code>. Navigate to the <code>Family</code> folder inside <code>Pictures</code> using a relative path.",
    "You are in <code>/home/user/Documents/Personal/Photos</code>. Navigate to the <code>data</code> folder inside <code>ProjectB</code> using an absolute path.",
    "You are in <code>/home/user/Downloads/archive</code>. Navigate to the <code>Albums</code> folder inside <code>Music</code> using a relative path.",
    "You are in <code>/home/user/Pictures</code>. Navigate to the <code>Q2</code> folder inside <code>Reports</code> using an absolute path.",
    "You are in <code>/home/user/Documents/Work/Projects/ProjectB/docs</code>. Navigate to the <code>Vacation</code> folder inside <code>Pictures</code> using a relative path.",
    "You are in <code>/home/user/Music</code>. Navigate to the <code>temp</code> folder inside <code>Downloads</code> using an absolute path."
)
for ($i = 0; $i -lt $q.subquestion.Count; $i++) {
    Set-NodeHtmlText ($q.subquestion[$i].text) "<p><strong>$($navTreePrompts[$i])</strong></p>"
}

$q = Get-Question $matchingXml "linux-mtch-navigation2-tree-advanced"
Set-NodeHtmlText ($q.questiontext.text) "<p><strong>Match Linux Navigation Commands with Real-World Examples with this tree structure:</strong></p>$tree"
$navAdvPrompts = @(
    "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. Navigate to the <code>Photos</code> folder inside <code>Personal</code> using a relative path.",
    "You are in <code>/home/user/Downloads/temp</code>. Navigate to the <code>Playlists</code> folder inside <code>Music</code> using a relative path.",
    "You are in <code>/home/user/Pictures/Family</code>. Navigate to the <code>archive</code> folder inside <code>Downloads</code> using an absolute path.",
    "You are in <code>/home/user/Documents/Work/Reports/Q2</code>. Navigate to the <code>Vacation</code> folder inside <code>Pictures</code> using a relative path.",
    "You are in <code>/home/user/Documents/Personal/Finance</code>. Navigate to the <code>ProjectB</code> folder inside <code>Projects</code> using an absolute path.",
    "You are in <code>/home/user/Music/Albums</code>. Navigate to the <code>temp</code> folder inside <code>Downloads</code> using a relative path.",
    "You are in <code>/home/user/Documents/Work/Projects/ProjectB/data</code>. Navigate to the <code>Q1</code> folder inside <code>Reports</code> using a relative path.",
    "You are in <code>/home/user/Pictures/Vacation</code>. Navigate to the <code>src</code> folder inside <code>ProjectA</code> using an absolute path.",
    "You are in <code>/home/user/Downloads/archive</code>. Navigate to the <code>Finance</code> folder inside <code>Personal</code> using a relative path.",
    "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. Navigate to the <code>Family</code> folder inside <code>Pictures</code> using an absolute path."
)
for ($i = 0; $i -lt $q.subquestion.Count; $i++) {
    Set-NodeHtmlText ($q.subquestion[$i].text) "<p><strong>$($navAdvPrompts[$i])</strong></p>"
}

$q = Get-Question $matchingXml "linux-mtch-redirection-tree"
Set-NodeHtmlText ($q.questiontext.text) "<h3><strong>Match Redirection Commands to Real-World Scenarios with tree structure:</strong></h3>$tree"
$redirPrompts = @(
    "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. Redirect the output of the <code>ls src</code> command to a file named <code>src_files.txt</code>.",
    "You are in <code>/home/user/Downloads</code>. Redirect the output of the <code>ls archive</code> command to a file named <code>archive_files.txt</code>.",
    "You are in <code>/home/user/Documents/Work/Reports</code>. Append the output of the <code>ls Q1</code> command to a file named <code>reports.txt</code>.",
    "You are in <code>/home/user/Pictures/Vacation</code>. Redirect the output of the <code>ls</code> command to a file named <code>vacation_photos.txt</code>.",
    "You are in <code>/home/user/Music/Playlists</code>. Redirect the output of the <code>ls</code> command to a file named <code>playlists.txt</code>.",
    "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. Redirect the output of the <code>grep ""TODO"" src/*.c</code> command to a file named <code>todos.txt</code>.",
    "You are in <code>/home/user/Downloads</code>. Redirect the output of the <code>find archive -name ""*.zip""</code> command to a file named <code>zip_files.txt</code>.",
    "You are in <code>/home/user/Documents/Work/Reports</code>. Append the output of the <code>grep ""error"" Q1/*.log</code> command to a file named <code>errors.txt</code>.",
    "You are in <code>/home/user/Pictures/Vacation</code>. Redirect the output of the <code>ls *.jpg</code> command to a file named <code>jpg_files.txt</code>.",
    "You are in <code>/home/user/Music/Playlists</code>. Redirect the output of the <code>ls *.mp3</code> command to a file named <code>mp3_files.txt</code>."
)
for ($i = 0; $i -lt $q.subquestion.Count; $i++) {
    Set-NodeHtmlText ($q.subquestion[$i].text) "<p><strong>$($redirPrompts[$i])</strong></p>"
}

$q = Get-Question $matchingXml "linux-mtch-wcard-tree"
Set-NodeHtmlText ($q.questiontext.text) "<h3><strong>Match Wildcard Commands to Real-World Scenarios with tree structure:</strong></h3>$tree"
$wcardPrompts = @(
    "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. List all files in the <code>src</code> folder with a <code>.c</code> extension.",
    "You are in <code>/home/user/Downloads</code>. Delete all files in the <code>temp</code> folder that start with <code>temp</code>.",
    "You are in <code>/home/user/Documents/Work/Reports</code>. Copy all files in the <code>Q1</code> folder that end with <code>.pdf</code> to the <code>Q2</code> folder.",
    "You are in <code>/home/user/Pictures/Vacation</code>. Move all files with a <code>.jpg</code> extension to the <code>Family</code> folder.",
    "You are in <code>/home/user/Music/Playlists</code>. List all files with a <code>.mp3</code> extension.",
    "You are in <code>/home/user/Downloads</code>. Delete all files in the <code>temp</code> folder that have a filename length of exactly 4 characters.",
    "You are in <code>/home/user/Documents/Work/Reports</code>. Copy all files in the <code>Q1</code> folder that start with <code>report</code> and have a <code>.txt</code> or <code>.doc</code> extension to the <code>Q2</code> folder.",
    "You are in <code>/home/user/Pictures/Vacation</code>. Move all files that start with <code>img</code> and have a <code>.jpg</code> or <code>.png</code> extension to the <code>Family</code> folder.",
    "You are in <code>/home/user/Music/Playlists</code>. List all files that start with <code>song</code> and have a filename ending with a digit."
)
for ($i = 0; $i -lt $q.subquestion.Count; $i++) {
    Set-NodeHtmlText ($q.subquestion[$i].text) "<p><strong>$($wcardPrompts[$i])</strong></p>"
}

$matchingXml.Save((Resolve-Path $matchingPath))

$shortPath = "moodle-qbanks/questions-OS-Linux-Short-20260507-1325.xml"
[xml]$shortXml = Get-Content -Raw -LiteralPath $shortPath

$shortPrompts = [ordered]@{
    "linux-short10" = "You are in <code>/home/user/Pictures/Vacation</code>. What command would you use to move all files from the <code>Vacation</code> folder to the <code>Family</code> folder?"
    "linux-short11" = "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. What command would you use to list all files in the <code>src</code> folder with a <code>.c</code> extension?"
    "linux-short12" = "You are in <code>/home/user/Downloads</code>. What command would you use to delete all files in the <code>temp</code> folder that start with <code>temp</code>?"
    "linux-short13" = "You are in <code>/home/user/Documents/Work/Reports</code>. What command would you use to copy all files in the <code>Q1</code> folder that end with <code>.pdf</code> to the <code>Q2</code> folder?"
    "linux-short14" = "You are in <code>/home/user/Pictures/Vacation</code>. What command would you use to move all files with a <code>.jpg</code> extension to the <code>Family</code> folder?"
    "linux-short15" = "You are in <code>/home/user/Documents/Work/Reports</code>. What command would you use to append the output of the <code>ls Q1</code> command to a file named <code>reports.txt</code>?"
    "linux-short16" = "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. How do you create a symbolic link named <code>docs_link</code> that points to the <code>docs</code> folder inside <code>ProjectB</code>?"
    "linux-short16 (copy)" = "You are in <code>/home/user/Music/Playlists</code>. How do you delete all files that start with <code>song</code> and have a filename ending with a digit?"
    "linux-short18" = "You are in <code>/home/user/Documents/Work/Reports</code>. How do you list all files in the <code>Q1</code> folder that start with <code>report</code> and have a <code>.txt</code> or <code>.doc</code> extension?"
    "linux-short18 (copy)" = "You are in <code>/home/user/Pictures/Vacation</code>. How do you move all files that start with <code>img</code> and have a <code>.jpg</code> or <code>.png</code> extension to the <code>Family</code> folder?"
    "linux-short20" = "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. How do you redirect the output of the <code>grep ""TODO"" src/*.c</code> command to a file named <code>todos.txt</code> and append any errors to a file named <code>errors.txt</code>?"
    "linux-short20 (copy)" = "You are in <code>/home/user/Pictures/Vacation</code>. How do you redirect the output of the <code>ls *.jpg</code> command to a file named <code>jpg_files.txt</code> and the error output to a file named <code>errors.txt</code>?"
    "linux-short5" = "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. What command would you use to navigate to the <code>Reports</code> folder using a relative path?"
    "linux-short6" = "You are in <code>/home/user/Pictures/Vacation</code>. What command would you use to navigate to the <code>src</code> folder inside <code>ProjectA</code> using a relative path?"
    "linux-short7" = "You are in <code>/home/user/Documents/Work/Reports/Q1</code>. What command would you use to navigate to the <code>Family</code> folder inside <code>Pictures</code> using a relative path?"
    "linux-short8" = "You are in <code>/home/user/Documents/Work/Projects/ProjectA</code>. What command would you use to create a new directory named <code>bin</code> inside the <code>src</code> folder?"
    "linux-short9" = "You are in <code>/home/user/Downloads</code>. What command would you use to delete the <code>temp</code> directory and all its contents?"
}

foreach ($name in $shortPrompts.Keys) {
    $q = Get-Question $shortXml $name
    if ($q) {
        Set-NodeHtmlText ($q.questiontext.text) "$tree<p><strong>$($shortPrompts[$name])</strong></p>"
    }
}

$shortXml.Save((Resolve-Path $shortPath))
Write-Output "Rewrote tree structure prompts."
