'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import argparse
import copy
import abc
import sys
import time

from arjuna.lib.core.utils import sys_utils
from arjuna.lib.core.enums import *
from arjuna.lib.enums import *
from arjuna.lib.core.reader.textfile import TextResourceReader
from arjuna.lib.core.types import constants
from arjuna.lib.core.adv.py import *

from .commands import *

class ArjunaCLI:

    def __init__(self, args):
        super().__init__()
        self._args = args
        self.arg_dict = None
        self.main_command = MainCommand()

        # Create parser for primary commands
        subparsers = self.main_command.create_subparsers()

        # Create re-usable parses for command arguments
        run_parser = RunParser(subparsers)
        session_parser = SessionParser(subparsers)
        group_parser = GroupParser(subparsers)
        names_parser = NamesParser(subparsers)

        # Create primary command handlers
        self.create_project = CreateProject(subparsers)
        self.run_project = RunProject(subparsers, [run_parser])
        self.run_session = RunSession(subparsers, [run_parser, session_parser])
        self.run_group = RunGroup(subparsers, [run_parser, group_parser])
        self.run_names = RunNames(subparsers, [run_parser, names_parser])

    def init(self):
        time.sleep(0.1)
        self.arg_dict = self.main_command.convert_to_dict(self._args)
        self.main_command.execute(self.arg_dict)

    def execute(self):
        command = self.arg_dict['command']
        del self.arg_dict['command']

        if not command:
            print("!!!Fatal Error!!! You did not provide any command.")
            print()
            self.main_command.print_help()
            sys.exit(1)

        # Delegation dictionary for primary command description
        desc_cases = {
            CommandEnum.CREATE_PROJECT: "Creating new project",
            CommandEnum.RUN_PROJECT: "Running the project",
            CommandEnum.RUN_SESSION: "Running the selected session",
            CommandEnum.RUN_GROUP: "Running the selected group",
            CommandEnum.RUN_NAMES: "Running the selected names"
        }

        # Hyphens in commands are replaced with underscores for enum conversion
        # So, create-project is internally referred as CREATE_PROJECT
        command_enum = CommandEnum[command.upper().replace("-", "_")]

        print(desc_cases[command_enum] + "...")

        # Delegation dictionary for primary command choices
        # Respective command object's 'execute' method is the handler.
        execute_cases = {
            CommandEnum.CREATE_PROJECT: (self.create_project.execute, ),
            CommandEnum.RUN_PROJECT: (self.run_project.execute, ),
            CommandEnum.RUN_SESSION: (self.run_session.execute, ),
            CommandEnum.RUN_GROUP: (self.run_group.execute, ),
            CommandEnum.RUN_NAMES: (self.run_names.execute, )
        }

        # Delegation using Arjuna's Enum based switch-case equivalent
        switch = EnumSwitch(execute_cases, (self.arg_dict,))
        switch(command_enum)
