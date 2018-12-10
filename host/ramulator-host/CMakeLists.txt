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
    PROJECT(RAMULATOR_HOST VERSION 0.9 LANGUAGES CXX)
ELSE()
    PROJECT(RAMULATOR_HOST LANGUAGES CXX)
ENDIF()

set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)

set(CMAKE_COLOR_MAKEFILE ON)
# And optionally
#set(CMAKE_VERBOSE_MAKEFILE ON)

SET(EXECUTABLE_OUTPUT_PATHi ${CMAKE_BINARY_DIR})
SET(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

EXECUTE_PROCESS(COMMAND uname -s RESULT_VARIABLE UNAME_RETURNCODE OUTPUT_VARIABLE UNAME_OUT ERROR_VARIABLE UNAME_ERR OUTPUT_STRIP_TRAILING_WHITESPACE)
IF(NOT UNAME_RETURNCODE EQUAL 0)
	MESSAGE(WARNING "Could not use ''uname -s'' to determine the kernel name! Assuming Linux.")
	SET(UNAME_OUT "Linux")
ENDIF(NOT UNAME_RETURNCODE EQUAL 0)
GET_FILENAME_COMPONENT(DRAMPOWERDIR "${PROJECT_SOURCE_DIR}/../../common/DRAMPower/src" ABSOLUTE)
MESSAGE(STATUS "DRAMPOWERDIR = ${DRAMPOWERDIR}")
FILE(GLOB SRCS RELATIVE ${PROJECT_SOURCE_DIR} src/*.cpp)
LIST(REMOVE_ITEM SRCS src/Gem5Wrapper.cpp)
ADD_EXECUTABLE(ramulator_host ${SRCS})
TARGET_COMPILE_OPTIONS(ramulator_host PUBLIC -O3 -g -Wall -w)
SET_PROPERTY(TARGET ramulator_host PROPERTY CXX_STANDARD 11) 
SET_PROPERTY(TARGET ramulator_host PROPERTY CXX_STANDARD_REQUIRED ON)
TARGET_INCLUDE_DIRECTORIES(ramulator_host PUBLIC "${DRAMPOWERDIR}")
TARGET_COMPILE_DEFINITIONS(ramulator_host PUBLIC RAMULATOR)
#LINK_DIRECTORIES(${DRAMPOWERDIR})
IF(UNAME_OUT STREQUAL "Linux")
	TARGET_LINK_LIBRARIES(ramulator_host PUBLIC boost_program_options PUBLIC "${DRAMPOWERDIR}/libdrampowerxml.a" PUBLIC "${DRAMPOWERDIR}/libdrampower.a" PUBLIC xerces-c)
ELSEIF(UNAME_OUT STREQUAL "Darwin")
	FIND_PACKAGE(Boost REQUIRED)
	LINK_DIRECTORIES(${Boost_LIBRARY_DIRS})
	TARGET_LINK_LIBRARIES(ramulator PUBLIC boost_program_options)
ELSE(UNAME_OUT STREQUAL "Darwin")
	MESSAGE(FATAL_ERROR "Unsupported kernel name!")
ENDIF(UNAME_OUT STREQUAL "Linux")
