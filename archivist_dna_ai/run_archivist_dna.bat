@echo off
REM Run the Archivist DNA AI from its installed path
cd /d "%USERPROFILE%\ArchivistDNA"
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoExit -Command "python archivist_dna.py"
