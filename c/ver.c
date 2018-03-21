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

// Standard library
#include <stdio.h>

// Corresponding header
#include "ver.h"

void print_header(void)
{
	printf("%s %s by %s\n", PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_AUTHOR);
	printf("Source code available at %s\n", PROGRAM_SOURCE);
	printf("Licensed under %s (see %s for details)", PROGRAM_LICENSE, PROGRAM_LICENSE_URL);
	puts("");
}

void print_usage(char* prog_name)
{
	puts("Usage:");
	printf("  %s <mode> <source file>\n", prog_name);
	puts("");
	puts("  mode            Operation mode. Either unpack or pack.");
	puts("  source file     Source file. When unpacking, it's the JPEG");
	puts("                  file which contains costume data. When");
	puts("                  packing, it's the DATA file with costume");
	puts("                  data.");
	puts("");
	puts("When packing, the JPEG file specified by the DATA file must ");
	puts("exist. A backup JPEG file will be created from the original.");
}
