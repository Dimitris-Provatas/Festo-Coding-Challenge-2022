# Festo Coding Challenge 2022

A project of the solutions for the [Festo Coding Challenge 2022](https://2022.coding-challenge.festo.com).

This code is not optimized or well thought out, it is here to get the job done. 😄

This coding challenge is really fun, yet challenging enough to be engaging and interesting. 🔥

The project is written in Python 3.9.7, hence the missing of some "QoL" features, such as `switch` statements.

## Contents

- Each directory is named after the sub-challenge it solves.
- Each directory has 2 files. The `solution.py` is the quick and dirty code to get the answer to the puzzles. The `pretty.py` is an elegant and clean implementation of the solutions.
- The `py_exec_boiler.sh` is an executable shell script I made to create boiler plate code for me. It gets 1-2 arguments, the first being the target directory name and the second (optional) being the number of sub-puzzles. If the second argument is missing, it just creates the main function.
- Since I do not have the rights to any of the puzzle data provided, they are not included in the repo. This repo only contains the code I wrote to solve the puzzles.
- I forgot to include the .vscode directory in the gitignore file, so you will have to live with that 🤙

### Dependencies

Due to the fact that I didn't want to re-invent the wheel, there are some external libraries used in this project. You can easily install all the dependensies by running the following command:

```bash
pip install -r requirements.txt  
```

The Dependencies used are the following:

* SYKE, non, I tried to keep this project as vanilla as posible
