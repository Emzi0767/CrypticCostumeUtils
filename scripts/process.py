# Copyright 2017 Emzi0767
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Imports
from typing import List, Dict, Any
from struct import unpack, pack
from time import time
from json import loads, dumps
from sys import argv
from os import stat
from os.path import basename, abspath, dirname, join, isfile
from shutil import copyfile as cp


# Definitions
__version__     = "1.0.0"
__author__      = "Emzi0767"
__source__      = "https://github.com/Emzi0767/CrypticCostumeUtils"
__license__     = "Apache License 2.0"
__license_url__ = f"{__source__}/blob/master/LICENSE.TXT"


# Data structures
class IptcTag:
    def __init__(self, record_number: int, tag: int, size: int, data: bytes):
        self.record_number = record_number
        self.tag = tag
        self.size = size
        self.data = data
    
    def to_bytes(self) -> bytes:
        data = pack(">BBBH", 0x1C, self.record_number, self.tag, self.size)
        data += self.data
        
        return data
    
    def __str__(self):
        return f"IPTC Tag: Record number {self.record_number}; Tag {self.tag}; Data size {self.size}"
    
    def __repr__(self):
        return self.data.decode("ascii")


class CrypticCostume:
    def __init__(self, tags: List[IptcTag]):
        if tags:
            self.version = unpack(">H", tags[0].data)[0]
            self.game_name = tags[1].data.decode("ascii")
            self.game_id = tags[2].data.decode("ascii")
            self.gender = tags[3].data.decode("ascii")
            
            i = 4
            if len(tags) == 9:
                self.species = tags[i].data.decode("ascii")
                i += 1
            
            else:
                self.species = None
            
            self.account = tags[i].data.decode("ascii")
            i += 1
            
            self.character = tags[i].data.decode("ascii")
            i += 1
            
            self.uid = tags[i].data.decode("ascii")
            i += 1
            
            self.data = tags[i].data.decode("ascii")
            i += 1
        
        else:
            self.version = 0
            self.game_name = None
            self.game_id = None
            self.gender = None
            self.species = None
            self.account = None
            self.character = None
            self.uid = None
            self.data = None
    
    def to_tags(self) -> List[IptcTag]:
        game_name = self.game_name.encode("ascii")
        game_id = self.game_id.encode("ascii")
        gender = self.gender.encode("ascii")
        species = self.species.encode("ascii") if self.species else None
        account = self.account.encode("ascii")
        character = self.character.encode("ascii")
        uid = self.uid.encode("ascii")
        data = self.data.encode("ascii")
    
        tags = [
            IptcTag(2, 0, 2, pack(">H", self.version)),
            IptcTag(2, 25, len(game_name), game_name),
            IptcTag(2, 25, len(game_id), game_id),
            IptcTag(2, 25, len(gender), gender)
        ]
        
        if species:
            tags.append(IptcTag(2, 25, len(species), species))
        
        tags += [
            IptcTag(2, 120, len(account), account),
            IptcTag(2, 120, len(character), character),
            IptcTag(2, 120, len(uid), uid),
            IptcTag(2, 202, len(data), data)
        ]
        
        return tags
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "game": {
                "name": self.game_name,
                "id": self.game_id
            },
            "character": {
                "gender": self.gender.split(":")[1],
                "species": self.species.split(":")[1] if self.species else None
            },
            "owner": {
                "account": self.account,
                "character": self.character,
                "uid": self.uid
            },
            "data": self.data
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]):
        cc = CrypticCostume([])
        cc.version = data["version"]
        cc.game_name = data["game"]["name"]
        cc.game_id = data["game"]["id"]
        cc.gender = "Gender:" + data["character"]["gender"]
        cc.species = ("Species:" + data["character"]["species"]) if data["character"]["species"] else None
        cc.account = data["owner"]["account"]
        cc.character = data["owner"]["character"]
        cc.uid = data["owner"]["uid"]
        cc.data = data["data"]
        
        return cc
    
    def __str__(self):
        gender = self.gender.split(":")[1]
        species = self.species.split(":")[1] if self.species else None
        
        data = f"Costume <Version={self.version}; Game={self.game_name}/{self.game_id}; Gender={gender}; "
        
        if species:
            data += f"Species={species}; "
        
        data += f"Author={self.character}@{self.account}; UID?={self.uid}>"
        
        return data
    
    def __repr__(self):
        return self.data


