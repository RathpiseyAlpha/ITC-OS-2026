param(
    [string]$QbankDir = "moodle-qbanks"
)

function NodeText($node) {
    if ($null -eq $node) { return "" }
    if ($node -is [string]) { return [string]$node }
    return [string]$node.InnerText
}

function Clean($value) {
    if ($null -eq $value) { return "" }
    $text = [string]$value
    $text = $text -replace '<[^>]+>', ' '
    $text = $text -replace '&nbsp;', ' '
    $text = $text -replace '\s+', ' '
    return $text.Trim()
}

function SetNodeText($node, [string]$value) {
    if ($null -eq $node) { return }
    if ($node -is [string]) { return }
    if ($node.FirstChild -and $node.FirstChild.NodeType -eq [System.Xml.XmlNodeType]::CData) {
        $node.FirstChild.Value = $value
        return
    }
    $node.InnerText = $value
}

function SetShortAnswers($xml, [string]$name, [string[]]$answers) {
    $question = $xml.quiz.question | Where-Object { $_.type -ne "category" -and $_.name.text -eq $name } | Select-Object -First 1
    if ($null -eq $question) { return }

    $existingAnswers = @($question.answer)
    foreach ($answer in $existingAnswers) {
        [void]$question.RemoveChild($answer)
    }

    foreach ($answerText in $answers) {
        $answer = $xml.CreateElement("answer")
        [void]$answer.SetAttribute("fraction", "100")
        [void]$answer.SetAttribute("format", "moodle_auto_format")

        $text = $xml.CreateElement("text")
        $text.InnerText = $answerText
        [void]$answer.AppendChild($text)

        $feedback = $xml.CreateElement("feedback")
        [void]$feedback.SetAttribute("format", "moodle_auto_format")
        $feedbackText = $xml.CreateElement("text")
        $feedbackText.InnerText = ""
        [void]$feedback.AppendChild($feedbackText)
        [void]$answer.AppendChild($feedback)

        [void]$question.AppendChild($answer)
    }
}

function RemoveBlankMatchingPairs($xml) {
    foreach ($question in ($xml.quiz.question | Where-Object { $_.type -eq "matching" })) {
        $blankPairs = @($question.subquestion | Where-Object {
            [string]::IsNullOrWhiteSpace((Clean (NodeText $_.text))) -or
            [string]::IsNullOrWhiteSpace((Clean (NodeText $_.answer.text)))
        })

        foreach ($pair in $blankPairs) {
            [void]$question.RemoveChild($pair)
        }
    }
}

function SetMatchAnswer($xml, [string]$questionName, [string]$promptContains, [string]$answerText) {
    $question = $xml.quiz.question | Where-Object { $_.type -eq "matching" -and $_.name.text -eq $questionName } | Select-Object -First 1
    if ($null -eq $question) { return }

    foreach ($pair in $question.subquestion) {
        $prompt = Clean (NodeText $pair.text)
        if ($prompt -like "*$promptContains*") {
            $textNode = $pair.SelectSingleNode("answer/text")
            if ($null -ne $textNode) {
                $textNode.InnerText = $answerText
            }
        }
    }
}

function AddLectureShortQuestion($xml, [string]$name, [string]$prompt, [string[]]$answers) {
    $existing = $xml.quiz.question | Where-Object { $_.type -ne "category" -and $_.name.text -eq $name } | Select-Object -First 1
    if ($null -ne $existing) { return }

    $question = $xml.CreateElement("question")
    [void]$question.SetAttribute("type", "shortanswer")

    $nameNode = $xml.CreateElement("name")
    $nameText = $xml.CreateElement("text")
    $nameText.InnerText = $name
    [void]$nameNode.AppendChild($nameText)
    [void]$question.AppendChild($nameNode)

    $questionText = $xml.CreateElement("questiontext")
    [void]$questionText.SetAttribute("format", "html")
    $questionTextText = $xml.CreateElement("text")
    $questionTextText.InnerText = "<p>$prompt</p>"
    [void]$questionText.AppendChild($questionTextText)
    [void]$question.AppendChild($questionText)

    $generalFeedback = $xml.CreateElement("generalfeedback")
    [void]$generalFeedback.SetAttribute("format", "html")
    $generalFeedbackText = $xml.CreateElement("text")
    $generalFeedbackText.InnerText = ""
    [void]$generalFeedback.AppendChild($generalFeedbackText)
    [void]$question.AppendChild($generalFeedback)

    foreach ($pair in @(
        @("defaultgrade", "1.0000000"),
        @("penalty", "0.3333333"),
        @("hidden", "0")
    )) {
        $node = $xml.CreateElement($pair[0])
        $node.InnerText = $pair[1]
        [void]$question.AppendChild($node)
    }

    $idNumber = $xml.CreateElement("idnumber")
    $idNumber.InnerText = ""
    [void]$question.AppendChild($idNumber)

    $usecase = $xml.CreateElement("usecase")
    $usecase.InnerText = "0"
    [void]$question.AppendChild($usecase)

    foreach ($answerText in $answers) {
        $answer = $xml.CreateElement("answer")
        [void]$answer.SetAttribute("fraction", "100")
        [void]$answer.SetAttribute("format", "moodle_auto_format")

        $text = $xml.CreateElement("text")
        $text.InnerText = $answerText
        [void]$answer.AppendChild($text)

        $feedback = $xml.CreateElement("feedback")
        [void]$feedback.SetAttribute("format", "html")
        $feedbackText = $xml.CreateElement("text")
        $feedbackText.InnerText = ""
        [void]$feedback.AppendChild($feedbackText)
        [void]$answer.AppendChild($feedback)

        [void]$question.AppendChild($answer)
    }

    [void]$xml.quiz.AppendChild($question)
}

