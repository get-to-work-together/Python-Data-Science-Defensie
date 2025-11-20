def recursive_walk(directory: str, glob_pattern: str = None, re_pattern: str = None):
    """Recursively travels through directory and it's subdirectories.

    directory: directory to search
    glob_pattern: (optional) file matching string with wild cards
    re_pattern: (optional) file template string with regular expression

    The function is a generator returning a dict for each file.

    The function gracefully exits on KeyboardInterrupt (Control-C)

    Examples:

    >>> all_files = list(recursive_walk('..'))

    >>> all_files = list(recursive_walk('..', glob_pattern = '*.csv'))

    >>> all_files = list(recursive_walk('..', re_pattern = '.*ca-.*'))
    """

    try:
        path = Path(directory)

        if re_pattern:
            regex = re.compile(re_pattern)

        for i, (root, dirs, files) in enumerate(path.walk()):
            print(i, end='\r')
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files[:] = [f for f in files if f[0] not in ".~"]
            if glob_pattern:
                files[:] = [f.name for f in root.glob(glob_pattern)]
            if re_pattern:
                files[:] = [f for f in files if regex.match(f)]

            # print(f"Directory path: {root}")
            # print(f"Directory Names: {dirs}")
            # print(f"Files Names: {files}")
            # print(80 * '-')

            for filename in files:
                file_path = root / Path(filename)

                # info = Path(file_path)
                owner = file_path.owner()
                group = file_path.group()

                # Get file stats
                stat = file_path.stat()

                # File size in bytes
                size = stat.st_size

                # Creation time (platform dependent)
                ctime = datetime.fromtimestamp(
                    stat.st_ctime)  # On Unix: metadata change time, on Windows: creation time

                # Modification time
                mtime = datetime.fromtimestamp(stat.st_mtime)

                # Last Access time
                atime = datetime.fromtimestamp(stat.st_atime)

                try:
                    with open(file_path, mode='rb') as f:
                        md5 = hashlib.md5(f.read()).hexdigest()
                except KeyboardInterrupt as ex:
                    raise (ex)
                except:
                    md5 = None

                yield {
                    "filename": filename,
                    "directory": str(root),
                    "size": size,
                    "owner": owner,
                    "group": group,
                    "created": ctime,
                    "modified": mtime,
                    "accessed": atime,
                    "md5": md5,
                }

    except KeyboardInterrupt:
        return