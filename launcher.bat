::Launcher template

::Get current directory
set mypath=%~dp0

::Set maya plugin path
set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;

::Set python path
set PYTHONPATH=%PYTHONPATH%;%mypath:~0,-1%;

::Start maya
"C:\Program Files\Autodesk\Maya2013.5\bin\maya.exe"