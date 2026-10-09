[CmdletBinding()]
param(
 [string]$DestinationRoot='F:\Neer-Nilam-DataLake',
 [switch]$Execute,
 [int]$RainfallStartYear=2016,
 [int]$RainfallEndYear=2025,
 [switch]$SkipRainfall,
 [switch]$SkipReports,
 [switch]$SkipWorldCover,
 [switch]$SkipCgwb,
 [switch]$PublishMetadata
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$Version='1.1.0'
$Session=(Get-Date).ToString('yyyyMMdd-HHmmss')
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Root=[IO.Path]::GetFullPath($DestinationRoot)
$Qualifier=Split-Path -Qualifier $Root
if (-not $Qualifier) { throw 'Destination must be an absolute Windows drive path.' }
$Drive=$Qualifier.Substring(0,1)
$Folders=@(
'00_ADMIN\manifests','00_ADMIN\source_notes','00_ADMIN\licences','00_ADMIN\checksums','00_ADMIN\provenance',
'01_RAW_DATA\01_EPIGRAPHY','01_RAW_DATA\02_HYDROLOGY','01_RAW_DATA\03_GEOSPATIAL',
'01_RAW_DATA\04_CLIMATE\CHIRPS-v3\monthly-global-tif','01_RAW_DATA\05_GROUNDWATER\CGWB',
'01_RAW_DATA\06_AGRICULTURE\Tamil-Nadu-Season-Crop-Report','01_RAW_DATA\06_AGRICULTURE\Tamil-Nadu-Statistical-Handbook-2023-24',
'01_RAW_DATA\07_LAND_COVER\ESA-WorldCover-2021-v200','01_RAW_DATA\08_SURFACE_WATER\JRC-Global-Surface-Water',
'01_RAW_DATA\09_TERRAIN\Copernicus-DEM','01_RAW_DATA\10_CENSUS',
'01_RAW_DATA\11_HISTORICAL_MAPS\National-Archives-India','01_RAW_DATA\11_HISTORICAL_MAPS\Abhilekh-Patal',
'01_RAW_DATA\11_HISTORICAL_MAPS\David-Rumsey','01_RAW_DATA\12_MANUSCRIPTS\CICT','01_RAW_DATA\12_MANUSCRIPTS\Kriti-Sampada',
'01_RAW_DATA\13_OCR\Kaggle-uTHCD','01_RAW_DATA\13_OCR\TamilOCR-TamilNet-references','01_RAW_DATA\14_HERITAGE_3D\Open-Heritage-3D',
'02_WORKING_DERIVED\rasters','02_WORKING_DERIVED\vectors','02_WORKING_DERIVED\tables',
'03_EVIDENCE_MODEL\sources','03_EVIDENCE_MODEL\claims','03_EVIDENCE_MODEL\entities','03_EVIDENCE_MODEL\historical_states',
'04_SCENE_PACKS\Brihadisvara-v0','05_PHYSICAL_REPRESENTATION\research','05_PHYSICAL_REPRESENTATION\prototypes',
'06_PROJECT_DOCUMENTS','07_LOGS','08_REPORTS\audit','09_QUARANTINE\invalid-downloads'
)
if (-not $Execute) {
 Write-Host 'NEER-NILAM P0 DATA SESSION - DRY RUN' -ForegroundColor Cyan
 Write-Host "Target: $Root"
 Write-Host "CHIRPS: $RainfallStartYear-$RainfallEndYear monthly global rasters; default 120 files, roughly 2.5-3 GiB."
 Write-Host 'Official reports: TN Season and Crop Report 2024-25, three Statistical Handbook sections, discover CGWB yearbook PDF.'
 Write-Host 'Optional: one ESA WorldCover tile candidate; validate signature before acceptance.'
 Write-Host 'Organizes existing data, preserves legacy paths, appends Log.txt, copies Word dossier, creates manifests/checksums.'
 Write-Host 'DRY RUN ONLY. No writes or downloads.' -ForegroundColor Yellow
 return
}
if ($RainfallStartYear -lt 1981 -or $RainfallEndYear -gt (Get-Date).Year -or $RainfallStartYear -gt $RainfallEndYear) { throw 'Invalid rainfall years. Use 1981-current year and start <= end.' }
if (-not (Test-Path -LiteralPath ($Drive + ':\'))) { throw "Drive $($Drive): is not mounted." }
$Volume=Get-Volume -DriveLetter $Drive
$Partition=Get-Partition -DriveLetter $Drive | Select-Object -First 1
$Disk=Get-Disk -Number $Partition.DiskNumber
$Free=[math]::Round($Volume.SizeRemaining/1GB,2)
Write-Host "Target=$Root; volume=$($Volume.FileSystemLabel); disk=$($Disk.FriendlyName); bus=$($Disk.BusType); free=$Free GiB" -ForegroundColor Cyan
if ($Free -lt 10) { throw 'At least 10 GiB free space is required.' }
if (($Volume.FileSystemLabel -notmatch 'Seagate') -and ($Disk.FriendlyName -notmatch 'Seagate')) {
 $v=Read-Host 'Verify physical drive and type SEAGATE'
 if ($v -cne 'SEAGATE') { throw 'Drive was not confirmed.' }
}
$v=Read-Host "Write/download only under $Root. Type COLLECT-NEERNILAM-P0"
if ($v -cne 'COLLECT-NEERNILAM-P0') { throw 'Cancelled before changes.' }
New-Item -ItemType Directory -Path $Root -Force | Out-Null
foreach($f in $Folders){ New-Item -ItemType Directory -Path (Join-Path $Root $f) -Force | Out-Null }
$Log=Join-Path $Root 'Log.txt'
$JsonLog=Join-Path $Root ("07_LOGS\critical-session-$Session.jsonl")
$Manifest=Join-Path $Root ("00_ADMIN\manifests\critical-session-$Session.csv")
$Hashes=Join-Path $Root ("00_ADMIN\checksums\critical-session-sha256-$Session.csv")
$RunDir=Join-Path $Repo 'docs\collection-runs'
New-Item -ItemType Directory -Path $RunDir -Force | Out-Null
$Rows=[Collections.Generic.List[object]]::new()
$HashRows=[Collections.Generic.List[object]]::new()
if (-not (Test-Path -LiteralPath $Log -PathType Leaf)) {
 @'
NEER-NILAM DATA-LAKE MASTER LOG
Append-only chronological record; details and decisions also live in GitHub docs/project-log.
Historical milestones compiled 2026-10-09:
001. Holographic/immersive concept and representation research logged.
002. GIS and physical display alternatives identified; no expensive hardware before measured proof.
003. Stage-1 optical/display validation started; Pepper's Ghost and projection-mapped relief remain proof tracks.
004. Source registry, evidence/data schemas and presentation-neutral architecture established in planning.
005. Team pitched project to Judy ma'am. Guidance relayed: she will explore a physical-representation path; focus now on software and dataset/data-lake collection. Display choice remains open.
006. Groundwater, agriculture and historical map sources added to discovery plan.
007. Initial script launch failed from C:\Windows\System32; no collection occurred in that failed attempt.
008. Repository cloned to C:\Users\gurun\source\Neer-Nilam; dry run confirmed no writes.
009. Seagate Expansion Drive verified as F: (NTFS, USB, online); 931.51 GiB capacity and 374 GiB free at first check.
010. Collection run 20261009-111437: DHARMA TN commit ab94f9e525e2ce21938e63ac93fd80aa78a4e423; DHARMA SII commit dfa95be6729f162c0e7b70eea15c51da94520ff4; HydroRIVERS 86.32 MiB; OSM 998 elements; 553 XML licence rows; 581 checksum rows.
011. Integrity audit passed 581/581 hashes, zero missing files and mismatches, no attention-level collection events.
012. DHARMA conflict: 507 XML records declare CC BY-SA 4.0; 46 no licence target detected; both repository READMEs say CC BY 4.0. No redistribution or public reusable derivatives until written clarification.
013. Critical acquisition, file categorization, Log and Word dossier session prepared; execution result appended below.

Guardrails: modern OSM, HydroRIVERS, rainfall, groundwater, agriculture and land cover are context, not direct proof of Chola-era conditions. Record source, valid/document time, transformations, rights, uncertainty and human review. Do not push raw datasets or permission-sensitive files to public GitHub.
'@ | Set-Content -LiteralPath $Log -Encoding utf8NoBOM
}
function Event([string]$Level,[string]$Id,[string]$Message,[string]$Rel='') {
 $e=[pscustomobject]@{timestamp=(Get-Date).ToString('o');session=$Session;level=$Level;dataset_id=$Id;message=$Message;relative_path=$Rel}
 $e | ConvertTo-Json -Compress | Add-Content -LiteralPath $JsonLog -Encoding utf8NoBOM
 $line='{0} [{1}] [{2}] {3}' -f $e.timestamp,$Level,$Id,$Message
 if($Rel){$line += " | $Rel"}
 Add-Content -LiteralPath $Log -Value $line -Encoding utf8NoBOM
 Write-Host $line
}
function Move-Data([string]$OldRel,[string]$NewRel) {
 $old=Join-Path $Root $OldRel; $new=Join-Path $Root $NewRel
 if(Test-Path -LiteralPath $old){
  $oi=Get-Item -LiteralPath $old -Force
  if($oi.LinkType -eq 'Junction'){Event 'ALREADY_CATEGORIZED' 'EXISTING' 'Legacy junction already exists.' $OldRel;return}
  if(Test-Path -LiteralPath $new){throw "Both old and new folders exist. No merge performed: $old"}
  New-Item -ItemType Directory -Path (Split-Path -Parent $new) -Force | Out-Null
  Move-Item -LiteralPath $old -Destination $new
  New-Item -ItemType Directory -Path (Split-Path -Parent $old) -Force | Out-Null
  New-Item -ItemType Junction -Path $old -Target $new | Out-Null
  Event 'CATEGORIZED' 'EXISTING' 'Moved to canonical category; old path retained as junction.' $NewRel
 } elseif(Test-Path -LiteralPath $new) {
  New-Item -ItemType Directory -Path (Split-Path -Parent $old) -Force | Out-Null
  New-Item -ItemType Junction -Path $old -Target $new | Out-Null
  Event 'LEGACY_JUNCTION' 'EXISTING' 'Created compatibility junction to canonical folder.' $NewRel
 } else { Event 'NOT_PRESENT' 'EXISTING' 'Source folder not found; no empty alias created.' $OldRel }
}
function ValidSignature([string]$Path,[string]$Kind,[long]$Min) {
 if(-not(Test-Path -LiteralPath $Path -PathType Leaf)){return $false}
 if((Get-Item -LiteralPath $Path).Length -lt $Min){return $false}
 $s=[IO.File]::OpenRead($Path)
 try{$b=New-Object byte[] 8;$n=$s.Read($b,0,8)}finally{$s.Dispose()}
 if($Kind -eq 'PDF'){return ($n -ge 5 -and [Text.Encoding]::ASCII.GetString($b,0,5) -eq '%PDF-')}
 if($n -lt 4){return $false}
 return (($b[0]-eq 0x49 -and $b[1]-eq 0x49 -and $b[2]-eq 0x2A -and $b[3]-eq 0) -or ($b[0]-eq 0x4D -and $b[1]-eq 0x4D -and $b[2]-eq 0 -and $b[3]-eq 0x2A) -or ($b[0]-eq 0x49 -and $b[1]-eq 0x49 -and $b[2]-eq 0x2B -and $b[3]-eq 0) -or ($b[0]-eq 0x4D -and $b[1]-eq 0x4D -and $b[2]-eq 0 -and $b[3]-eq 0x2B))
}
function Record([string]$Id,[string]$Title,[string]$Url,[string]$Status,[string]$Rel,[string]$Rights,[string]$Notes,[switch]$Hash) {
 $p=Join-Path $Root $Rel
 $isFile=Test-Path -LiteralPath $p -PathType Leaf
 $isDir=Test-Path -LiteralPath $p -PathType Container
 $exists=($isFile -or $isDir)
 $size=0L
 $sha=''
 if($isFile){
  $it=Get-Item -LiteralPath $p
  $size=$it.Length
  if($Hash){
   $sha=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash
   $HashRows.Add([pscustomobject]@{relative_path=$Rel;size_bytes=$size;sha256=$sha;dataset_id=$Id;captured_utc=(Get-Date).ToUniversalTime().ToString('o')})
  }
 } elseif($isDir) {
  $fileList=@(Get-ChildItem -LiteralPath $p -File -Recurse -ErrorAction SilentlyContinue)
  if($fileList.Count -gt 0){$size=($fileList | Measure-Object -Property Length -Sum).Sum}
 }
 $Rows.Add([pscustomobject]@{session_id=$Session;dataset_id=$Id;title=$Title;source_url=$Url;status=$Status;relative_path=$Rel;exists=[bool]$exists;size_bytes=$size;sha256=$sha;rights_status=$Rights;notes=$Notes})
}
function Get-Asset([string]$Id,[string]$Title,[string]$Url,[string]$Rel,[string]$Kind,[long]$Min,[string]$Rights,[string]$Notes) {
 $target=Join-Path $Root $Rel;New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
 if(Test-Path -LiteralPath $target -PathType Leaf){
  if(ValidSignature $target $Kind $Min){Event 'SKIPPED_EXISTING_VALID' $Id 'Existing valid asset was preserved.' $Rel;Record $Id $Title $Url 'SKIPPED_EXISTING_VALID' $Rel $Rights $Notes -Hash;return $true}
  $bad=Join-Path (Join-Path $Root '09_QUARANTINE\invalid-downloads') ((Split-Path -Leaf $target)+'.invalid-existing-'+$Session)
  Move-Item -LiteralPath $target -Destination $bad
  Event 'QUARANTINED' $Id 'Pre-existing file failed validation.' $bad
 }
 $ok=$false;$partial=$target+'.partial'
 for($try=1;$try -le 2;$try++){
  if(Test-Path -LiteralPath $partial){Remove-Item -LiteralPath $partial -Force}
  try{
   Event 'DOWNLOAD_START' $Id "Attempt $try of 2." $Rel
   Invoke-WebRequest -Uri $Url -OutFile $partial -TimeoutSec 600 -Headers @{'User-Agent'='Neer-Nilam-DataLake/1.1 research collector'}
   if(-not(ValidSignature $partial $Kind $Min)){
    $bad=Join-Path (Join-Path $Root '09_QUARANTINE\invalid-downloads') ((Split-Path -Leaf $target)+'.invalid-'+$Session+'-'+$try)
    Move-Item -LiteralPath $partial -Destination $bad
    throw "Payload was not a valid $Kind file; it was quarantined at $bad."
   }
   Move-Item -LiteralPath $partial -Destination $target;$ok=$true;break
  }catch{
   Event 'DOWNLOAD_ATTEMPT_FAILED' $Id $_.Exception.Message $Rel
   if(Test-Path -LiteralPath $partial){$bad=Join-Path (Join-Path $Root '09_QUARANTINE\invalid-downloads') ((Split-Path -Leaf $target)+'.partial-'+$Session+'-'+$try);Move-Item -LiteralPath $partial -Destination $bad -ErrorAction SilentlyContinue}
  }
 }
 if($ok){
  Event 'DOWNLOADED_VALIDATED' $Id "Validated $Kind payload ($([math]::Round((Get-Item $target).Length/1MB,2)) MiB)." $Rel
  @"
Dataset ID: $Id
Title: $Title
Source URL: $Url
Retrieved UTC: $((Get-Date).ToUniversalTime().ToString('o'))
Rights note: $Rights
Use limitation: $Notes
"@ | Set-Content -LiteralPath ($target+'.SOURCE.txt') -Encoding utf8NoBOM
  Record $Id $Title $Url 'DOWNLOADED_VALIDATED' $Rel $Rights $Notes -Hash;return $true
 }
 Record $Id $Title $Url 'FAILED_AFTER_TWO_ATTEMPTS' $Rel $Rights $Notes;return $false
}
Event 'BEGIN' 'P0-SESSION' "Collector $Version; CHIRPS $RainfallStartYear-$RainfallEndYear."
Move-Data '01_raw\epigraphy\DHARMA-TamilNadu' '01_RAW_DATA\01_EPIGRAPHY\DHARMA-TamilNadu'
Move-Data '01_raw\epigraphy\DHARMA-SII' '01_RAW_DATA\01_EPIGRAPHY\DHARMA-SII'
Move-Data '01_raw\hydrology\HydroRIVERS-v1-Asia' '01_RAW_DATA\02_HYDROLOGY\HydroRIVERS-v1-Asia'
Move-Data '01_raw\spatial\osm' '01_RAW_DATA\03_GEOSPATIAL\OpenStreetMap'
Record 'DLA-001' 'DHARMA Tamil Nadu epigraphy' 'https://github.com/erc-dharma/tfa-tamilnadu-epigraphy' 'ALREADY_COLLECTED_HOLD_REUSE' '01_RAW_DATA\01_EPIGRAPHY\DHARMA-TamilNadu' 'LICENCE_RECONCILIATION_REQUIRED' 'Commit ab94f9e525e2ce21938e63ac93fd80aa78a4e423; hold redistribution until written clarification.'
Record 'DLA-002' 'DHARMA SII epigraphy' 'https://github.com/erc-dharma/tfa-sii-epigraphy' 'ALREADY_COLLECTED_HOLD_REUSE' '01_RAW_DATA\01_EPIGRAPHY\DHARMA-SII' 'LICENCE_RECONCILIATION_REQUIRED' 'Commit dfa95be6729f162c0e7b70eea15c51da94520ff4; hold redistribution until written clarification.'
$hydroRel='01_RAW_DATA\02_HYDROLOGY\HydroRIVERS-v1-Asia\HydroRIVERS_v10_as_shp.zip'
Record 'DLA-004' 'HydroRIVERS Asia original ZIP' 'https://www.hydrosheds.org/products/hydrorivers' 'ALREADY_COLLECTED' $hydroRel 'HYDROSHEDS_TERMS_REVIEW' 'Generalized river network; check terms before redistribution.' -Hash
$osmDir=Join-Path $Root '01_RAW_DATA\03_GEOSPATIAL\OpenStreetMap'
$osm=Get-ChildItem -LiteralPath $osmDir -Filter 'overpass-thanjavur-kumbakonam-*.json' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if($osm){$rel=$osm.FullName.Substring($Root.Length).TrimStart('\');Record 'DLA-003' 'OpenStreetMap corridor extract' 'https://www.openstreetmap.org/copyright' 'ALREADY_COLLECTED' $rel 'ODBL_ATTRIBUTION_REQUIRED' 'Initial run reported 998 current mapped elements; not historical evidence.' -Hash}
else{Record 'DLA-003' 'OpenStreetMap corridor extract' 'https://www.openstreetmap.org/copyright' 'EXISTING_EXTRACT_NOT_FOUND' '01_RAW_DATA\03_GEOSPATIAL\OpenStreetMap' 'ODBL_ATTRIBUTION_REQUIRED' 'No matching JSON cutout found after categorization.'}
$dossierName='Neer-Nilam_Project_History_and_Collection_Dossier_2026-10-09.docx'
$dossierCandidates=@(
 (Join-Path $Repo ("docs\project-dossier\"+$dossierName)),
 (Join-Path $env:USERPROFILE ("Downloads\"+$dossierName)),
 (Join-Path $env:USERPROFILE ("Desktop\"+$dossierName))
)
$dossierSrc=$dossierCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
if($dossierSrc){Copy-Item -LiteralPath $dossierSrc -Destination (Join-Path $Root ("06_PROJECT_DOCUMENTS\"+$dossierName)) -Force;Event 'DOCX_COPIED' 'DOCX-001' "Copied project history and physical-representation Word dossier from $dossierSrc." '06_PROJECT_DOCUMENTS'}
else{Event 'DOCX_MISSING' 'DOCX-001' 'Word dossier was not found in the clone, Downloads or Desktop. Download the dossier artifact, save it in Downloads, and rerun the session if the file is needed on Seagate.' '06_PROJECT_DOCUMENTS'}
$manifestSrc=Join-Path $Repo 'data\manifests\critical-data-acquisition-session-v1.csv'
if(Test-Path -LiteralPath $manifestSrc -PathType Leaf){Copy-Item -LiteralPath $manifestSrc -Destination (Join-Path $Root '00_ADMIN\manifests\critical-data-acquisition-session-v1.csv') -Force}
$logSrc=Join-Path $Repo 'docs\project-log\Log.txt'
if(Test-Path -LiteralPath $logSrc -PathType Leaf){Copy-Item -LiteralPath $logSrc -Destination (Join-Path $Root '00_ADMIN\provenance\GitHub-Log-snapshot.txt') -Force}
if(-not $SkipWorldCover){
 $url='https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N09E078_Map.tif'
 [void](Get-Asset 'DLA-006' 'ESA WorldCover 2021 v200 tile candidate N09E078' $url '01_RAW_DATA\07_LAND_COVER\ESA-WorldCover-2021-v200\ESA_WorldCover_10m_2021_v200_N09E078_Map.tif' 'TIFF' 5MB 'CC BY 4.0 with ESA attribution' 'Modern 2021 context only; URL is a candidate and signature is checked.')
}
if(-not $SkipRainfall){
 $base='https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/global/tifs'
 $total=($RainfallEndYear-$RainfallStartYear+1)*12;$done=0
 for($year=$RainfallStartYear;$year -le $RainfallEndYear;$year++){
  for($month=1;$month -le 12;$month++){
   $done++;$mm='{0:D2}' -f $month;$name="chirps-v3.0.$year.$mm.tif";$url="$base/$name"
   $rel="01_RAW_DATA\04_CLIMATE\CHIRPS-v3\monthly-global-tif\$name"
   [void](Get-Asset 'DLA-008' "CHIRPS v3 monthly rainfall $year-$mm" $url $rel 'TIFF' 10MB 'Check current official CHIRPS v3 CC BY 4.0/public-domain terms and cite dataset DOI' 'Modern gridded rainfall estimate, not gauge data; clip region for study. Selected period only.')
   if(($done%12)-eq 0){Write-Host "CHIRPS progress $done/$total" -ForegroundColor DarkCyan}
  }
 }
 @'
CHIRPS v3 monthly GeoTIFFs
Official landing page: https://chc.ucsb.edu/data/chirps3
Source directory: https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/global/tifs/
Default period: Jan 2016-Dec 2025. This is a selected window, not the full 1981-present archive.
Dataset DOI: 10.15780/G2JQ0P. Funk et al. (2026), Scientific Data 13, 718, DOI 10.1038/s41597-026-07096-4.
Check current official licence wording and attribution before redistribution. Clip the selected raw rasters to the pilot corridor for analysis.
'@ | Set-Content -LiteralPath (Join-Path $Root '00_ADMIN\source_notes\CHIRPS-v3-SOURCE-AND-CITATION.txt') -Encoding utf8NoBOM
}
if(-not $SkipReports){
 $pdfs=@(
 [pscustomobject]@{id='DLA-022';title='Tamil Nadu Season and Crop Report 2024-2025';url='https://drive.google.com/uc?export=download&id=1kvlGkhj-FoYdGk4UkZR4h5G8Nz2cERPX';path='01_RAW_DATA\06_AGRICULTURE\Tamil-Nadu-Season-Crop-Report\Tamil-Nadu-Season-and-Crop-Report-2024-2025.pdf';notes='Official modern agriculture report; preserve table/page/unit/reference period.'},
 [pscustomobject]@{id='TN-HANDBOOK-CLIMATE';title='TN Statistical Handbook 2023-24 Climate and Rainfall';url='https://drive.google.com/uc?export=download&id=1apatQ7dTXHeViypoXqshKQjy6gpNrjeB';path='01_RAW_DATA\06_AGRICULTURE\Tamil-Nadu-Statistical-Handbook-2023-24\03_Climate-and-Rainfall.pdf';notes='Modern climate context; cite table/page and period.'},
 [pscustomobject]@{id='TN-HANDBOOK-AGRICULTURE';title='TN Statistical Handbook 2023-24 Agriculture';url='https://drive.google.com/uc?export=download&id=1_MGyPaeR1U1SslSjqeUdEJd2V5LkE5jT';path='01_RAW_DATA\06_AGRICULTURE\Tamil-Nadu-Statistical-Handbook-2023-24\04_Agriculture.pdf';notes='Modern crop context; preserve definitions and units.'},
 [pscustomobject]@{id='TN-HANDBOOK-IRRIGATION';title='TN Statistical Handbook 2023-24 Irrigation';url='https://drive.google.com/uc?export=download&id=1mRx6pFJsn6sQzLG14rL7AOogXSrRHo5S';path='01_RAW_DATA\06_AGRICULTURE\Tamil-Nadu-Statistical-Handbook-2023-24\05_Irrigation.pdf';notes='Modern irrigation context only.'}
 )
 foreach($p in $pdfs){[void](Get-Asset $p.id $p.title $p.url $p.path 'PDF' 40000 'Official publication; review reuse terms' $p.notes)}
}
if(-not $SkipCgwb){
 $landing='https://cgwb.gov.in/cgwbpnm/public/publication-detail/2023'
 $rel='01_RAW_DATA\05_GROUNDWATER\CGWB\Groundwater-Year-Book-Tamil-Nadu-Puducherry-2024-2025.pdf';$ok=$false
 try{
  $page=Invoke-WebRequest -Uri $landing -TimeoutSec 90 -Headers @{'User-Agent'='Neer-Nilam-DataLake/1.1'}
  $pattern='(?is)<a\b[^>]*href\s*=\s*(["''])(?<href>.*?)\1[^>]*>(?<body>.*?)</a>'
  $urls=[Collections.Generic.List[string]]::new()
  foreach($m in [regex]::Matches($page.Content,$pattern)){
   $href=[Net.WebUtility]::HtmlDecode($m.Groups['href'].Value);$body=[regex]::Replace($m.Groups['body'].Value,'<[^>]+>',' ')
   if((($body -match '(?i)download|pdf|view') -or ($href -match '(?i)\.pdf|download|file|media')) -and $href -and $href -notmatch '^#|^javascript:|publication-detail'){
    try{$urls.Add(([Uri]::new([Uri]$landing,$href)).AbsoluteUri)}catch{}
   }
  }
  foreach($u in @($urls|Sort-Object -Unique)){if(Get-Asset 'DLA-020' 'CGWB groundwater year book Tamil Nadu/Puducherry 2024-2025' $u $rel 'PDF' 40000 'Official report; verify reuse terms' 'Modern measurements only; inspect districts, station IDs, dates, units and page references.'){ $ok=$true;break}}
 }catch{Event 'CGWB_LINK_DISCOVERY_FAILED' 'DLA-020' $_.Exception.Message $landing}
 if(-not $ok){Event 'MANUAL_DOWNLOAD_REQUIRED' 'DLA-020' 'No candidate from the official publication page passed PDF signature validation; download manually from the official page and record its source.' '01_RAW_DATA\05_GROUNDWATER\CGWB';Record 'DLA-020' 'CGWB groundwater yearbook Tamil Nadu/Puducherry 2024-2025' $landing 'MANUAL_DOWNLOAD_REQUIRED' $rel 'OFFICIAL_TERMS_REVIEW' 'Dynamic link not validated; no successful download claimed.'}
}
$gated=@(
@{id='DLA-007';title='JRC Global Surface Water 1984-2024';url='https://global-surface-water.appspot.com/download';status='MANUAL_TILE_SELECTION_REQUIRED';path='01_RAW_DATA\08_SURFACE_WATER\JRC-Global-Surface-Water';rights='Attribution and citation';notes='Select correct 10x10-degree tile and layer/version; no global mirror.'},
@{id='DLA-005';title='Copernicus DEM GLO-90';url='https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM';status='MANUAL_ACCESS_AND_TILE_REVIEW';path='01_RAW_DATA\09_TERRAIN\Copernicus-DEM';rights='GLO-90 official access/terms; GLO-30 restricted';notes='Use official regional tile and access route.'},
@{id='DLA-010/011';title='Census of India Thanjavur sources';url='https://www.censusindia.gov.in/nada/index.php/catalog/45367';status='MANUAL_ITEM_AND_TERMS_REVIEW';path='01_RAW_DATA\10_CENSUS';rights='Official item-specific terms';notes='Choose exact catalogue file; modern baseline only.'},
@{id='DLA-025';title='National Archives of India maps';url='https://www.nationalarchives.nic.in/en/public-records-holdings/cartographic-records';status='CATALOGUE_DISCOVERY_ONLY';path='01_RAW_DATA\11_HISTORICAL_MAPS\National-Archives-India';rights='Access and reproduction rules';notes='Catalogue only; request selected local map.'},
@{id='DLA-026';title='Abhilekh Patal archives';url='https://nationalarchives.nic.in/en/online-records-national-archives-india/abhilekh-patal';status='CATALOGUE_DISCOVERY_ONLY';path='01_RAW_DATA\11_HISTORICAL_MAPS\Abhilekh-Patal';rights='Item-level terms';notes='Record archive identifiers and exact pages.'},
@{id='DLA-027';title='David Rumsey maps';url='https://www.davidrumsey.com/about/copyright-and-permissions';status='ITEM_LEVEL_RIGHTS_REVIEW';path='01_RAW_DATA\11_HISTORICAL_MAPS\David-Rumsey';rights='Per-item map/image rights';notes='Prefer detailed Tanjore/Cauvery sheets.'},
@{id='DLA-014';title='CICT palm-leaf manuscript catalogue';url='https://www.digitalarchives.cict.in/';status='ITEM_LEVEL_RIGHTS_REVIEW';path='01_RAW_DATA\12_MANUSCRIPTS\CICT';rights='Per-item rights; NC limits may apply';notes='Catalogue first; no bulk images.'},
@{id='DLA-015';title='Kriti Sampada manuscript catalogue';url='https://www.namami.gov.in/manuscript-database';status='CATALOGUE_DISCOVERY_ONLY';path='01_RAW_DATA\12_MANUSCRIPTS\Kriti-Sampada';rights='Image rights separate from metadata';notes='Identify exact item and holding institution.'},
@{id='DLA-017';title='Kaggle uTHCD Tamil handwriting';url='https://www.kaggle.com/competitions/tamil-hwcr/data';status='LOGIN_AND_RULES_REVIEW';path='01_RAW_DATA\13_OCR\Kaggle-uTHCD';rights='Competition rules and authenticated access';notes='Isolated handwriting is not inscription or palm-leaf data; no scraping.'},
@{id='DLA-012';title='Tamil Nadu WRD Tank Information System';url='https://tngis.tn.gov.in/wrd/';status='PERMISSION_AND_API_REVIEW';path='01_RAW_DATA\03_GEOSPATIAL';rights='Permission sensitive until confirmed';notes='No scrape or republication before authorization.'},
@{id='DLA-016';title='Open Heritage 3D';url='https://openheritage3d.org/data';status='ITEM_SELECTION_AND_LICENSE_REVIEW';path='01_RAW_DATA\14_HERITAGE_3D\Open-Heritage-3D';rights='Dataset-specific licence';notes='Select exact site; check size, capture metadata and licence.'}
)
foreach($g in $gated){$path=Join-Path $Root $g.path;$exists=Test-Path -LiteralPath $path;$Rows.Add([pscustomobject]@{session_id=$Session;dataset_id=$g.id;title=$g.title;source_url=$g.url;status=$g.status;relative_path=$g.path;exists=$exists;size_bytes=0;sha256='';rights_status=$g.rights;notes=$g.notes});Event $g.status $g.id $g.notes $g.path}
@'
PHYSICAL REPRESENTATION — DECISION STATUS
Judy ma'am is exploring a physical-representation path. Current direction from the team is software and data-lake collection first; no display purchase or final selection is approved.

Pepper's Ghost: a floating-image illusion produced by reflecting a concealed display in an inclined transparent reflector. Strong for a focal monument/story moment; limited viewing cone, alignment, ambient-light/contrast sensitivity; not a true volumetric hologram or a landscape base.

Projection-mapped physical relief: physical terrain/landscape geometry overlaid with calibrated projected data. Stronger for geography, relative elevation, water, settlement and routes; sensitive to calibration, occlusion, room light and physical model design.

Hybrid: relief projection as main landscape, optional Pepper's Ghost focal layer, separate evidence display and deterministic physical controls. Most promising only if low-cost independent tests show measurable comprehension benefit worth the complexity.

Provisional recommendation: maintain presentation-neutral software. Compare Pepper's Ghost and projection-mapped relief using the same source-backed scene; test hybrid only afterwards. Expose source, uncertainty and evidence class on a separate accessible screen. Do not purchase hardware before tests.
'@ | Set-Content -LiteralPath (Join-Path $Root '05_PHYSICAL_REPRESENTATION\research\Physical-Representation-Decision-Note.txt') -Encoding utf8NoBOM
$Rows | Export-Csv -LiteralPath $Manifest -NoTypeInformation -Encoding utf8NoBOM
if($HashRows.Count -gt 0){$HashRows|Export-Csv -LiteralPath $Hashes -NoTypeInformation -Encoding utf8NoBOM}
$okCount=@($Rows|Where-Object{$_.status -in @('DOWNLOADED_VALIDATED','SKIPPED_EXISTING_VALID')}).Count
$failCount=@($Rows|Where-Object{$_.status -like 'FAILED*'}).Count
$gateCount=@($Rows|Where-Object{$_.status -match 'MANUAL|REVIEW|REQUIRED|GATED|CATALOGUE|PERMISSION|LOGIN|ITEM_SELECTION'}).Count
$summaryRel="docs\collection-runs\critical-session-$Session-summary.md"
$summary=@"
# Neer-Nilam Critical Session $Session

- Validated or pre-existing assets: $okCount
- Failed assets: $failCount
- Manual/rights/access gates: $gateCount
- Local manifest: 00_ADMIN/manifests/critical-session-$Session.csv
- Local checksums: 00_ADMIN/checksums/critical-session-sha256-$Session.csv

This run reorganizes existing datasets while retaining legacy paths, appends Log.txt, copies the Word dossier, and attempts a selected 2016-2025 monthly CHIRPS baseline, official Tamil Nadu statistical PDFs, dynamic CGWB yearbook link resolution and one WorldCover tile candidate. Files must pass PDF/TIFF signature and size validation. JRC water, Copernicus DEM, Census, archival maps, manuscripts, Kaggle, TNGIS and Open Heritage 3D remain manually gated.

Modern climate, groundwater, crop, land-cover, OSM and HydroRIVERS datasets are context, not direct evidence of ancient conditions. DHARMA README-versus-XML licence conflicts remain unresolved. Review manifest, JSONL log, checksums and quarantined files before claiming success.
"@
Set-Content -LiteralPath (Join-Path $Repo $summaryRel) -Value $summary -Encoding utf8NoBOM
$runManifest=Join-Path $RunDir "critical-session-$Session-manifest.csv"
$runHashes=Join-Path $RunDir "critical-session-$Session-checksums.csv"
$runLog=Join-Path $RunDir "critical-session-$Session-Log.txt"
Copy-Item -LiteralPath $Manifest -Destination $runManifest -Force
if(Test-Path -LiteralPath $Hashes -PathType Leaf){Copy-Item -LiteralPath $Hashes -Destination $runHashes -Force}
Event 'COMPLETE' 'P0-SESSION' "Validated/present=$okCount; failed=$failCount; manual/gated=$gateCount. Review session log and manifest." ("07_LOGS\critical-session-$Session.jsonl")
Copy-Item -LiteralPath $Log -Destination $runLog -Force
if($PublishMetadata){
 & git -C $Repo diff --cached --quiet
 if($LASTEXITCODE -ne 0){Event 'PUBLISH_SKIPPED' 'GITHUB' 'Pre-staged changes found; did not commit or push.'}
 else{
  $publish=Read-Host 'Publish only this session summary, manifest, checksum list and Log snapshot to GitHub? Type PUBLISH-METADATA'
  if($publish -ceq 'PUBLISH-METADATA'){
   & git -C $Repo add -- $summaryRel ("docs\collection-runs\critical-session-$Session-manifest.csv") ("docs\collection-runs\critical-session-$Session-checksums.csv") ("docs\collection-runs\critical-session-$Session-Log.txt")
   if($LASTEXITCODE -eq 0){& git -C $Repo commit -m "data(log): record critical session $Session";if($LASTEXITCODE -eq 0){& git -C $Repo push origin main;if($LASTEXITCODE -eq 0){Event 'PUBLISHED' 'GITHUB' 'Only metadata was published; raw datasets were not staged.'}else{Event 'PUBLISH_FAILED' 'GITHUB' 'Push failed; inspect local commit.'}}}
  }else{Event 'PUBLISH_NOT_AUTHORIZED' 'GITHUB' 'Metadata not pushed because confirmation did not match.'}
 }
}else{Event 'PUBLISH_NOT_REQUESTED' 'GITHUB' 'Review output then rerun with -PublishMetadata if desired.'}
Write-Host ''
Write-Host 'Critical session ended. Inspect the manifest, JSONL log, checksum CSV and Log.txt before ejecting.' -ForegroundColor Green
