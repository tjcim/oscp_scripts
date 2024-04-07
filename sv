#!/usr/bin/env fish

set -eg ip
set -e lip
set -e uports
set -e ports
set -g _ip

if count $argv > /dev/null
  set -g _ip $argv[1]
else
  ## IP
  read -l _ip --prompt-str="What is the remote IP?: "
  set -g _ip $_ip
end

# Only set the $IP variable if the $ip is not empty
if test -n "$_ip"; set -Ux ip {$_ip}; end

## LIP
set -Ux lip (ip -4 a show tun0 | grep -Po 'inet \K[\d.]+')
