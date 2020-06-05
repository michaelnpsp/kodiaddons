'
' Waits for kodi exit and then execute the provided command in args
'
On Error Resume Next

sQuery="select * from win32_process where name='kodi.exe'"
Set svc=getobject("winmgmts:root\cimv2")
Do
    wscript.sleep 1000
    Set cproc=svc.execquery(sQuery)
Loop Until cproc.count <> 1
Set svc=Nothing

Dim objShell
Set objShell = WScript.CreateObject ("WScript.shell")
objShell.run wscript.arguments(0)
