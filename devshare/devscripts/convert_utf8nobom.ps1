$srcFile = "fixtures/Sample_Data.json"
$destFile = "fixtures/Sample_Data.json"
$MyRawString = Get-Content -Raw "fixtures/Sample_Data.json"
$Utf8NoBomEncoding = New-Object System.Text.UTF8Encoding $False
[System.IO.File]::WriteAllLines($destFile, $MyRawString, $Utf8NoBomEncoding)
