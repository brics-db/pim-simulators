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

IF(POLICY CMP0076)
	CMAKE_POLICY(SET CMP0076 NEW)
ENDIF()

set(CMAKE_DISABLE_IN_SOURCE_BUILD ON)
set(CMAKE_DISABLE_SOURCE_CHANGES  ON)

set(CMAKE_COLOR_MAKEFILE ON)
# And optionally
#set(CMAKE_VERBOSE_MAKEFILE ON)

SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
SET(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

LIST(APPEND LST_CORE "${PROJECT_SOURCE_DIR}/src/CAHelpers.cc" "${PROJECT_SOURCE_DIR}/src/CmdHandlers.cc" "${PROJECT_SOURCE_DIR}/src/CmdScheduler.cc" "${PROJECT_SOURCE_DIR}/src/CommandAnalysis.cc" "${PROJECT_SOURCE_DIR}/src/MemArchitectureSpec.cc" "${PROJECT_SOURCE_DIR}/src/MemBankWiseParams.cc" "${PROJECT_SOURCE_DIR}/src/MemCommand.cc" "${PROJECT_SOURCE_DIR}/src/MemoryPowerModel.cc" "${PROJECT_SOURCE_DIR}/src/MemorySpecification.cc" "${PROJECT_SOURCE_DIR}/src/MemPowerSpec.cc" "${PROJECT_SOURCE_DIR}/src/MemTimingSpec.cc" "${PROJECT_SOURCE_DIR}/src/Parameter.cc" "${PROJECT_SOURCE_DIR}/src/Parametrisable.cc" "${PROJECT_SOURCE_DIR}/src/TraceParser.cc")
LIST(APPEND LST_CLI "${PROJECT_SOURCE_DIR}/src/cli/drampower.cc")
LIST(APPEND LST_XML "${PROJECT_SOURCE_DIR}/src/xmlparser/MemSpecParser.cc" "${PROJECT_SOURCE_DIR}/src/xmlparser/XMLHandler.cc" "${PROJECT_SOURCE_DIR}/src/xmlparser/XMLParser.cc")
LIST(APPEND LST_LIB "${PROJECT_SOURCE_DIR}/src/libdrampower/LibDRAMPower.cc")

SET(FILE_TRACES_ZIP traces.zip)
SET(DIR_TRACES_ZIP ${CMAKE_BINARY_DIR})
SET(PATH_TRACES_ZIP ${DIR_TRACES_ZIP}/${FILE_TRACES_ZIP})
ADD_CUSTOM_COMMAND(OUTPUT ${PATH_TRACES_ZIP} COMMAND wget --quiet --output-document=${PATH_TRACES_ZIP} https://github.com/Sv3n/DRAMPowerTraces/archive/master.zip WORKING_DIRECTORY ${DIR_TRACES_ZIP})

SET(DIR_TRACES ${DIR_TRACES_ZIP}/traces)
SET(TRACES_FILES ${DIR_TRACES}/LICENSE ${DIR_TRACES}/commands.trace ${DIR_TRACES}/mediabench-epic.trace ${DIR_TRACES}/mediabench-h263encode.trace ${DIR_TRACES}/mediabench-jpegencode.trace ${DIR_TRACES}/mediabench-mpeg2encode.trace)
ADD_CUSTOM_COMMAND(OUTPUT ${TRACES_FILES} COMMAND unzip ${PATH_TRACES_ZIP} && mkdir -p ${DIR_TRACES} && mv DRAMPowerTraces-master/traces/* ${DIR_TRACES}/ && rm -rf DRAMPowerTraces-master WORKING_DIRECTORY ${DIR_TRACES_ZIP})

ADD_CUSTOM_TARGET(traces-zip DEPENDS ${PATH_TRACES_ZIP})
ADD_CUSTOM_TARGET(traces DEPENDS traces-zip ${TRACES_FILES})

ADD_CUSTOM_TARGET(runtest)
ADD_CUSTOM_COMMAND(TARGET runtest POST_BUILD COMMAND "python test/test.py")
ADD_DEPENDENCIES(runtest traces)

FIND_PACKAGE(XercesC 3.2 REQUIRED)

ADD_EXECUTABLE(drampower-bin)
SET_TARGET_PROPERTIES(drampower-bin PROPERTIES OUTPUT_NAME drampower)
TARGET_SOURCES(drampower-bin PUBLIC ${LST_CORE} PUBLIC ${LST_CLI} PUBLIC ${LST_XML})
TARGET_INCLUDE_DIRECTORIES(drampower-bin PUBLIC "${PROJECT_SOURCE_DIR}/src" PUBLIC "${XercesC_INCLUDE_DIRS}")
TARGET_LINK_LIBRARIES(drampower-bin PUBLIC ${XercesC_LIBRARIES})
ADD_DEPENDENCIES(drampower-bin traces)

ADD_LIBRARY(drampower-lib STATIC)
SET_TARGET_PROPERTIES(drampower-lib PROPERTIES OUTPUT_NAME drampower)
TARGET_SOURCES(drampower-lib PUBLIC ${LST_CORE} PUBLIC ${LST_LIB})
TARGET_INCLUDE_DIRECTORIES(drampower-lib PUBLIC "${PROJECT_SOURCE_DIR}/src")
ADD_DEPENDENCIES(drampower-lib traces)

ADD_LIBRARY(drampower-lib-xml STATIC)
SET_TARGET_PROPERTIES(drampower-lib-xml PROPERTIES OUTPUT_NAME drampowerxml)
TARGET_SOURCES(drampower-lib-xml PUBLIC ${LST_CORE} PUBLIC ${LST_LIB} PUBLIC ${LST_XML})
TARGET_INCLUDE_DIRECTORIES(drampower-lib-xml PUBLIC "${PROJECT_SOURCE_DIR}/src" PUBLIC "${XercesC_INCLUDE_DIRS}")
TARGET_LINK_LIBRARIES(drampower-lib-xml PUBLIC ${XercesC_LIBRARIES})
ADD_DEPENDENCIES(drampower-lib-xml traces)

ADD_CUSTOM_TARGET(pretty)
STRING(REPLACE ";" " " SOURCES_CORE "${LST_CORE}")
STRING(REPLACE ";" " " SOURCES_CLI "${LST_CLI}")
STRING(REPLACE ";" " " SOURCES_LIB "${LST_LIB}")
STRING(REPLACE ";" " " SOURCES_XML "${LST_XML}")
LIST(APPEND LST_HEADERS "${PROJECT_SOURCE_DIR}/src/Parametrisable.h" "${PROJECT_SOURCE_DIR}/src/MemCommand.h" "${PROJECT_SOURCE_DIR}/src/MemoryPowerModel.h" "${PROJECT_SOURCE_DIR}/src/TraceParser.h" "${PROJECT_SOURCE_DIR}/src/MemPowerSpec.h" "${PROJECT_SOURCE_DIR}/src/xmlparser/XMLHandler.h" "${PROJECT_SOURCE_DIR}/src/xmlparser/MemSpecParser.h" "${PROJECT_SOURCE_DIR}/src/xmlparser/XMLParser.h" "${PROJECT_SOURCE_DIR}/src/MemTimingSpec.h" "${PROJECT_SOURCE_DIR}/src/Utils.h" "${PROJECT_SOURCE_DIR}/src/CommandAnalysis.h" "${PROJECT_SOURCE_DIR}/src/Parameter.h" "${PROJECT_SOURCE_DIR}/src/CmdScheduler.h" "${PROJECT_SOURCE_DIR}/src/libdrampower/LibDRAMPower.h" "${PROJECT_SOURCE_DIR}/src/MemBankWiseParams.h" "${PROJECT_SOURCE_DIR}/src/MemorySpecification.h" "${PROJECT_SOURCE_DIR}/src/MemArchitectureSpec.h")
STRING(REPLACE ";" " " SOURCES_HEADERS "${LST_HEADERS}")
ADD_CUSTOM_COMMAND(TARGET pretty PRE_BUILD COMMAND uncrustify -c src/uncrustify.cfg ${SOURCES_CORE} ${SOURCES_CLI} ${SOURCES_LIB} ${SOURCES_XML} --no-backup)
ADD_CUSTOM_COMMAND(TARGET pretty PRE_BUILD COMMAND uncrustify -c src/uncrustify.cfg ${SOURCES_HEADERS} --no-backup)
