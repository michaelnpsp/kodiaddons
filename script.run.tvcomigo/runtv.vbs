'
' Waits for kodi exit and then execute the provided command in args
'
On Error Resume Next

'Objects
Set fso = CreateObject("Scripting.FileSystemObject")
Set shl = CreateObject("WScript.Shell")

'Misc funcs
Function find_file(paths)
	For Each file In paths
		if fso.FileExists(file) then
			find_file = file
			Exit Function
		end if
	Next
End Function

'Settings
MUNDOR_URL     = "http://ott.mundo-r.com/nmp_app.html"

MOUSE_SERVER   = find_file( Array("C:\WifiMouseServer\WifiMouseServer.exe", "C:\Program Files (x86)\WifiMouseServer.exe") )

CHROME_BROWSER = find_file( Array("C:\Program Files\Google\Chrome\Application\chrome.exe", "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") )

CHROME_COMMAND = """{1}"" --start-maximized --disable-translate --disable-new-tab-first-run --no-default-browser-check --no-first-run --kiosk ""{2}"""

'Chrome already running ?
Set svc = getobject("winmgmts:root\cimv2")
Set cproc = svc.execquery("select * from win32_process where name='chrome.exe'")
if cproc.count<>0 then
	shl.Run "taskkill /im chrome.exe", 0, False
	WScript.Quit
end if

'Run WifiMouseServer
shl.Run MOUSE_SERVER, 5, False

'Run Chrome+TvComigo
CHROME_COMMAND = Replace(CHROME_COMMAND, "{1}", CHROME_BROWSER)
CHROME_COMMAND = Replace(CHROME_COMMAND, "{2}", MUNDOR_URL)
shl.Run CHROME_COMMAND, 5, True

'Kill WifiMouseServer
shl.Run "taskkill /im WifiMouseServer.exe", 0, False





