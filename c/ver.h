// Copyright 2017 Emzi0767
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#ifdef __cplusplus
extern "C"
{
#endif

#define PROGRAM_NAME "Cryptic Costume Utility"
#define PROGRAM_VERSION "v1.0"
#define PROGRAM_AUTHOR "Emzi0767"
#define PROGRAM_SOURCE "https://github.com/Emzi0767/CrypticCostumeUtils"
#define PROGRAM_LICENSE "Apache License 2.0"
#define PROGRAM_LICENSE_URL "https://github.com/Emzi0767/CrypticCostumeUtils/blob/master/LICENSE.TXT"

// Prints out the program name, version, author, source, and license info
void print_header(void);

// Prints out program usage instructions
void print_usage(char* prog_name);

#ifdef __cplusplus
}
#endif
