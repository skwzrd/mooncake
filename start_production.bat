@echo off

set this_path=%~dp0

cd %this_path%server
start cmd /k py mooncake.py

cd %this_path%vue
start cmd /k npm run build

start firefox "http://localhost:5000/"
