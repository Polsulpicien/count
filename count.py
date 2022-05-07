import os


class Count:
    def __init__(
        self, 
        directory,
        extensions:list = [".py"], 
        exclude_files:list = ["__pycache__"],
        skip_on_error = True,
        ignore_this_file = True,
        max_depth = 50
    ):
        self.directory = directory
        self.extensions = extensions
        self.exclude_files = exclude_files
        self.skip_on_error = skip_on_error
        self.ignore_this_file = ignore_this_file
        self.depth = max_depth

        self.file_name = os.path.basename(self.directory)
        self.this_file = os.path.realpath(__file__)

        self.files = []
        self.error_files = []
        self.total_of_files = 0
        self.total_of_lines = 0
        self.total_of_blank_lines = 0
        self.class_count = 0
        self.comment_count = 0
        self.func = 0

    def get_files(self, path = None):
        if path == None:
            path = self.directory
        self.depth -= 1
        with os.scandir(path) as data:
            for entry in data:
                skip = False
                for filename in self.exclude_files:
                    if entry.path.endswith(filename):
                        skip = True
                        break
                if skip == False:
                    yield entry.path
                    if entry.is_dir() and self.depth > 0:
                        yield from self.get_files(entry.path)
    
    def display(self):
        print("=====================================")
        print(f"| File Count Errors: {len(self.error_files)}")
        for file in self.error_files:
            print(f"[ERROR] > {file}")

        print("=====================================")
        print(f"|       Files > {len(self.files)}")
        print(f"|       Class > {self.class_count}")
        print(f"|    Function > {self.func}")
        print(f"|    Comments > {self.comment_count}")
        print(f"| Empty lines > {self.total_of_blank_lines}")
        print(f"| Total lines > {self.total_of_lines + self.total_of_blank_lines} ({self.total_of_lines})")
        
    def scan(self):
        print(f"(0.0%) {self.directory} > Scanning")
        self.files = list(self.get_files())
        self.total_of_files = len(self.files)
        for i, file_directory in enumerate(self.files):
            if file_directory == self.this_file or not os.path.isfile(self.this_file):
                continue

            skip = True
            if self.extensions != []:
                for ending in self.extensions:
                    if file_directory.endswith(ending):
                        skip = False
            else:
                skip = False

            if not skip:
                try:
                    file = open(file_directory, "r", encoding="utf8")
                    local_count = 0
                    local_blank_count = 0
                    for line in file:
                        if line != "\n":
                            local_count += 1
                        else:
                            local_blank_count +=1
                        if "class" in line:
                            self.class_count += 1
                        elif "#" in line:
                            self.comment_count += 1 
                        elif "def" in line:
                            self.func += 1 
                    print(f"{'({:.1f}%)'.format(100*i/self.total_of_files)} {file_directory} > {local_count} ({local_blank_count})")
                    self.total_of_lines += local_count
                    self.total_of_blank_lines += local_blank_count
                    file.close()
                except:
                    self.error_files.append(file_directory)
                    continue
        self.display()

files = Count(
    directory = os.getcwd(), 
    exclude_files = ["__pycache__"]
).scan()
