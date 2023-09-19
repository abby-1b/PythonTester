from sys import argv
from types import CodeType
import re

LOOK_BACK_LINES = 4
LOOK_AHEAD_LINES = 3
IGNORE_WHITESPACE = r" |\t|\n(?=\n+)|\n(\s+)(?=\n+)"

YELLOW = "\u001b[33m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
RESET = "\u001b[0m"

# Check if the user didn't pass a file to run
if len(argv) < 2:
	print(
		YELLOW + "Please pass the file you'd like to run.\n" +
		"For example:\n" + GREEN + "python testing.py your_code.py" + RESET
	)
	exit()

# Get the code from the passed input file
input_code: str = ""
input_file = argv[1]
try:
	input_code = open(input_file).read()
except:
	# If it doesn't exist, throw a message and exit
	print(f"The file {input_file} doesn't seem to exist.")
	exit()

# Check if two strings are equal, according to 
def outputs_equal(
	expected: str,
	gotten: str
) -> bool:
	exp_str = re.sub(IGNORE_WHITESPACE, "", expected)
	got_str = re.sub(IGNORE_WHITESPACE, "", gotten  )
	return exp_str == got_str

# Run the code, but with the input replaced in eval
def test_code(
	# The code we're testing
	input_code: str | CodeType,

	# The lines we pass to the input
	input_override_lines: list[str]
) -> str:
	test_output = ""
	
	# This is here so we can exit the `exec` at any time, without exiting
	# from the main Python thread.
	class ExecInterrupt(Exception):
		pass

	# The index of the line we're passing to the input
	testing_idx: int = 0

	# Whether or not all the inputs have been used up. This is used as a
	# fallback (/workaround?) for when the `input()` is called inside a
	# try/except block, which causes `raise ExecInterrupt` to not work.
	is_input_done = False

	# Replaces the `print` function, and instead retur
	def print_override(
		*values: object,
		sep: str = " ",
		end: str = "\n",
	) -> None:
		nonlocal is_input_done
		nonlocal test_output
		out = sep.join([str(v) for v in values]) + end
		if not is_input_done: test_output += out
		# print(out, end="") # Testing

	def input_override(p: object) -> str:
		nonlocal is_input_done
		nonlocal testing_idx

		if is_input_done:
			return ""

		# If we're over the number of lines, loop back around
		if testing_idx >= len(input_override_lines):
			print_override(p)
			is_input_done = True
			raise ExecInterrupt

		# Get the line of input we're on
		v = input_override_lines[testing_idx]
		testing_idx += 1 # Add 1 to the line we're on

		# Print the original input string, plus the input we're passing
		print_override(str(p) + v)

		return v # Return the value

	# Run the code until ExecInterrupt is thrown (thrown by input_override)
	try:
		exec(input_code, {
			"input": input_override,
			"print": print_override,
		})
	except ExecInterrupt:
		pass

	return test_output

# Colorizes a string (including its whitespace!)
def colorize_str(s: str, color: str) -> str:
	return color + s \
		.replace("\t", "    ") \
		.replace(" ", "\u001b[2m•\u001b[22m" + color) \
		.replace("\n", "\u001b[2m\u21B2\u001b[22m" + color)

# Checks if a line is empty
def is_line_empty(line: str):
	return len(line.strip()) == 0

# Checks if two lines aren't equal (so we know that's where the issue is)
def lines_not_equal(l1: str, l2: str) -> bool:
	whitespace_regex = r" |\t"
	l1 = re.sub(whitespace_regex, "", l1).casefold()
	l2 = re.sub(whitespace_regex, "", l2).casefold()
	return l1 != l2

# Checks if two lines aren't equal (see above)
def chars_not_equal(c1: str, c2: str) -> bool:
	return c1 != c2

