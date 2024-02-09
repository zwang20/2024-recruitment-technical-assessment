from dataclasses import dataclass

@dataclass
class File:
    id: int
    name: str
    categories: list[str]
    parent: int
    size: int


"""
Task 1
"""
def leafFiles(files: list[File]) -> list[str]:

    # get the set of all parent (non-leaf) files
    parent_files: set[int] = set()
    for file in files:
        parent_files.add(file.parent)
    
    # the leaf files will be all the files that are not parents
    leaf_files: list[str] = []
    for file in files:
        if file.id not in parent_files:
            leaf_files.append(file.name)

    return leaf_files


"""
Task 2
"""
def kLargestCategories(files: list[File], k: int) -> list[str]:

    # create a dictionary with category as key and 
    # the set of ids as values
    categories: dict[str, set[int]] = {}
    for file in files:
        for category in file.categories:
            if category not in categories.keys():  
                categories[category] = set()
            categories[category].add(file.id)
    
    # sort them in alphabetical order before sorting them by size
    alphabetical_categories = sorted(list(categories.items()), key=lambda x: x[0])
    largest_categories = sorted(alphabetical_categories, key=lambda category: -len(category[1]))
    k_largest_categories = [category[0] for category in largest_categories[:k]]
    return k_largest_categories

"""
Task 3
"""
import typing
def largestFileSize(files: list[File]) -> int:
    # this is a misleading name for a function
    # prehaps consider largestFileSystemEntry?

    @dataclass
    class File_Node:
        id: int
        size: int
        parent: int
        children: list[typing.Self]

    # create a dict of nodes
    nodes: dict[int, File_Node] = {}
    for file in files:
        nodes[file.id] = File_Node(file.id, file.size, file.parent, list())
    
    # add nodes to their parents
    for node in nodes.values():
        if node.parent != -1:
            nodes[node.parent].children.append(node)

    # return the max size via recursively calculating the size
    def size(node: File_Node) -> int:
        return node.size + sum(map(size, node.children))
    return max({
        size(node) for node in nodes.values()
        if node.parent == -1
    })


if __name__ == '__main__':
    testFiles = [
        File(1, "Document.txt", ["Documents"], 3, 1024),
        File(2, "Image.jpg", ["Media", "Photos"], 34, 2048),
        File(3, "Folder", ["Folder"], -1, 0),
        File(5, "Spreadsheet.xlsx", ["Documents", "Excel"], 3, 4096),
        File(8, "Backup.zip", ["Backup"], 233, 8192),
        File(13, "Presentation.pptx", ["Documents", "Presentation"], 3, 3072),
        File(21, "Video.mp4", ["Media", "Videos"], 34, 6144),
        File(34, "Folder2", ["Folder"], 3, 0),
        File(55, "Code.py", ["Programming"], -1, 1536),
        File(89, "Audio.mp3", ["Media", "Audio"], 34, 2560),
        File(144, "Spreadsheet2.xlsx", ["Documents", "Excel"], 3, 2048),
        File(233, "Folder3", ["Folder"], -1, 4096),
    ]

    assert sorted(leafFiles(testFiles)) == [
        "Audio.mp3",
        "Backup.zip",
        "Code.py",
        "Document.txt",
        "Image.jpg",
        "Presentation.pptx",
        "Spreadsheet.xlsx",
        "Spreadsheet2.xlsx",
        "Video.mp4"
    ]

    assert kLargestCategories(testFiles, 3) == [
        "Documents", "Folder", "Media"
    ]

    assert largestFileSize(testFiles) == 20992