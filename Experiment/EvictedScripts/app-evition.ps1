$packageOutput = $(adb -s $args[0] shell pm list packages)

$packageOutput | ForEach-Object {
    $package = $_ -replace '^package'
    if ($package -match 'com.uma.(.+)'){
        adb -s $args[0] shell am force-stop $matches[0]
    }
}