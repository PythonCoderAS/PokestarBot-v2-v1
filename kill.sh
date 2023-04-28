#!/usr/bin/env bash

base="$(dirname "$0")"

pidfile_path="${base}/bot_data/Pidfile"

signal="${1:-2}"

if test -e "${pidfile_path}"
then
  pid="$(cat "$pidfile_path")"
else
  echo Pidfile is missing. Enter in the PID manually. A ps for all python programs hass been provided.
  # shellcheck disable=SC2009
  output=$(ps -A)
  echo "${output}" | grep -i "python"
  read -rp "PID: " pid
fi


kill -"$signal" "$pid"

while ps -p "$pid" > /dev/null 2>&1;
do
  sleep 1
done
rm pidfile_path 2>/dev/null
echo Killed successfully.
