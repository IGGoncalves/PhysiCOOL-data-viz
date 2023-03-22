
## Parsing output files
### Creating the output file name:
PhysiCell saves outputs as "output00000000_cells.mat", "output00000001_cells.mat", ... 
In other words, 8 digits are used to represent the current time point. Python has a method to automatically build
an X-digit string from a number, named `"zfill(X)"` that takes `X` (the number of digits) as input and pads it with as 
many zeroes as necessary to reach `X`.

For example:
- `"12".zfill(3)` -> The string will have 3 digits. "12" already has 2 digits, so zfill()
    will add 1 zero to the beginning of the string, making it "012".
- `"1".zfill(5)` -> The string will have 5 digits. "1" only has 1 digit, so 4 zeroes need to be
added, making it "00001".

See [the Python string documentation](https://docs.python.org/3/library/stdtypes.html#str.zfill).

### Working with Path and strings

### Accessing XML values