function prompt {
  $date = "[" + $(Get-Date -UFormat "%H:%M:%S") + "]:"
  $path = "[..]/" + $(Split-Path -leaf -path (Get-Location))
  Write-Host ($date) -nonewline -foregroundcolor Red
  Write-Host ($path) -nonewline -foregroundcolor Green
  return "$ "
}