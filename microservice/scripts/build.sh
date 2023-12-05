#!/bin/bash
set -euxo pipefail
scriptdir=$(cd $(dirname $0) && pwd)

$scriptdir/build-python.sh
