#!/bin/bash

set -e

echo "Generating runtimes"
python build-rts.py --rts-src-descriptor=bb-runtimes/gnat_rts_sources/lib/gnat/rts-sources.json nrf52832 nrf52833 nrf52840

for target in nRF52832 nRF52833 nRF52840; do
    for profile in light light-tasking embedded; do
        echo "Crateifying ${profile}-${target,,}"
        python crateify.py --runtime-dir=install/${profile}-${target,,} --profile=${profile} --pretty-target=${target}
    done
done