$linuxShortAnswers = @{
    "linux-short1" = @("mv *.log logs/", "mv *.log logs")
    "linux-short2" = @("cp *.jpg images/", "cp *.jpg images")
    "linux-short3" = @("rm temp*")
    "linux-short4" = @("ls *.txt")
    "linux-short5" = @("cd ../../Reports", "cd ../../Reports/")
    "linux-short6" = @("cd ../../Documents/Work/Projects/ProjectA/src", "cd ../../Documents/Work/Projects/ProjectA/src/")
    "linux-short7" = @("cd ../../../../Pictures/Family")
    "linux-short8" = @("mkdir src/bin")
    "linux-short9" = @("rm -r temp", "rm -r temp/")
    "linux-short10" = @("mv * ../Family/", "mv * ../Family")
    "linux-short11" = @("ls src/*.c")
    "linux-short12" = @("rm temp/temp*")
    "linux-short13" = @("cp Q1/*.pdf Q2/", "cp Q1/*.pdf Q2")
    "linux-short14" = @("mv *.jpg ../Family/", "mv *.jpg ../Family")
    "linux-short15" = @("ls Q1 >> reports.txt")
    "linux-short16" = @("ln -s ../ProjectB/docs docs_link")
    "linux-short16 (copy)" = @("rm song*[0-9].*")
    "linux-short18" = @("ls Q1/report*.txt Q1/report*.doc", "ls Q1/report*.{txt,doc}")
    "linux-short18 (copy)" = @("mv img*.jpg img*.png ../Family/", "mv img*.{jpg,png} ../Family/")
    "linux-short20" = @('grep "TODO" src/*.c > todos.txt 2>> errors.txt')
    "linux-short20 (copy)" = @("ls *.jpg > jpg_files.txt 2> errors.txt")
    "NEWSHORT1" = @("cut -d: -f6 /etc/passwd", "cut -f6 -d: /etc/passwd")
    "NEWSHORT2" = @("cut -d: -f7 /etc/passwd", "cut -f7 -d: /etc/passwd")
    "NEWSHORT3" = @("cut -d' ' -f1 access.log | sort -u | wc -l", "cut -d' ' -f1 access.log | sort | uniq | wc -l")
    "NEWSHORT4" = @('awk ''{print $1, $9}'' access.log', "cut -d' ' -f1,9 access.log")
    "NEWSHORT5" = @('awk ''($9==401 || $9==403) {print $1}'' access.log | sort | uniq -c', "grep -E ' 401 | 403 ' access.log | cut -d' ' -f1 | sort | uniq -c")
    "NEWSHORT5-1" = @('awk ''{print $7}'' access.log | sort -u | wc -l', "cut -d' ' -f7 access.log | sort -u | wc -l")
    "NEWSHORT5-2" = @("grep -Ei 'python|/\\?cmd' access.log", "grep -E 'python|/\\?cmd' access.log")
    "NEWSHORT5-3" = @("grep -E '/wp-admin|/admin|/wp-login\\.php' access.log | wc -l")
    "NEWSHORT6" = @("grep 'department:IT' employee.txt | wc -l", "cut -d',' -f3 employee.txt | grep 'department:IT' | wc -l")
    "NEWSHORT7" = @("cut -d',' -f2,4 employee.txt", "cut -f2,4 -d, employee.txt")
    "NEWSHORT8" = @("cut -d',' -f2 employee.txt | grep '^name:M'")
    "NEWSHORT9" = @("cut -d',' -f2 employee.txt | grep -E 'n$'", "cut -d',' -f2 employee.txt | grep 'n$'")
}

foreach ($fileName in @(
    "questions-OS-Linux-Short-20260507-1325.xml",
    "questions-OS-new-20260507-1323.xml"
)) {
    $path = Join-Path $QbankDir $fileName
    if (Test-Path -LiteralPath $path) {
        [xml]$xml = Get-Content -Raw -LiteralPath $path
        foreach ($entry in $linuxShortAnswers.GetEnumerator()) {
            SetShortAnswers $xml $entry.Key $entry.Value
        }
        $xml.Save((Resolve-Path -LiteralPath $path))
    }
}

