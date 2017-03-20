## Description
- A Simplicial Complex module implemented by C++

## API Description - SCExport (.so)
- createInstance: Create an instance of SimplicialComplex
  output: instance of SimplicialComplex -> objType
- removeInstance: Release resources of instance
  input: instance of SimplicialComplex -> objType
- initialize: Initialize the instance by taking some necessary parameters
  input: instance of SimplicialComplex -> objType
         number of rules -> int
         threshold -> float
         number of columns -> int
         number of rows -> int
         input file path (set NULL is there is no input file) -> string
- setBitMapRow: Set the bit-vector directly row-by-row
  input: instance of SimplicialComplex -> objType
         number of columns -> int
         which row of this bit-vector -> int
         bit-vector data (string vector) -> string
- process: Do the process of Simplicial Complex
  input: instance of SimplicialComplex -> objType

## Example usage
- Please refers to main.cpp as more detail of usage.
- There are two different ways of input to use this module
1. set a file input in initialize() without call setBitMapRow()
2. set NULL in file path in initialize() and call setBitMapRow() in your loop
- General calling sequence is: createInstance() -> initialize() -> setBitMapRow() -> ... -> 
                               process() -> removeInstance()
- The output will be written into a file, results.txt.
- The format of the input file is referred to ../data/dataSample-small1.dat