@echo off

rem Bypass "Terminate Batch Job" prompt on CTRL+C.
if "%~1"=="-FIXED_CTRL_C" (
   rem Remove the -FIXED_CTRL_C parameter
   rem The /1 parameter is needed to prevent the script name (i.e. %0) to
   rem be shifted out and replaced by "-FIXED_CTRL_C"
   shift /1
) ELSE (
   rem Run the batch with <NUL and -FIXED_CTRL_C
   CALL <NUL %0 -FIXED_CTRL_C %*
   GOTO :EOF
)

python3 -m scripts.sync

:EOF