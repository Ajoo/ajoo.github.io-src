@echo off
cd output
for %%i in (*) do if not "%%i" == "CNAME" del %%i
for /d %%i in (*) do rmdir /s /q %%i
cd ..