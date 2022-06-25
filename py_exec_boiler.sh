#!/bin/sh

numofpuzzles=1

# We need a file name
if [[ -z $1 ]]
then
  echo "Provide a destination directory name"
  exit 1
fi

if [ ! -z $2 ]
then
  numofpuzzles=$2
fi

# Easier copy pasting
add_empty_lines () {
  echo "" >> "$1"
  echo "" >> "$1"
}

add_boiler_plate () {
  # Python executable path
  echo "#!${PYTHON}" > "$1"

  # Make it pretty
  add_empty_lines "$1"

  # Create the number of functions as placeholders
  for i in $(seq ${numofpuzzles:-1})
  do
    # The first function is the main puzzle, let's name it main
    if [ $i -eq 1 ];
    then
      echo "def main():" >> "$1"
    else
      # Everything else is genericly named puzzle + number of puzzle without counting the first one
      puzzleNum=$((i - 1))
      echo "def puzzle${puzzleNum}():" >> "$1"
    fi
    echo "  pass" >> "$1"

    # Make it pretty
    add_empty_lines "$1"
  done

  # Make the script module based, because you never know I guess
  echo "if __name__ == \"__main__\":" >> "$1"

  # Same logic as the above loop, but now we only call the functions
  for i in $(seq ${numofpuzzles:-1})
  do
    if [ $i -eq 1 ];
    then
      echo "  main()" >> "$1"
    else
      # By default, every function other than main is commented out
      puzzleNum=$((i - 1))
      echo "  # puzzle${puzzleNum}()" >> "$1"
    fi
  done

  # Make the file executable
  chmod +x "$1"
}

# Get working dir
PWD=$(pwd)
# File name and path
SOLUTION="$PWD/$1/solution.py"
PRETTY="$PWD/$1/pretty.py"
# Create the file
touch "$SOLUTION"
touch "$PRETTY"
# Get the python path
PYTHON=$(which python)

# Create the files
add_boiler_plate "$SOLUTION" $2
add_boiler_plate "$PRETTY"   $2

# Remind to rename functions in pretty
echo "# TODO: Rename functions to make them intuitive!" >> "$PRETTY"

# Let the user know this is done
echo "Your files can be found here:"
echo "$SOLUTION"
echo "$PRETTY"

