# PythonTester
 A tool to make a Python tester from any Python script!

This library generates a tester for any Python script. To use it, pass the path
to the file you want to use as a "baseline" file (a .py file that returns the
output you want, given the inputs you want). This script generates a tester
file, which you can share with others so they're able to see if their scripts'
outputs are similar to yours. The tester file has the original baseline file
built-in (as bytecode, so people can't just copy-paste the given code), along
with the JSON tests. Sharing the outputted file standalone should be enough.

# Why don't ALL scripts work?

To preserve compatibility between Python versions while keeping an acceptable
level of obfuscation (so people can't just copy paste your code when you send
them your tester), the "baseline" script you pass in is converted into
non-standard bytecode (which isn't really Python bytecode!). This is done
directly with Python's `ast` module, which provides source code parsing
functionality across versions. 

Due to this, things like functions aren't yet implemented. They are, however,
being planned for the future.
