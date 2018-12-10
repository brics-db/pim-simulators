# Copyright (c) 2018 Till Kolditz
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

CMAKE_MINIMUM_REQUIRED(VERSION 3.8 FATAL_ERROR)

IF(POLICY CMP0048)
    CMAKE_POLICY(SET CMP0048 NEW)
    PROJECT(DRAMPOWER VERSION 0.9 LANGUAGES CXX)
ELSE()
    PROJECT(DRAMPOWER LANGUAGES CXX)
ENDIF()

set(CMAKE_DISABLE_IN_SOURCE_BUILD OFF)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)

set(CMAKE_COLOR_MAKEFILE ON)
# And optionally
#set(CMAKE_VERBOSE_MAKEFILE ON)

SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
SET(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

LIST(APPEND LST_CORE "${PROJECT_SOURCE_DIR}/src/CAHelpers.cc" "${PROJECT_SOURCE_DIR}/src/CmdHandlers.cc" "${PROJECT_SOURCE_DIR}/src/CmdScheduler.cc" "${PROJECT_SOURCE_DIR}/src/CommandAnalysis.cc" "${PROJECT_SOURCE_DIR}/src/MemArchitectureSpec.cc" "${PROJECT_SOURCE_DIR}/src/MemBankWiseParams.cc" "${PROJECT_SOURCE_DIR}/src/MemCommand.cc" "${PROJECT_SOURCE_DIR}/src/MemoryPowerModel.cc" "${PROJECT_SOURCE_DIR}/src/MemorySpecification.cc" "${PROJECT_SOURCE_DIR}/src/MemPowerSpec.cc" "${PROJECT_SOURCE_DIR}/src/MemTimingSpec.cc" "${PROJECT_SOURCE_DIR}/src/Parameter.cc" "${PROJECT_SOURCE_DIR}/src/Parametrisable.cc" "${PROJECT_SOURCE_DIR}/src/TraceParser.cc")
LIST(APPEND LST_CLI "${PROJECT_SOURCE_DIR}/src/drampower.cc")
LIST(APPEND LST_XML "${PROJECT_SOURCE_DIR}/src/MemSpecParser.cc" "${PROJECT_SOURCE_DIR}/src/XMLHandler.cc" "${PROJECT_SOURCE_DIR}/src/XMLParser.cc")
LIST(APPEND LST_LIB "${PROJECT_SOURCE_DIR}/src/LibDRAMPower.cc")
#FILE(GLOB SRC_CORE LIST_DIRECTORIES FALSE "${PROJECT_SOURCE_DIR}/src/*.cc")
#FILE(GLOB SRC_CLI LIST_DIRECTORIES FALSE "${PROJECT_SOURCE_DIR}/src/cli/*.cc")
#FILE(GLOB SRC_XML LIST_DIRECTORIES FALSE "${PROJECT_SOURCE_DIR}/src/xmlparser/*.cc")
#FILE(GLOB SRC_LIB LIST_DIRECTORIES FALSE "${PROJECT_SOURCE_DIR}/src/libdrampower/*.cc")

ADD_CUSTOM_TARGET(traces-zip ALL)
ADD_CUSTOM_COMMAND(TARGET traces POST_BUILD COMMAND "wget --quiet --output-document=traces.zip https://github.com/Sv3n/DRAMPowerTraces/archive/master.zip")

ADD_CUSTOM_TARGET(runtest)
ADD_CUSTOM_COMMAND(TARGET runtest POST_BUILD COMMAND "python test/test.py")
ADD_DEPENDENCIES(runtest traces)

ADD_EXECUTABLE(drampower-bin)
SET_TARGET_PROPERTIES(drampower-bin PROPERTIES OUTPUT_NAME drampower)
TARGET_SOURCES(drampower-bin ${LST_CORE} ${LST_CLI} ${LST_XML})

ADD_LIBRARY(drampower-lib STATIC)
SET_TARGET_PROPERTIES(drampower-lib PROPERTIES OUTPUT_NAME libdrampower.a)
TARGET_SOURCES(drampower-lib ${LST_CORE} ${LST_LIB})

ADD_LIBRARY(drampower-lib-xml STATIC)
SET_TARGET_PROPERTIES(drampower-lib-xml PROPERTIES OUTPUT_NAME libdrampowerxml.a)
TARGET_SOURCES(drampower-lib-xml ${LST_CORE} ${LST_LIB} ${LST_XML})
