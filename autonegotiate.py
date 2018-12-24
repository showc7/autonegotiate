#!/usr/bin/python3

import os
import argparse

setup_file = "test.txt"

class Utils:
    @staticmethod
    def exists(interface):
        try:
            with open(setup_file, 'r') as file:
                return ('ethtool -s ' + interface + ' autoneg off') in file.read().split('\n')
        except:
            return False

class SetupAutonegotiateOnBootAction:
    def execute(self, interface):
        if Utils.exists(interface):
            print("already setup")
            return
        lines = []
        with open(setup_file, 'w+') as file:
            lines = list(filter(lambda line: len(line) > 0, file.read().split('\n')))
        lines.append('ethtool -s ' + interface + ' autoneg off')
        with open(setup_file, 'w') as file:
            for line in lines:
                file.write(line)

class RemoveAutonegotiateOnBootAction:
    def execute(self, interface):
        new_lines = []

        with open(setup_file, 'r') as file:
            for line in file.read().split('\n'):
                if ('ethtool -s ' + interface + ' autoneg off') in line: continue
                new_lines.append(line)

        with open(setup_file, 'w') as file:
            for line in new_lines:
                file.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', dest='interface', required=True, help="hardware interface name")
    parser.add_argument('--action', dest='action', choices=['add','remove'], required=True, help="add - to add automatic setup of autonegotiation of false\n remove - to roll back add addjustments")
    
    options = parser.parse_args()

    if options.action == 'add':
        action = SetupAutonegotiateOnBootAction()
        action.execute(options.interface)
    elif options.action == 'remove':
        action = RemoveAutonegotiateOnBootAction()
        action.execute(options.interface)
