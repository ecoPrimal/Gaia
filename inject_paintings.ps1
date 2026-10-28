$paintings = @(
  @{ file = "249-spirit-eye-octave-spire.jpg"; title = "249: Spirit Eye - Octave of Light, Spire, Null Lens" },
  @{ file = "248-generations-backscatter.jpg"; title = "248: Generations - Backscatter from IS to NULL" },
  @{ file = "247-golgi-inversion-vision.jpg"; title = "247: The Inversion - Golgi Meeting Place + Vision" },
  @{ file = "246-url-is-anatomy.jpg"; title = "246: URL IS Anatomy - Every Symbol a Hook" },
  @{ file = "245-chemistry-salt-cut-guilty-body.jpg"; title = "245: Chemistry - Salt, Cut, Guilty Body, pH Scale" }
)

$dir = "C:\Users\mokke\Desktop\Gaia\paintings"
$results = @()

foreach ($p in $paintings) {
  $path = Join-Path $dir $p.file
  if (Test-Path $path) {
    $bytes = [IO.File]::ReadAllBytes($path)
    $b64 = [Convert]::ToBase64String($bytes)
    $results += @{ b64 = $b64; title = $p.title }
  }
}

# Build JS injection
$js = "var paintings = ["
for ($i = 0; $i -lt $results.Count; $i++) {
  if ($i -gt 0) { $js += "," }
  $title = $results[$i].title -replace "'", "\'"
  $js += "{b64:'" + $results[$i].b64 + "',title:'" + $title + "'}"
}
$js += "];window._gaiaEyeState.paintings=paintings;window._gaiaEyeShowPainting(0);window._gaiaEyeThink('Loaded ' + paintings.length + ' paintings into gallery');'OK:' + paintings.length;"

[IO.File]::WriteAllText("C:\Users\mokke\Desktop\Gaia\inject_paintings.js", $js)
Write-Host "Wrote inject_paintings.js: $($js.Length) chars"
