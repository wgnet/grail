trap
{
	deactivate
	rmvirtualenv grail
	write-output $_
	exit 1
}

Import-Module virtualenvwrapper
mkvirtualenv grail

pip install pep8==1.6.2 teamcity-messages==1.12
if ($LastExitCode -ne 0) {
    throw "Failed to install python packages"
}

pip install -e .
if ($LastExitCode -ne 0) {
    throw "Failed to install grail with all required packages"
}

pep8 --ignore=E501 .
if ($LastExitCode -ne 0) {
    throw "There are pep8 errors with grail"
}

cd .
python ./run_tests.py
if ($LastExitCode -ne 0) {
    throw "Tests are failed"
}