$matchingPath = Join-Path $QbankDir "questions-OS-Matching-20260507-1323.xml"
[xml]$matchingXml = Get-Content -Raw -LiteralPath $matchingPath
RemoveBlankMatchingPairs $matchingXml
SetMatchAnswer $matchingXml "linux-mtch-ff1" "Deleting an empty directory named testdir" "rmdir testdir"
SetMatchAnswer $matchingXml "linux-mtch-ff1-tree" "Rename the Family folder to Relatives" "mv ../Family ../Relatives"
SetMatchAnswer $matchingXml "linux-mtch-redirection1" "Viewing only the first 10 lines of a file named log.txt" "head -n 10 log.txt"
SetMatchAnswer $matchingXml "linux-mtch-redirection1" "Viewing only the last 20 lines of a file" "tail -n 20 logfile.txt"
SetMatchAnswer $matchingXml "linux-mtch-redirection1" "Using one command" "cat file.txt | wc -w"
SetMatchAnswer $matchingXml "linux-mtch-redirection1" "Copying all files starting with doc to backup/" "cp doc* backup/"
SetMatchAnswer $matchingXml "linux-mtch-redirection2" "Redirect the output of the ls command" "ls > file_list.txt"
SetMatchAnswer $matchingXml "linux-mtch-redirection2" "Append the output of the date command" "date >> log.txt"
SetMatchAnswer $matchingXml "linux-mtch-redirection2" "Redirect the output of the echo ""Hello, World!"" command" 'echo "Hello, World!" > greeting.txt'
SetMatchAnswer $matchingXml "linux-mtch-redirection2" "Redirect the output of the cal command" "cal > calendar.txt"
SetMatchAnswer $matchingXml "linux-mtch-redirection2" "Append the output of the who command" "who >> users.txt"
SetMatchAnswer $matchingXml "linux-mtch-wcard-tree" "filename containing exactly one digit" "ls src/*[0-9]*"
SetMatchAnswer $matchingXml "linux-mtch-wildcard1-notree2" "filename length of 4 to 6 characters" "ls log? log?? log???"
$matchingXml.Save((Resolve-Path -LiteralPath $matchingPath))

$lectureShortPath = Join-Path $QbankDir "questions-OS-Short Answer-20260507-1324.xml"
[xml]$lectureXml = Get-Content -Raw -LiteralPath $lectureShortPath

$newLectureShort = @(
    @("lec-short24", "Which POSIX system call creates a child process by duplicating the current process?", @("fork()", "fork")),
    @("lec-short25", "Which POSIX function waits for a specific child process to finish?", @("waitpid()", "waitpid")),
    @("lec-short26", "Which POSIX function family replaces the current process image with a new program?", @("exec()", "exec")),
    @("lec-short27", "What is the Linux virtual filesystem that exposes process and kernel information?", @("/proc", "proc")),
    @("lec-short28", "What command-line tool traces the system calls made by a program?", @("strace")),
    @("lec-short29", "What is the numeric file descriptor for standard output in Unix-like systems?", @("1")),
    @("lec-short30", "What IPC mechanism maps the same memory region into multiple processes?", @("shared memory", "Shared Memory")),
    @("lec-short31", "What IPC mechanism stores discrete messages in an OS-managed queue?", @("message queue", "message queues", "Message Queue")),
    @("lec-short32", "Which socket call assigns a server socket to a local address and port?", @("bind()", "bind")),
    @("lec-short33", "Which socket call lets a server wait for incoming connection requests?", @("listen()", "listen")),
    @("lec-short34", "Which socket call returns a new connected socket for a client connection?", @("accept()", "accept")),
    @("lec-short35", "Which pthread function creates a new thread?", @("pthread_create()", "pthread_create")),
    @("lec-short36", "Which pthread function waits for a thread to finish?", @("pthread_join()", "pthread_join")),
    @("lec-short37", "What synchronization object is commonly used to protect shared data from races?", @("mutex", "Mutex")),
    @("lec-short38", "What bug occurs when multiple threads access shared data concurrently and the result depends on timing?", @("race condition", "Race Condition")),
    @("lec-short39", "In a process, what memory region stores dynamically allocated data?", @("heap", "Heap")),
    @("lec-short40", "In a process, what memory region stores function parameters, local variables, and return addresses?", @("stack", "Stack")),
    @("lec-short41", "What is a terminated child process whose parent has not collected its exit status?", @("zombie process", "zombie")),
    @("lec-short42", "What is a child process called when its parent exits before it finishes?", @("orphan process", "orphan")),
    @("lec-short43", "What Java interface is commonly implemented to define a task for a thread?", @("Runnable", "runnable"))
)

foreach ($entry in $newLectureShort) {
    AddLectureShortQuestion $lectureXml $entry[0] $entry[1] $entry[2]
}

$lectureXml.Save((Resolve-Path -LiteralPath $lectureShortPath))

Write-Output "Revised Linux banks and added lecture short-answer questions."