# Extractor
def extract_costume(filename: str) -> CrypticCostume:
    # Check if JPEG
    if filename[-4:].lower() != ".jpg" and filename[-5:].lower() != ".jpeg":
        raise IOError("Input file must be JPEG.")
    
    # Check if any data inside
    filedata = stat(filename)
    filesize = filedata.st_size
    if filesize < 4:
        raise IOError("File too short.")
    
    # Read all the data
    with open(filename, "rb") as f:
        imgdata = f.read()
    
    # Check if valid JPEG file
    if imgdata[0] != 0xFF or imgdata[1] != 0xD8 or imgdata[filesize - 2] != 0xFF or imgdata[filesize - 1] != 0xD9:
        raise IOError("Input data is not a valid JPEG file.")
    
    # Locate APP13 marker
    i = 0
    while imgdata[i] != 0xFF or imgdata[i + 1] != 0xED:
        i += 1
    
    # If end was reached without locating the marker, marker was not found
    if i >= filesize:
        raise IOError("APP13 marker not found.")
    
    # Trim the image to contain just APP13 data
    imgdata = imgdata[i:]
    datasize = unpack(">H", imgdata[2:4])[0]
    imgdata = imgdata[2:datasize + 2]
    
    # Read APP13 data header
    i = 2
    while imgdata[i] != 0x00:
        i += 1
    
    # Check if valid
    sig1 = imgdata[2:i].decode("ascii")
    if sig1 != "Photoshop 3.0":
        raise IOError(f"Invalid APP13 marker type ('{sig1}' != 'Photoshop 3.0').")
    
    # Read APP13 data magic and check if valid
    i += 1
    sig2 = imgdata[i:i + 4].decode("ascii")
    if sig2 != "8BIM":
        raise IOError(f"Invalid APP13 marker sub-type ('{sig2}' != '8BIM').")
    
    # Check APP13 data type and check if valid
    i += 4
    hdata = unpack(">H", imgdata[i:i + 2])[0]
    if hdata != 0x0404:
        raise IOError(f"Invalid IRB type ('0x{hdata:04x}' != '0x0404')")
    
    # Get APP13 data name
    i += 2
    hnamelen = imgdata[i]
    i += 1
    hname = imgdata[i:i + hnamelen].decode("ascii")
    i += hnamelen
    if hnamelen % 2 != 1:
        i += 1
    
    # Get APP13 data length
    datalen = unpack(">I", imgdata[i:i + 4])[0]
    i += 4
    imgdata = imgdata[i:i + datalen]
    
    # Extract IPTC tags from the data
    i = 0
    tags = []
    while i < datalen:
        if imgdata[i] != 0x1C:
            break
        
        tagdata = unpack(">BBH", imgdata[i + 1:i + 5])
        tags.append(IptcTag(tagdata[0], tagdata[1], tagdata[2], imgdata[i + 5:i + 5 + tagdata[2]]))
        i += 5 + tagdata[2]
    
    # Return the extracted tags
    return CrypticCostume(tags)


# Packer
def pack_costume(costume: CrypticCostume) -> bytes:
    # Convert the costume to tags
    tags = costume.to_tags()
    
    # Build the APP13 header
    data = b'Photoshop 3.0\x008BIM\x04\x04\x00\x00'
    
    # Convert the tags to bytes
    tagb = b''
    for tag in tags:
        tagb += tag.to_bytes()
    
    # Even out the tag data length
    if len(tagb) % 2 != 0:
        tagb += b'\x00'
    
    # Appen the tag data length
    data += pack(">I", len(tagb))
    data += tagb
    
    # Create APP13 extension
    data = b'\xFF\xED' + pack(">H", len(data) + 2) + data
    
    # Return the created extension
    return data


