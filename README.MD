# Cryptic Costume Tools
Tools that allow unpacking and repacking of costume data from saved Star Trek Online (and potentially other Cryptic 
titles') saved costume files.

The costume data itself is written into a proprietary extension of the JPEG file, more information can be found in 
`specification/spec.txt` file (these are rough notes, but should give you an idea of how to implement your own 
packer and unpacker, should you desire to do so). 

The supplied Python script is a very rough implementation, there is a lot of room for improvement.

## Requirements
In the `scripts` directory, there's a file called `process.py`. It's a Python script, and requires a copy of Python 3.6 
to be available on your system. You can download it from [Python's official website](https://www.python.org/) or, if 
using GNU/Linux or other UNIX-like system, install it using your system's package manager, or compile from sources.

## Usage
Simply invoke the script with required arguments:

* **Unpacking**: `python process.py unpack source.jpg target.json`
* **Packing**: `python process.py pack source.json target.jpg`

Unpacking will extract the data from the JPEG, and output them to the specified JSON file. You can then edit the file 
according to your desires.

Packing requires both target and source file to exist. It will read the data from the specified JSON file, create a 
backup of the JPEG file, then modify the JPEG file with data from the JSON.

## Notes
This is created based on reverse engineering, bad documentations, and digging into proprietary standards. It is not 
guaranteed to work. If you happen to encouter a problem, open an issue, describe the problem, and attach the file you 
were trying to convert.