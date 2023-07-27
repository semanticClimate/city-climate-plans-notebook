#!/bin/bash
# @name: render.sh
# @creation_date: 2023-01-18
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Runs Jupyter Notebook and renders in Quarto
# @acknowledgements:
# https://www.redhat.com/sysadmin/arguments-options-bash-scripts

############################################################
# subprograms                                              #
############################################################
License()
{
  echo 'Copyright 2023 Simon Bowie <ad7588@coventry.ac.uk>'
  echo
  echo 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:'
  echo
  echo 'The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.'
  echo
  echo 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'
}

Help()
{
   # Display Help
   echo "This script runs Jupyter Notebook and renders in Quarto"
   echo
   echo "Syntax: render.sh [-l|h|r|z]"
   echo "options:"
   echo "l     Print the MIT License notification."
   echo "h     Print this Help."
   echo "r     Run full execute and render process (using Docker Compose)."
   echo "z     Run full execute and render process (using local installation)."
   echo
}

Run_Jupyter()
{
  docker exec -i $JUPYTER_CONTAINER jupyter nbconvert --to notebook --execute $JUPYTER_FILE
}

Render_Quarto()
{
  quarto render
}

Render_Quarto_Docker()
{
  docker exec -i $QUARTO_CONTAINER quarto render ./input
}

Push_GitHub()
{
  git add .
  git commit -m "$COMMIT_MESSAGE"
  git push origin main
}

############################################################
############################################################
# main program                                             #
############################################################
############################################################

# set variables
JUPYTER_CONTAINER=jupyterlab
JUPYTER_FILE=*_press.ipynb
QUARTO_CONTAINER=quarto
COMMIT_MESSAGE='automated site update'

# error message for no flags
if (( $# == 0 )); then
    Help
    exit 1
fi

# get the options
while getopts ":hlrz" flag; do
   case $flag in
      l) # display License
        License
        exit;;
      h) # display Help
        Help
        exit;;
      r) # run whole process (Docker)
        Run_Jupyter
        Render_Quarto_Docker
        Push_GitHub
        exit;;
      z) # run whole process (local)
        Run_Jupyter
        Render_Quarto
        Push_GitHub
        exit;;
      \?) # Invalid option
        Help
        exit;;
   esac
done