# Misc
def json_predicate(obj: Any) -> Dict[str, Any]:
    return obj.to_dict()


def graft_app13(imgdata: bytes, graft: bytes) -> bytes:
    # Check if any data inside
    if not imgdata:
        raise IOError("File too short.")
    
    # Check if valid JPEG file
    if imgdata[0] != 0xFF or imgdata[1] != 0xD8 or imgdata[len(imgdata) - 2] != 0xFF or imgdata[len(imgdata) - 1] != 0xD9:
        raise IOError("Input data is not a valid JPEG file.")
    
    # Locate APP13 marker
    i = 0
    while imgdata[i] != 0xFF or imgdata[i + 1] != 0xED:
        i += 1
        
    # If end was reached without locating the marker, marker was not found
    if i >= len(imgdata):
        raise IOError("APP13 marker not found.")
    
    # Get the data before APP13 extension
    datab = imgdata[:i]
    
    # Get APP13 extension length
    hsize = unpack(">H", imgdata[i + 2:i + 4])[0] + 2
    
    # Get the data after APP13 extension
    dataa = imgdata[i + hsize:]
    
    # Create a JPEG file
    return datab + graft + dataa
    

# Entry point
if __name__ == "__main__":
    if len(argv) >= 4:
        operation = argv[1]
        input_fn = abspath(argv[2])
        output_fn = abspath(argv[3])
    
    else:
        operation = None
        input_fn = None
        output_fn = None
    
    print(f"Cryptic Costume Unpacker v{__version__} by {__author__}")
    print(f"Source code available at {__source__}")
    print(f"Licensed under {__license__} (see {__license_url__} for details")
    print("")
    
    if operation == "unpack" and input_fn and output_fn:
        input = input_fn
        output = output_fn
        
        input_fn = basename(input)
        output_fn = basename(output)
        
        if not isfile(input):
            print("Source file does not exist!")
            exit()
    
        print("Unpacking costume")
        print(f"Source:      {input_fn}")
        print(f"Destination: {output_fn}")
        
        data = extract_costume(input)
        print("Decoded costume:")
        print(str(data))
        
        with open(output, "w", encoding="utf-8") as f:
            f.write(dumps(data, default=json_predicate))
    
    elif operation == "pack" and input_fn and output_fn:
        input = input_fn
        output = output_fn
        
        input_fn = basename(input)
        output_fn = basename(output)
        
        if not isfile(input):
            print("Source file does not exist!")
            exit()
        
        if not isfile(output):
            print("Target file does not exist!")
            exit()
        
        backup_fn = output_fn + "." + str(int(time())) + ".bak"
        backup = join(dirname(output), backup_fn)
    
        print("Packing costume")
        print(f"Source:      {input}")
        print(f"Destination: {output}")
        
        with open(input, "r", encoding="utf-8") as f:
            data = f.read()
        
        data = loads(data)
        data = CrypticCostume.from_dict(data)
        print("Loaded costume:")
        print(str(data))
        
        print(f"Making a backup of target file at '{backup_fn}'")
        cp(output, backup)
        
        print("Packing the costume")
        data = pack_costume(data)
        
        print("Reading target file")
        with open(output, "rb") as f:
            base = f.read()
        
        print("Grafting the data onto target file")
        data = graft_app13(base, data)
        
        print("Writing output file")
        with open(output, "wb") as f:
            f.write(data)
    
    else:
        script = basename(argv[0])
        print("Usage:")
        print("")
        print("To unpack a file:")
        print(f"  {script} unpack source.jpg target.json")
        print("  Source JPEG file must exist and contain a saved costume. The target file will be overwritten.")
        print("")
        print("To pack a file:")
        print(f"  {script} pack source.json target.jpg")
        print("  Both source JSON and target JPEG file must exist. A backup file of the JPEG will be created alongside the patched file.")
