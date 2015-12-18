#!/usr/bin/env bash
source ./venv/bin/activate
output=$(python tests.py $1 3>&1 1>&2 2>&3 | tee /dev/stderr)

regex='^.*FAILED.{1}\(failures|errors=[0-9]+\)$'
if [[ $output =~ $regex ]]
then
    # There is at least one unit test FAILURE or ERROR.
    # Do not run the app.
    echo ""
    echo "NAUGHTY! NAUGHTY! NAUGHTY!"
    echo "YOU ARE FORBIDDEN TO RUN THE APP UNTIL ALL TEST CASES PASS."
    echo ""
else
    # There are no unit test errors, let's run the app.
    python run.py "--debug"
fi