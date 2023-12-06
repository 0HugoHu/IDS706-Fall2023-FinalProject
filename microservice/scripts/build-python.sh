#!/bin/bash
set -euxo pipefail
scriptdir=$(pwd)


# install CDK CLI from npm, so that npx can find it later
npm install

# Find and build all Python projects
for requirements in $(find $scriptdir/ -name requirements.txt  -not -path "$scriptdir/node_modules/*"); do
    (
        echo "=============================="
        echo "building project: $requirements"
        echo "=============================="

        cd $(dirname $requirements)
        echo "Building project at $(dirname $requirements)"
        [[ ! -f DO_NOT_AUTOTEST ]] || exit 0

        python3 -m venv /tmp/.venv

        source /tmp/.venv/bin/activate
        pip install -r requirements.txt

        $scriptdir/synth.sh
        # It is critical that we clean up the pip venv before we build the next python project
        # Otherwise, if anything gets pinned in a requirements.txt, you end up with a weird broken environment
        rm -rf /tmp/.venv

    )
done
