#!/bin/sh

# We need a file name
if [ -z $1 ]
then
  echo "Provide a file name"
  exit 1
fi

# Easier copy pasting
add_empty_lines () {
  echo "" >> "$FILENAME"
  echo "" >> "$FILENAME"
}

# Get working dir
PWD=$(pwd)
# File name and path
FILENAME="$PWD/$1.py"
# Create the file
touch "$FILENAME"
# Get the python path
PYTHON=$(which python)
echo "#!${PYTHON}" > "$FILENAME"

# Make it pretty
add_empty_lines

# Create the number of functions as placeholders
for i in $(seq ${2:-1})
do
  # The first function is the main puzzle, let's name it main
  if [ $i -eq 1 ];
  then
    echo "def main():" >> "$FILENAME"
  else
    # Everything else is genericly named puzzle + number of puzzle without counting the first one
    puzzleNum=$((i - 1))
    echo "def puzzle${puzzleNum}():" >> "$FILENAME"
  fi
  echo "  pass" >> "$FILENAME"

  # Make it pretty
  add_empty_lines
done

# Make the script module based, because you never know I guess
echo "if __name__ == \"__main__\":" >> "$FILENAME"

# Same logic as the above loop, but now we only call the functions
for i in $(seq ${2:-1})
do
  if [ $i -eq 1 ];
  then
    echo "  main()" >> "$FILENAME"
  else
    # By default, every function other than main is commented out
    puzzleNum=$((i - 1))
    echo "  # puzzle${puzzleNum}()" >> "$FILENAME"
  fi
done

# Make the file executable
chmod +x "$FILENAME"

# Let the user know this is done
echo "Your file can be located here:"
echo "$FILENAME"

