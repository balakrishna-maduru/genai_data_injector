import os
import fsspec
from datetime import datetime

def get_file_system(filesystem_type, **kwargs):
        return fsspec.filesystem(filesystem_type, **kwargs)

class FileSystem:
    def __init__(self, source_fs, destination_fs=None):
        self.source_fs = source_fs
        self.destination_fs = destination_fs
        self.target_fs=0
    
    @property
    def file_system(self):
        return self.destination_fs if self.target_fs and self.destination_fs else self.source_fs

    def copy(self, from_path, to_path):
        print(f"from_path : {from_path}")
        print(f"to_path : {to_path}")
        if self.destination_fs:
            with self.source_fs.open(from_path, 'rb') as source_file, self.destination_fs.open(to_path, 'wb') as destination_file:
                destination_file.write(source_file.read())
        else:
            raise ValueError("Destination filesystem is not specified.")

    def move(self, from_path, to_path):
        self.copy(from_path, to_path)
        self.rm(from_path)

    def rm(self, file_path):
        self.file_system.rm(file_path)

    def mkdir(self, path, create_parents=True, target_fs=0, **kwargs):
        self.target_fs = target_fs
        return self.file_system.makedirs(path, exist_ok=create_parents)

    def makedirs(self, path, exist_ok=False, target_fs=0):
        self.target_fs = target_fs
        return self.file_system.makedirs(path)

    def rmdir(self, path, target_fs=0):
        self.target_fs = target_fs
        return self.file_system.rmdir(path)

    def ls(self, path, detail=True, target_fs=0, **kwargs):
        self.target_fs = target_fs
        return self.file_system.rmdir.ls(path, detail=detail, **kwargs)

    def walk(self, path, maxdepth=None, topdown=True, on_error="omit", target_fs=0, **kwargs):
        self.target_fs = target_fs
        return list(self.file_system.rmdir.walk(path, maxdepth=maxdepth, topdown=topdown, on_error=on_error, **kwargs))

    def find(self, path, maxdepth=None, withdirs=False, detail=False, target_fs=0, **kwargs):
        self.target_fs = target_fs
        return list(self.file_system.find(path, maxdepth=maxdepth, withdirs=withdirs, detail=detail, **kwargs))

    def du(self, path, total=True, maxdepth=None, withdirs=False, target_fs=0, **kwargs):
        self.target_fs = target_fs
        return self.file_system.du(path, total=total, maxdepth=maxdepth, withdirs=withdirs, **kwargs)

    def glob(self, path, maxdepth=None, target_fs=0, **kwargs):
        self.target_fs = target_fs
        return self.file_system.glob(path, maxdepth=maxdepth, **kwargs)

    def exists(self, path, target_fs=0, **kwargs):
        self.target_fs = target_fs
        return self.file_system.exists(path, **kwargs)

    def info(self, path, convert_date=True, target_fs=0, **kwargs):
        self.target_fs = target_fs
        data = self.file_system.info(path, **kwargs)
        if convert_date:
            data['created'] = datetime.fromtimestamp(data['created']).isoformat()
            data['mtime'] = datetime.fromtimestamp(data['mtime']).isoformat()
        data['type'] = os.path.splitext(path)[-1]
        data['file_name'] = os.path.basename(path)
        return data

    def checksum(self, path, target_fs=0):
        self.target_fs = target_fs
        return self.file_system.checksum(path)

    def size(self, path, target_fs=0):
        self.target_fs = target_fs
        return self.file_system.size(path)

    def sizes(self, paths, target_fs=0):
        self.target_fs = target_fs
        return self.file_system.sizes(paths)

    def isdir(self, path, target_fs=0):
        self.target_fs = target_fs
        return self.file_system.isdir(path)

    def isfile(self, path, target_fs=0):
        self.target_fs = target_fs
        return self.file_system.isfile(path)

    def read_text(self, path, encoding=None, errors=None, newline=None, target_fs=0, **kwargs):
        self.target_fs = target_fs
        with self.file_system.open(path, 'rt', encoding=encoding, errors=errors, newline=newline, **kwargs) as file:
            return file.read()

    def write_text(self, path, value, encoding=None, errors=None, newline=None,target_fs=0, **kwargs):
        self.target_fs = target_fs
        with self.file_system.open(path, 'wt', encoding=encoding, errors=errors, newline=newline, **kwargs) as file:
            file.write(value)

    def cat_file(self, path, start=None, end=None,target_fs=0, **kwargs):
        self.target_fs = target_fs
        with self.file_system.open(path, 'rt', **kwargs) as file:
            content = file.read()
            return content[start:end]

    def pipe_file(self, path, value,target_fs=0, **kwargs):
        self.target_fs = target_fs
        with self.file_system.fs.open(path, 'wt',target_fs=0, **kwargs) as file:
            file.write(value)

    def pipe(self, path, value=None,target_fs=0, **kwargs):
        self.target_fs = target_fs
        if value is None:
            with self.file_system.fs.open(path, 'rt', **kwargs) as file:
                return file.read()
        else:
            with self.file_system.fs.open(path, 'wt', **kwargs) as file:
                file.write(value)

    def cat_ranges(self, paths, starts, ends, max_gap=None, on_error="return", target_fs=0, **kwargs):
        self.target_fs = target_fs
        content = ''
        for path, start, end in zip(paths, starts, ends):
            with self.file_system.open(path, 'rt', **kwargs) as file:
                file_content = file.read()
                content += file_content[start:end]
                if max_gap is not None and len(file_content) - end > max_gap:
                    raise ValueError(f"Gap between ranges exceeds max_gap in file: {path}")
        return content

    def cat(self, path, recursive=False, on_error="raise",target_fs=0, **kwargs):
        self.target_fs = target_fs
        if recursive:
            return self.cat_ranges([path], [0], [None], on_error=on_error,target_fs=target_fs, **kwargs)
        else:
            return self.cat_file(path,target_fs, **kwargs)

    def get_file(self, rpath, lpath, callback=None, outfile=None,target_fs=0, **kwargs):
        self.target_fs = target_fs
        self.file_system.get(rpath, lpath, recursive=False, callback=callback, maxdepth=None, **kwargs)

    def get(self, rpath, lpath, recursive=False, callback=None, maxdepth=None,target_fs=0, **kwargs):
        self.target_fs = target_fs
        self.file_system.get(rpath, lpath, recursive=recursive, callback=callback, maxdepth=maxdepth, **kwargs)

    def put_file(self, lpath, rpath, callback=None, target_fs=0, **kwargs):
        self.target_fs = target_fs
        self.file_system.put(lpath, rpath, recursive=False, callback=callback, maxdepth=None, **kwargs)

    def put(self, lpath, rpath, recursive=False, callback=None, maxdepth=None, target_fs=0, **kwargs):
        self.target_fs = target_fs
        self.file_system.put(lpath, rpath, recursive=recursive, callback=callback, maxdepth=maxdepth, **kwargs)

    def head(self, path, size=1024, target_fs=0):
        self.target_fs = target_fs
        with self.file_system.open(path, 'rb') as file:
            return file.read(size)

    def tail(self, path, size=1024, target_fs=0):
        self.target_fs = target_fs
        with self.file_system.open(path, 'rb') as file:
            file.seek(-size, os.SEEK_END)
            return file.read()

    def cp_file(self, path1, path2, **kwargs):
        self.copy(path1, path2)

    def expand_path(self, path, recursive=False, maxdepth=None, target_fs=0, **kwargs):
        self.target_fs = target_fs
        return list(self.file_system.expand_path(path, recursive=recursive, maxdepth=maxdepth, **kwargs))

    def touch(self, path, truncate=True, target_fs=0, **kwargs):
        self.target_fs = target_fs
        if not self.exists(path, target_fs = target_fs):
            self.write_text(path, '', target_fs=target_fs)
        elif truncate:
            with self.file_system.open(path, 'w', **kwargs) as file:
                file.truncate(0)
