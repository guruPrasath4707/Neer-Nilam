# Neer-Nilam data-lake bootstrap collector
# Version: 0.1.0. Safe by default: no write/download until -Execute is supplied.
[CmdletBinding()]
param(
    [string]$DestinationRoot = 'F:\Neer-Nilam-DataLake',
    [switch]$Execute,
    [switch]$SkipOSM
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ScriptVersion = '0.1.0'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$RunId = (Get-Date).ToString('yyyyMMdd-HHmmss')
$FullDestination = [System.IO.Path]::GetFullPath($DestinationRoot)
$Qualifier = Split-Path -Qualifier $FullDestination
if (-not $Qualifier) { throw 'Destination must be an absolute Windows drive path, for example F:\Neer-Nilam-DataLake' }
$DriveLetter = $Qualifier.Substring(0, 1)

Write-Host ''
Write-Host 'Neer-Nilam Data-Lake Collector 0.1.0' -ForegroundColor Cyan
Write-Host "Target: $FullDestination"
Write-Host 'Planned: DHARMA Tamil Nadu XML, DHARMA SII XML, HydroRIVERS Asia, bounded OSM extract.'
Write-Host 'Not automatic: Kaggle, manuscript images, restricted government GIS, global raster dumps, large 3D datasets.'
if (-not $Execute) {
    Write-Host 'DRY RUN ONLY. Nothing was created or downloaded.' -ForegroundColor Yellow
    Write-Host 'Check that the Seagate drive is connected, then rerun with -Execute.'
    return
}

if (-not (Test-Path -LiteralPath ($DriveLetter + ':\'))) {
    throw ('Drive ' + $DriveLetter + ': is not mounted. Connect the external drive and try again.')
}
$volume = Get-Volume -DriveLetter $DriveLetter
$partition = Get-Partition -DriveLetter $DriveLetter | Select-Object -First 1
$disk = Get-Disk -Number $partition.DiskNumber
$freeGiB = [math]::Round(($volume.SizeRemaining / 1GB), 2)
Write-Host "Volume label: $($volume.FileSystemLabel)"
Write-Host "Disk model:   $($disk.FriendlyName)"
Write-Host "Bus type:     $($disk.BusType)"
Write-Host "Free space:   $freeGiB GiB"
if ($freeGiB -lt 3) { throw 'At least 3 GiB free space is required for the initial collection.' }
if (($volume.FileSystemLabel -notmatch 'Seagate') -and ($disk.FriendlyName -notmatch 'Seagate')) {
    $driveConfirmation = Read-Host 'The volume name does not identify Seagate. Verify the physical drive, then type SEAGATE to continue'
    if ($driveConfirmation -cne 'SEAGATE') { throw 'Destination volume not confirmed as the intended Seagate HDD. No files were written.' }
}
$finalConfirmation = Read-Host "This will write only under $FullDestination. Type COLLECT to proceed"
if ($finalConfirmation -cne 'COLLECT') { throw 'Collection cancelled by user.' }

$Directories = @('00_admin\manifests','00_admin\licences','00_admin\checksums','01_raw\epigraphy','01_raw\hydrology','01_raw\spatial\osm','02_restricted_not_downloaded','03_normalized','04_evidence','05_derived','06_logs','07_quarantine')
foreach ($relative in $Directories) { New-Item -ItemType Directory -Path (Join-Path $FullDestination $relative) -Force | Out-Null }
$RunLog = Join-Path $FullDestination ("06_logs\collection-" + $RunId + '.jsonl')
$RepoManifest = Join-Path $RepoRoot 'data\manifests\data-lake-acquisition-v1.csv'
$ManifestPath = Join-Path $FullDestination '00_admin\manifests\data-lake-acquisition-v1.csv'
if (Test-Path -LiteralPath $RepoManifest) { Copy-Item -LiteralPath $RepoManifest -Destination $ManifestPath -Force }
$ShaPath = Join-Path $FullDestination ("00_admin\checksums\sha256-" + $RunId + '.csv')
$LicensePath = Join-Path $FullDestination '00_admin\licences\dharma-xml-license-inventory.csv'

function Write-Event {
    param([string]$Level, [string]$DatasetId, [string]$Message, [string]$Path = '')
    $entry = [pscustomobject]@{ timestamp=(Get-Date).ToString('o'); run_id=$RunId; level=$Level; dataset_id=$DatasetId; message=$Message; path=$Path }
    $entry | ConvertTo-Json -Compress | Add-Content -LiteralPath $RunLog -Encoding utf8NoBOM
    Write-Host "[$Level][$DatasetId] $Message"
}
function Get-RepositorySnapshot {
    param([string]$Url, [string]$TargetPath, [string]$DatasetId)
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Event 'BLOCKED' $DatasetId 'Git is not installed or not on PATH.' $TargetPath
        return
    }
    if (Test-Path -LiteralPath (Join-Path $TargetPath '.git')) {
        $head = (& git -C $TargetPath rev-parse HEAD 2>&1 | Out-String).Trim()
        Write-Event 'SKIPPED_EXISTING' $DatasetId "Existing checkout preserved; HEAD=$head. No reset/pull performed." $TargetPath
        return
    }
    if (Test-Path -LiteralPath $TargetPath) {
        Write-Event 'BLOCKED' $DatasetId 'Target folder exists but is not a Git checkout; not overwritten.' $TargetPath
        return
    }
    New-Item -ItemType Directory -Path (Split-Path -Parent $TargetPath) -Force | Out-Null
    $output = & git clone --depth 1 $Url $TargetPath 2>&1
    $exitCode = $LASTEXITCODE
    $output | ForEach-Object { Write-Host $_ }
    if ($exitCode -ne 0) { Write-Event 'FAILED' $DatasetId "git clone failed with exit code $exitCode." $TargetPath; return }
    $head = (& git -C $TargetPath rev-parse HEAD 2>&1 | Out-String).Trim()
    $branch = (& git -C $TargetPath branch --show-current 2>&1 | Out-String).Trim()
    Write-Event 'DOWNLOADED' $DatasetId "Shallow clone complete; branch=$branch; commit=$head" $TargetPath
}

Write-Event 'BEGIN' 'DLA-RUN' "Run started; collector=$ScriptVersion; destination=$FullDestination"
Get-RepositorySnapshot -Url 'https://github.com/erc-dharma/tfa-tamilnadu-epigraphy.git' -TargetPath (Join-Path $FullDestination '01_raw\epigraphy\DHARMA-TamilNadu') -DatasetId 'DLA-001'
Get-RepositorySnapshot -Url 'https://github.com/erc-dharma/tfa-sii-epigraphy.git' -TargetPath (Join-Path $FullDestination '01_raw\epigraphy\DHARMA-SII') -DatasetId 'DLA-002'

# Capture each XML file's declared licence; undeclared records require manual rights review.
$licenseRows = [System.Collections.Generic.List[object]]::new()
foreach ($repoFolder in @((Join-Path $FullDestination '01_raw\epigraphy\DHARMA-TamilNadu'),(Join-Path $FullDestination '01_raw\epigraphy\DHARMA-SII'))) {
    if (-not (Test-Path -LiteralPath $repoFolder)) { continue }
    $repoLabel = Split-Path -Leaf $repoFolder
    foreach ($file in (Get-ChildItem -LiteralPath $repoFolder -Filter '*.xml' -File -Recurse -ErrorAction SilentlyContinue)) {
        try {
            $xmlText = Get-Content -LiteralPath $file.FullName -Raw
            $matches = [regex]::Matches($xmlText, '<licence\b[^>]*target=["'']([^"'']+)["'']', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
            $licences = @()
            foreach ($match in $matches) { $licences += $match.Groups[1].Value }
            $uniqueLicences = @($licences | Sort-Object -Unique)
            $licenceValue = if ($uniqueLicences.Count -gt 0) { $uniqueLicences -join ';' } else { 'NO_XML_LICENCE_TAG_FOUND_REVIEW_REQUIRED' }
            $reviewStatus = if ($uniqueLicences.Count -gt 0) { 'REVIEW_EACH_RECORD' } else { 'UNDECLARED_REVIEW_REQUIRED' }
            $licenseRows.Add([pscustomobject]@{ repository=$repoLabel; relative_path=$file.FullName.Substring($FullDestination.Length).TrimStart('\'); licence_url=$licenceValue; review_status=$reviewStatus })
        } catch {
            $licenseRows.Add([pscustomobject]@{ repository=$repoLabel; relative_path=$file.FullName.Substring($FullDestination.Length).TrimStart('\'); licence_url='INVENTORY_READ_ERROR'; review_status='UNDECLARED_REVIEW_REQUIRED' })
        }
    }
}
if ($licenseRows.Count -gt 0) {
    $licenseRows | Export-Csv -LiteralPath $LicensePath -NoTypeInformation -Encoding utf8NoBOM
    Write-Event 'GENERATED' 'DLA-001/DLA-002' "Wrote $($licenseRows.Count) XML-level licence inventory rows." $LicensePath
} else {
    Write-Event 'REVIEW_REQUIRED' 'DLA-001/DLA-002' 'No XML files were available to inventory; check clone results.' $LicensePath
}

# Download and retain the original HydroRIVERS archive.
$hydroDir = Join-Path $FullDestination '01_raw\hydrology\HydroRIVERS-v1-Asia'
$hydroZip = Join-Path $hydroDir 'HydroRIVERS_v10_as_shp.zip'
try {
    New-Item -ItemType Directory -Path $hydroDir -Force | Out-Null
    if (-not (Test-Path -LiteralPath $hydroZip)) {
        $partial = $hydroZip + '.partial'
        if (Test-Path -LiteralPath $partial) { Remove-Item -LiteralPath $partial -Force }
        Invoke-WebRequest -Uri 'https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_as_shp.zip' -OutFile $partial -TimeoutSec 600 -Headers @{ 'User-Agent' = 'Neer-Nilam-DataLake/0.1' }
        if ((Get-Item -LiteralPath $partial).Length -lt 1MB) { throw 'HydroRIVERS download is unexpectedly small; do not use it as valid input.' }
        Move-Item -LiteralPath $partial -Destination $hydroZip
        Write-Event 'DOWNLOADED' 'DLA-004' "Downloaded $([math]::Round((Get-Item $hydroZip).Length / 1MB, 2)) MiB." $hydroZip
    } else {
        Write-Event 'SKIPPED_EXISTING' 'DLA-004' 'Archive already exists; not overwritten.' $hydroZip
    }
    $hydroHash = (Get-FileHash -LiteralPath $hydroZip -Algorithm SHA256).Hash
    Write-Event 'CHECKSUM' 'DLA-004' "SHA256=$hydroHash" $hydroZip
    $extractDir = Join-Path $hydroDir 'extracted'
    if (-not (Test-Path -LiteralPath $extractDir)) {
        Expand-Archive -LiteralPath $hydroZip -DestinationPath $extractDir
        Write-Event 'EXTRACTED' 'DLA-004' 'Expanded archive while preserving original ZIP.' $extractDir
    } else {
        Write-Event 'SKIPPED_EXISTING' 'DLA-004' 'Extraction folder already exists; not overwritten.' $extractDir
    }
    @'
Source: HydroSHEDS / HydroRIVERS v1 Asia shapefile
Landing page: https://www.hydrosheds.org/products/hydrorivers
Archive: https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_as_shp.zip
Rights: Read the current HydroSHEDS license agreement before redistribution or publication.
Use: Generalized regional river network, not a complete local tank/canal inventory.
Citation: Lehner, B. and Grill, G. (2013), HydroRIVERS; see source landing page for full citation.
'@ | Set-Content -LiteralPath (Join-Path $hydroDir 'SOURCE-AND-LICENSE.txt') -Encoding utf8NoBOM
} catch {
    Write-Event 'FAILED' 'DLA-004' $_.Exception.Message $hydroZip
    $partialPath = $hydroZip + '.partial'
    if (Test-Path -LiteralPath $partialPath) { Write-Event 'PARTIAL_RETAINED' 'DLA-004' 'A partial download remains; do not use as valid input.' $partialPath }
}

# Query only a bounded area for current OSM features; preserve the query and the response.
if (-not $SkipOSM) {
    $osmDir = Join-Path $FullDestination '01_raw\spatial\osm'
    $osmPath = Join-Path $osmDir ("overpass-thanjavur-kumbakonam-" + $RunId + '.json')
    $queryPath = Join-Path $osmDir ("overpass-query-" + $RunId + '.txt')
    $query = @'
[out:json][timeout:120];
(
  nwr["waterway"~"^(river|canal|stream|ditch|drain|dam|weir)$"](10.68,79.00,11.08,79.48);
  nwr["natural"="water"](10.68,79.00,11.08,79.48);
  nwr["landuse"="reservoir"](10.68,79.00,11.08,79.48);
  nwr["historic"~"^(monument|archaeological_site|ruins)$"](10.68,79.00,11.08,79.48);
  nwr["amenity"="place_of_worship"](10.68,79.00,11.08,79.48);
  nwr["building"="temple"](10.68,79.00,11.08,79.48);
  nwr["man_made"~"^(water_well|water_works|water_tower)$"](10.68,79.00,11.08,79.48);
);
out center geom;
'@
    try {
        Set-Content -LiteralPath $queryPath -Value $query -Encoding utf8NoBOM
        $body = 'data=' + [System.Uri]::EscapeDataString($query)
        $response = Invoke-WebRequest -Uri 'https://overpass-api.de/api/interpreter' -Method Post -ContentType 'application/x-www-form-urlencoded' -Body $body -TimeoutSec 240 -Headers @{ 'User-Agent' = 'Neer-Nilam-DataLake/0.1 (bounded research extraction)' }
        $parsed = $response.Content | ConvertFrom-Json -ErrorAction Stop
        if ($null -eq $parsed.elements) { throw 'Overpass response did not contain an elements array.' }
        [System.IO.File]::WriteAllText($osmPath, $response.Content, [System.Text.UTF8Encoding]::new($false))
        Write-Event 'DOWNLOADED' 'DLA-003' "Saved $($parsed.elements.Count) OSM elements. This is current mapped geography only." $osmPath
        @'
Source: OpenStreetMap contributors via Overpass API
Rights: ODbL; credit OpenStreetMap and contributors and preserve applicable ODbL obligations.
This cutout is limited to the query stored beside it. It is not historical evidence.
Keep object IDs, tags, query text and the retrieval timestamp.
'@ | Set-Content -LiteralPath (Join-Path $osmDir 'SOURCE-AND-LICENSE.txt') -Encoding utf8NoBOM
    } catch {
        Write-Event 'FAILED' 'DLA-003' $_.Exception.Message $osmPath
        Write-Event 'RETRY_GUIDANCE' 'DLA-003' 'Retain the saved query; Overpass may rate-limit or time out. Retry later with the same bounded query.' $queryPath
    }
} else {
    Write-Event 'SKIPPED_BY_OPTION' 'DLA-003' 'OSM request skipped by -SkipOSM.' ''
}

# Generate SHA-256 checksums for raw files. Git administrative data and partial files are excluded.
$shaRows = [System.Collections.Generic.List[object]]::new()
$rawRoot = Join-Path $FullDestination '01_raw'
foreach ($file in (Get-ChildItem -LiteralPath $rawRoot -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' -and $_.Name -notlike '*.partial' })) {
    try {
        $hash = Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256
        $shaRows.Add([pscustomobject]@{ relative_path=$file.FullName.Substring($FullDestination.Length).TrimStart('\'); size_bytes=$file.Length; sha256=$hash.Hash; last_write_utc=$file.LastWriteTimeUtc.ToString('o') })
    } catch {
        Write-Event 'CHECKSUM_FAILED' 'DLA-RUN' $_.Exception.Message $file.FullName
    }
}
if ($shaRows.Count -gt 0) {
    $shaRows | Export-Csv -LiteralPath $ShaPath -NoTypeInformation -Encoding utf8NoBOM
    Write-Event 'GENERATED' 'DLA-RUN' "Wrote $($shaRows.Count) SHA-256 rows." $ShaPath
}
@"
Neer-Nilam local data lake
Run ID: $RunId
Collector version: $ScriptVersion
Raw files are retained unchanged where practical. The acquisition manifest, log and checksum list describe collection; they do not prove historical claims.
Review all rights before redistribution or public release. Restricted or permission-sensitive sources were not downloaded by this script.
"@ | Set-Content -LiteralPath (Join-Path $FullDestination 'README-DATALAKE.txt') -Encoding utf8NoBOM
Write-Event 'COMPLETE' 'DLA-RUN' 'Collection run ended. Review log, SHA-256 list, XML licence inventory and all FAILED/REVIEW_REQUIRED entries.' $FullDestination
Write-Host ''
Write-Host "Collection log: $RunLog" -ForegroundColor Green
Write-Host "Checksum list:  $ShaPath"
Write-Host "Licence list:   $LicensePath"
Write-Host 'Next: inspect errors and licence inventory before normalization; do not ingest every downloaded record blindly.'
