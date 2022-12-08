from adventofcode2022 import read_file


def parse_terminal(string: str) -> tuple():
    commands = string.split("$ ")
    commands = [list(filter(lambda x: x != "", ele_)) for ele_ in [ele.split("\n") for ele in commands]][2:]
    commands = [{ele[0]: ele[1:]} if "cd " not in ele[0] else {ele[0][:2]: ele[0][3:]} for ele in commands]
    return commands


def find_folder_index(name, content):

    for i, ele in enumerate(content):
        if type(ele) == Folder:
            if ele.folder_name == name:
                return i

    return False


class Folder:
    def __init__(self, folder_name, parent):
        self.folder_name = folder_name
        self.content: list = []
        self.parent = parent
        self.size = 0

    def add(self, command_dict):
        command = list(command_dict.keys())[0]
        command_details = command_dict[command]
        if command == "cd" and command_details != "..":

            find_folder = find_folder_index(command_details, self.content)
            # add folder if does not exist
            if find_folder == False:
                print(f"Adding folder {command_details}")
                self.content.append(Folder(command_details, parent=self))
            else:
                print(f"folder found at index {find_folder}")

        elif command == "cd" and command_details == "..":
            # go up one level
            print(f"go up one level to {self.parent.folder_name}")
            # for ele in self.content:
            #     self.size += ele.size
            #      print(f"updated dir {self.folder_name} as {self.size=}")
        elif command == "ls":
            # add content
            for _file in command_details:
                if "dir " not in _file:
                    file_size, file_name = _file.split(" ")
                    self.content.append(Files(file_name, int(file_size)))

        else:
            raise Exception("Unknown command")


class Files:
    def __init__(self, file_name, file_size):
        self.file_name = file_name
        self.size = file_size


# for command_dict in command:
#     root.add(command_dict)


def go_up_bool(command) -> bool:
    return command == {"cd": ".."}


def recurse_add(current_folder, commands):
    # in hindsight does not need to be recursive

    command = commands[0]
    if len(commands) == 1:
        current_folder.add(command)
        while current_folder.folder_name != "/":
            current_folder.add({"cd": ".."})
            current_folder = current_folder.parent
        return current_folder
    else:
        current_folder.add(command)
        if list(command.keys())[0] == "cd":
            if go_up_bool(command):
                current_folder = current_folder.parent
            else:
                # enter newly added folder
                print(f"cd into {command['cd']}")
                folder_index = find_folder_index(command["cd"], current_folder.content)
                current_folder = current_folder.content[folder_index]

    return recurse_add(current_folder, commands[1:])


folder_sizes = []


def get_folder_sizes_recurse(current_folder: Folder):
    folder_size = 0
    for ele in current_folder.content:

        if type(ele) == Folder:

            get_folder_sizes_recurse(ele)

        folder_size += ele.size

    current_folder.size = folder_size
    folder_sizes.append((current_folder.folder_name, folder_size))


file_path = "./input/day07.csv"
command = parse_terminal(read_file(file_path))

root = Folder("/", None)

recurse_add(root, command)
get_folder_sizes_recurse(root)

relevant_total = [ele for ele in folder_sizes if ele[1] <= 100000]
final_total = [ele[1] for ele in relevant_total]

print(sum(final_total))

# Part 2
all_sizes = [ele[1] for ele in folder_sizes]
all_sizes.sort()
free_up = 30000000 - (70000000 - max(all_sizes))


def find_smallest_to_delete(free_up: int, file_sizes: list) -> int:
    for ele in file_sizes:
        if free_up < ele:
            return ele


print(find_smallest_to_delete(free_up, all_sizes))
