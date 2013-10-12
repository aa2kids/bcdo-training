#!/bin/bash

#Operates similarly on MacOSX.
#Different behavior on the Ubuntu linux box.
#Difference in the way the function is declared.
#If change function declaration to old way
# it works on linux
#  change
# function localizer {
# to
# localizer () {

function localizer {
  echo "==> in function localizer, a starts as '$a'"
  local a
  echo "==> After local declaration, a is '$a'"
  a="localizer version"
  echo "==> Leaving localizer, a is '$a'"
}

a="test"
echo "Before calling localizer, a is '$a'"
localizer
echo "After calling localizer, a is '$a'"
