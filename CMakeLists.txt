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

CMAKE_MINIMUM_REQUIRED(VERSION 3.11 FATAL_ERROR)

IF(POLICY CMP0048)
    CMAKE_POLICY(SET CMP0048 NEW)
    PROJECT(PIM_SIMULATORS VERSION 0.9 LANGUAGES CXX)
ELSE()
    PROJECT(PIM_SIMULATORS LANGUAGES CXX)
ENDIF()

set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)

set(CMAKE_COLOR_MAKEFILE ON)
# And optionally
#set(CMAKE_VERBOSE_MAKEFILE ON)

SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
SET(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

SET(NPROC "1")
EXECUTE_PROCESS(COMMAND nproc RESULT_VARIABLE NPROC_RETURNCODE OUTPUT_VARIABLE NPROC_OUT ERROR_VARIABLE NPROC_ERR OUTPUT_STRIP_TRAILING_WHITESPACE)
IF(NOT NPROC_RETURNCODE EQUAL 0)
    MESSAGE(WARNING "Could not use nproc to determine number of cores! Not using parallel compilation!")
ELSE(NOT NPROC_RETURNCODE EQUAL 0)
    SET(NPROC "${NPROC_OUT}")
ENDIF(NOT NPROC_RETURNCODE EQUAL 0)

EXECUTE_PROCESS(COMMAND which scons RESULT_VARIABLE SCONS_RETURNCODE)
IF(NOT SCONS_RETURNCODE EQUAL 0)
    MESSAGE(FATAL_ERROR "scons is not installed! Install using: sudo apt install scons")
ENDIF(NOT SCONS_RETURNCODE EQUAL 0)

#EXECUTE_PROCESS(COMMAND make -j "${NPROC}" WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/common/DRAMPower")
#EXECUTE_PROCESS(COMMAND scons -j "${NPROC}" WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/common/DRAMPower")
ADD_SUBDIRECTORY("${PROJECT_SOURCE_DIR}/common/DRAMPower")

#EXECUTE_PROCESS(COMMAND make -j "${NPROC}" WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/pim/ramulator-pim")
ADD_SUBDIRECTORY("${PROJECT_SOURCE_DIR}/pim/ramulator-pim")

#EXECUTE_PROCESS(COMMAND make -j "${NPROC}" WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/host/ramulator-host")
ADD_SUBDIRECTORY("${PROJECT_SOURCE_DIR}/host/ramulator-host")

EXECUTE_PROCESS(COMMAND scons -j "${NPROC}" WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/zsim-ramulator")
