for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q server.db