import os

from config import config, ELSE, CONTENT
from dataset import dataset

os.system("cls")

def generate_commands(config, dataset, prefix='', is_root=True):
    commands = []
    for key in config:
        if key in dataset:
            for synonym in dataset[key]:
                if isinstance(config[key], dict):
                    sub_commands = generate_commands(config[key], dataset, prefix=f"{prefix} {synonym}", is_root=False)
                    if sub_commands:
                        commands.extend(sub_commands)
                elif config[key] == CONTENT:
                    commands.append(f"{prefix} {synonym} (контент)")
                else:
                    commands.append(f"{prefix} {synonym}")
            if is_root:
                commands.append("-" * 22)
        elif key == ELSE:
            commands.append(f"{prefix}")
        elif key == CONTENT:
            if isinstance(config[key], dict):
                sub_commands = generate_commands(config[key], dataset, prefix=f"{prefix} (контент)", is_root=False)
                if sub_commands:
                    commands.extend(sub_commands)
            else:
                commands.append(f"{prefix} (контент)")
            
    return commands


commands = generate_commands(config, dataset)
for command in commands:
    print(command.strip())