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
    PROJECT(RAMulator-Host VERSION 0.9 LANGUAGES CXX)
ELSE()
    PROJECT(RAMulator-Host LANGUAGES CXX)
ENDIF()

set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)

set(CMAKE_COLOR_MAKEFILE ON)
# And optionally
#set(CMAKE_VERBOSE_MAKEFILE ON)

SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
SET(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

EXECUTE_PROCESS(COMMAND uname -s RESULT_VARIABLE UNAME_RETURNCODE OUTPUT_VARIABLE UNAME_OUT ERROR_VARIABLE UNAME_ERR OUTPUT_STRIP_TRAILING_WHITESPACE)
IF(NOT UNAME_RETURNCODE EQUAL 0)
	MESSAGE(WARNING "Could not use ''uname -s'' to determine the kernel name! Assuming Linux.")
	SET(UNAME_OUT "Linux")
ENDIF(NOT UNAME_RETURNCODE EQUAL 0)

IF(CMAKE_BINARY_DIR STREQUAL CMAKE_CURRENT_BINARY_DIR)
	SET(STANDALONE TRUE)
	MESSAGE(STATUS "${PROJECT_NAME}: In standalone mode")
ELSE()
	SET(STANDALONE FALSE)
	MESSAGE(STATUS "${PROJECT_NAME}: In subproject mode")
ENDIF()

FILE(GLOB SRCS RELATIVE ${PROJECT_SOURCE_DIR} src/*.cpp)
LIST(REMOVE_ITEM SRCS src/Gem5Wrapper.cpp)
ADD_EXECUTABLE(ramulator_host ${SRCS})
TARGET_COMPILE_OPTIONS(ramulator_host PUBLIC -O3 -g -Wall)
SET_PROPERTY(TARGET ramulator_host PROPERTY CXX_STANDARD 11)
SET_PROPERTY(TARGET ramulator_host PROPERTY CXX_STANDARD_REQUIRED ON)
GET_FILENAME_COMPONENT(DRAMPOWER_SOURCES "${PROJECT_SOURCE_DIR}/../../common/DRAMPower/src" ABSOLUTE)
GET_FILENAME_COMPONENT(RAMULATOR_SOURCES "${PROJECT_SOURCE_DIR}/../../common/ramulator/src" ABSOLUTE)
TARGET_INCLUDE_DIRECTORIES(ramulator_host PUBLIC "${DRAMPOWER_SOURCES}" PUBLIC "${RAMULATOR_SOURCES}")
TARGET_COMPILE_DEFINITIONS(ramulator_host PUBLIC RAMULATOR)
TARGET_LINK_LIBRARIES(ramulator_host PUBLIC boost_program_options)
IF(UNAME_OUT STREQUAL "Linux")
	IF(STANDALONE)
		SET(FILE_LIBDRAMPOWERXML ${DRAMPOWER_SOURCES}/libdrampowerxml.a)
    IF(NOT EXISTS FILE_LIBDRAMPOWERXML)
			ADD_SUBDIRECTORY(${PROJECT_SOURCE_DIR}/../../common/DRAMPower/ ${PROJECT_BINARY_DIR}/DRAMPower)
			TARGET_LINK_LIBRARIES(ramulator_host PUBLIC drampower-lib-xml)
		ELSE()
			TARGET_LINK_LIBRARIES(ramulator_host PUBLIC "${FILE_LIBDRAMPOWERXML}")
		ENDIF()
    ADD_SUBDIRECTORY(${PROJECT_SOURCE_DIR}/../../common/ramulator)
	ELSEIF(TARGET drampower-lib-xml)
    MESSAGE(STATUS "${PROJECT_NAME}: Found target 'drampower-lib-xml'.")
		TARGET_LINK_LIBRARIES(ramulator_host PUBLIC drampower-lib-xml)
  ELSE()
    MESSAGE(FATAL_ERROR "${PROJECT_NAME}: Could not determine location of static library libdrampowerxml.a")
	ENDIF()
	FIND_PACKAGE(XercesC 3.2 REQUIRED)
	TARGET_LINK_LIBRARIES(ramulator_host PUBLIC ${XercesC_LIBRARIES})
ELSEIF(UNAME_OUT STREQUAL "Darwin")
	FIND_PACKAGE(Boost REQUIRED)
	LINK_DIRECTORIES(${Boost_LIBRARY_DIRS})
ELSE(UNAME_OUT STREQUAL "Darwin")
	MESSAGE(FATAL_ERROR "Unsupported kernel name!")
ENDIF(UNAME_OUT STREQUAL "Linux")
