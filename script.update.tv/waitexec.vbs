'
' Waits for kodi exit and then execute the provided command in args
'
On Error Resume Next

Dim oshell
Set oshell = wscript.CreateObject ("WScript.shell")

sQuery = "select * from win32_process where name='kodi.exe'"
Set svc = getobject("winmgmts:root\cimv2")

Dim count
count = 1
Do
	If (count mod 7) = 0 then
		oshell.run "taskkill /f /im kodi.exe", 0 , True
	End If
	count = count + 1
    wscript.sleep 1000
    Set cproc = svc.execquery(sQuery)
Loop Until cproc.count <> 1

Set svc=Nothing

oshell.run wscript.arguments(0)
