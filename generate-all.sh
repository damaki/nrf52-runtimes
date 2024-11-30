#!/bin/bash

set -e

ARGUMENT_LIST=(
  "version"
)


# read arguments
opts=$(getopt \
  --longoptions "$(printf "%s:," "${ARGUMENT_LIST[@]}")" \
  --name "$(basename "$0")" \
  --options "" \
  -- "$@"
)

eval set --$opts

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version)
      version=$2
      shift 2
      ;;

    *)
      break
      ;;
  esac
done

echo "Generating runtimes"
python build-rts.py \
    --rts-src-descriptor=bb-runtimes/gnat_rts_sources/lib/gnat/rts-sources.json \
    nrf52832 \
    nrf52833 \
    nrf52840

for target in nRF52832 nRF52833 nRF52840; do
    for profile in light light-tasking embedded; do
        echo "Crateifying ${profile}-${target,,}"

        if [[ -z $version ]]; then
            python crateify.py \
                --runtime-dir=install/${profile}-${target,,} \
                --profile=${profile} \
                --pretty-target=${target}
        else
            python crateify.py \
                --runtime-dir=install/${profile}-${target,,} \
                --profile=${profile} \
                --pretty-target=${target} \
                --version=$version
        fi
    done
done