# PowerShell script to update coupon codes

$inputFile = ".\links"
$tempFile = ".\links.tmp"

# Create a backup of the original file
Copy-Item $inputFile "$inputFile.backup"

# Get the content of the file
$content = Get-Content $inputFile

# Write the header
@"
NOV9FREE

/?couponCode=NOV9FREE

"@ | Set-Content $tempFile

# Process each line starting from line 4
$content | Select-Object -Skip 3 | ForEach-Object {
    if ($_ -match '^https://.*udemy\.com/course/.*') {
        # Remove existing coupon code if present and add new one
        $baseUrl = $_ -replace '\?couponCode=[^&\s]*', ''
        "$baseUrl/?couponCode=NOV9FREE"
    } else {
        $_
    }
} | Add-Content $tempFile

# Replace original file with new content
Move-Item -Force $tempFile $inputFile

Write-Host "URLs have been updated with the new coupon code NOV9FREE"
Write-Host "A backup of the original file has been saved as $inputFile.backup"