# Prints an inequality, but pretty!
def print_ineq(
	expected: str,
	gotten: str
):
	# Split the lines
	lines_exp = expected.split("\n") # The lines we EXPECT
	lines_got = gotten.split("\n") # The lines we GOT

	# The index of the first wrong character in the line
	diff_char_idx = 0

	cl_exp = -1 # The current line of the expected string
	cl_got = -1 # The current line of the gotten string
	while True:
		cl_exp += 1
		cl_got += 1
		while cl_exp < len(lines_exp) and is_line_empty(lines_exp[cl_exp]):
			cl_exp += 1
		while cl_got < len(lines_got) and is_line_empty(lines_got[cl_got]):
			cl_got += 1
		
		if cl_exp >= len(lines_exp) or cl_got >= len(lines_got):
			diff_char_idx = 0
			break
		elif lines_not_equal(
			lines_exp[cl_exp],
			lines_got[cl_got]
		):
			diff_char_idx = 0
			while diff_char_idx < min(
				len(lines_exp[cl_exp]),
				len(lines_got[cl_got])
			):
				if chars_not_equal(
					lines_exp[cl_exp][diff_char_idx],
					lines_got[cl_got][diff_char_idx]
				):
					break
				diff_char_idx += 1
			break

	# Define some pretty constants...
	TAB_SPLIT = "\u001b[0m| "
	TABBED_UP_INDENT = 10 * " " + TAB_SPLIT
	UP_INDENT = 12 * " "

	# Flags to be set for warnings!
	are_lines_missing = False
	are_lines_extra = False

	# Get the lines leading up to the wrong line
	leading_lines = lines_got[max(0, cl_got - LOOK_BACK_LINES):cl_got]
	leading_lines = [
		(TAB_SPLIT if i == 0 else TABBED_UP_INDENT) +
		colorize_str(a + "\n", YELLOW) for i, a in enumerate(leading_lines)
	]
	print("Got:      " + "\n".join(leading_lines))
	if cl_got >= len(lines_got):
		are_lines_missing = True
		print(TABBED_UP_INDENT)
	else:
		print( # Print the wrong line
			TABBED_UP_INDENT + colorize_str(lines_got[cl_got][:diff_char_idx], YELLOW) +
			colorize_str(lines_got[cl_got][diff_char_idx:] + "\n", RED)
		)

	# Print the expected output
	print("\u001b[0m" + UP_INDENT + " " * diff_char_idx + "^")

	trailing_lines = lines_exp[
		cl_exp :
		cl_exp + LOOK_AHEAD_LINES
	]
	trailing_lines = [
		(TAB_SPLIT if i == 0 else TABBED_UP_INDENT) +
		colorize_str(a + "\n", GREEN) for i, a in enumerate(trailing_lines)
	]
	if len(trailing_lines) > 0:
		print("Expected: " + "\n".join(trailing_lines) + RESET)
	else:
		print("Expected: " + TAB_SPLIT + RESET)
		are_lines_extra = True
	
	# Print a warning message :)
	warn_message = ""
	if are_lines_extra:
		warn_message = "you've printed too many lines!"
	elif are_lines_missing:
		warn_message = "you're missing a few lines!"
	elif diff_char_idx > 1:
		warn_message = "this line is partially right"
	if len(warn_message) > 0: print(YELLOW + "Note: " + warn_message + RESET)

	# Note: `•` means there's a space!
	#       `↲` means there's a new line!

# ...
module_final = "PUT_MODULE_HERE"

def run_tests():
	# Count the tests that were failed and passed
	total_tests = 0
	tests_passed = 0
	tests_failed = 0

	# Go through each test
	tests: list[list[str]] = [["PUT_TESTS_HERE"]]
	for test_num, t in enumerate(tests, 1):
		expected_output: str = ""
		try:
			expected_output = test_code(module_final, t).strip()
		except: pass

		code_output: str = ""
		try:
			code_output = test_code(input_code, t).strip()
		except: pass
		
		total_tests += 1
		if outputs_equal(expected_output, code_output):
			tests_passed += 1
		else:
			if tests_failed == 0:
				print("Failed test \u001b[33m#" + str(test_num) + "\u001b[0m")
				print_ineq(expected_output, code_output)
			tests_failed += 1

	# Print the amount of tests passed
	if tests_passed == 0:
		print("Passed " + RED + "0" + RESET + " tests.")
	elif tests_passed == total_tests:
		print("Passed " + GREEN + str(tests_passed) + RESET + " tests.")
	else:
		print("Passed " + YELLOW + str(tests_passed) + RESET + " tests.")

	# Print the amount of tests failed
	if tests_failed == 0:
		print("Failed " + GREEN + "0" + RESET + " tests.")
	elif tests_failed == total_tests:
		print("Failed " + RED + str(tests_failed) + RESET + " tests.")
	else:
		print("Failed " + YELLOW + str(tests_failed) + RESET + " tests.")

	if tests_passed == total_tests:
		# Print a good job message :)
		from random import choice
		print(GREEN + choice([
			"Nice!", "Good job!", "Great!", "Perfect!", "It seems to work!",
			"No issues here!", "Seems to be fine!", "Looks alright!"
		]))

	print(RESET, end="")

if __name__ == "__main__":
	run_tests()
