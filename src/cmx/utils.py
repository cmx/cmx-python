import re


class _FMeta(type):
    """Metaclass that allows F @ function syntax on the class itself"""

    def __matmul__(cls, other):
        """Allow F @ function syntax"""
        return cls(other)


class F(metaclass=_FMeta):
    """Functional notation wrapper - allows using @ operator for function composition

    Usage:
    - F @ function - wraps a function
    - (F @ function)(args) - calls the wrapped function
    """

    def __init__(self, fn=None):
        self.fn = fn

    def __matmul__(self, other):
        """Allow instance @ function syntax"""
        if callable(other):
            return F(other)
        # If other is not callable, apply the function to it
        if self.fn is not None:
            return self.fn(other)
        return other

    def __call__(self, *args, **kwargs):
        """Make F callable"""
        if self.fn is not None:
            return self.fn(*args, **kwargs)
        raise TypeError("F object is not callable without a function")


def _F(fn, name=None):
    """Decorator for functional notation - allows function to work with @ operator

    Can be used as:
    - @_F decorator
    - _F(function) wrapper
    - _F(function, name="custom_name") wrapper with custom name
    """
    if callable(fn):

        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        wrapper.__name__ = name or fn.__name__
        wrapper.__doc__ = fn.__doc__
        return wrapper
    # If fn is not callable, return a decorator
    else:

        def decorator(func):
            return _F(func, name=fn)

        return decorator


def is_empty(line):
    return len(line.strip()) == 0


def get_indent(text):
    for line in text.split("\n"):
        if line:
            return len(line) - len(line.lstrip())
    return 0


def dedent(text):
    lines = text.split("\n")
    first_line = None
    for line in lines:
        if line:
            first_line = line
            break
    if first_line is None:
        return text
    indent = get_indent(first_line)
    return "\n".join([line[indent:] for line in lines])


def get_block(filename, line_number):

    current_line_number = 0
    lines, indent = [], None
    with open(filename, "r") as f:
        while True:
            line = f.readline()
            if line == "":  # this is the end of lines
                break
            current_line_number += 1
            if current_line_number < line_number:
                continue
            current_indent = get_indent(line)
            if line == "\n":
                lines.append(line)
            else:
                if indent is None:
                    indent = current_indent
                elif current_indent < indent:
                    break
                    # print(lines, sep="\n")
                    # print(current_indent, indent)
                lines.append(line)

    return lines


def is_subclass(obj, cls):
    try:
        return issubclass(obj, cls)
    except TypeError:
        return False


def to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


class SimpleLogger:
    """A simple logger replacement for ml-logger functionality used in cmx.

    This provides basic file I/O operations for saving images, videos, and text
    that were previously handled by ml-logger.
    """

    def __init__(self, root=None, prefix=None):
        """Initialize the logger with a root directory and optional prefix.

        Args:
            root: Root directory for saving files (defaults to current directory)
            prefix: Optional prefix to prepend to file paths
        """
        import os

        self.root = root or os.getcwd()
        self.prefix = prefix or ""

    def _get_full_path(self, filename):
        """Get the full path for a file, handling prefix and root."""
        import os

        if self.prefix:
            filename = os.path.join(self.prefix, filename)
        if not os.path.isabs(filename):
            filename = os.path.join(self.root, filename)
        return filename

    def save_image(self, image, filename, normalize=False):
        """Save an image to disk.

        Args:
            image: Image array (numpy array or PIL Image)
            filename: Path where to save the image
            normalize: Whether to normalize the image values
        """
        import os
        from PIL import Image
        import numpy as np

        full_path = self._get_full_path(filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if isinstance(image, np.ndarray):
            if normalize:
                image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
            elif image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)
            image = Image.fromarray(image)

        image.save(full_path)

    def save_video(self, frames, filename):
        """Save video frames to a file.

        Args:
            frames: List of image frames (numpy arrays)
            filename: Path where to save the video
        """
        import os

        full_path = self._get_full_path(filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        if filename.endswith(".gif"):
            from PIL import Image

            images = [Image.fromarray(frame) if not isinstance(frame, Image.Image) else frame for frame in frames]
            images[0].save(full_path, save_all=True, append_images=images[1:], duration=100, loop=0)
        else:
            # For other video formats, you would need additional dependencies like opencv or imageio
            # For now, raise an error suggesting alternatives
            raise NotImplementedError(
                f"Video format '{os.path.splitext(filename)[1]}' not supported. "
                "Use .gif format or install additional video encoding libraries."
            )

    def savefig(self, filename, **kwargs):
        """Save the current matplotlib figure.

        Args:
            filename: Path where to save the figure
            kwargs: Additional arguments passed to matplotlib's savefig
        """
        import os
        import matplotlib.pyplot as plt

        full_path = self._get_full_path(filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        plt.savefig(full_path, **kwargs)

    def log_text(self, text, filename, overwrite=False):
        """Log text to a file.

        Args:
            text: Text content to write
            filename: Path where to save the text
            overwrite: If True, overwrite the file; if False, append
        """
        import os

        full_path = self._get_full_path(filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        mode = "w" if overwrite else "a"
        with open(full_path, mode) as f:
            f.write(text)

    def get_dash_url(self):
        """Get a URL for the dashboard (returns file:// URL for local files)."""
        return f"file://{self.root}"

    def load_json(self, filename):
        """Load a JSON file.

        Args:
            filename: Path to the JSON file

        Returns:
            Parsed JSON data
        """
        import json

        full_path = self._get_full_path(filename)
        with open(full_path, "r") as f:
            return json.load(f)

    def load_file(self, filename):
        """Load a file and return a file-like object.

        Args:
            filename: Path to the file

        Returns:
            File-like object (BytesIO)
        """
        from io import BytesIO

        full_path = self._get_full_path(filename)
        with open(full_path, "rb") as f:
            return BytesIO(f.read())

    @staticmethod
    def now():
        """Get the current timestamp as a string.

        Returns:
            ISO formatted timestamp string
        """
        from datetime import datetime

        return datetime.now().isoformat()

    def job_started(self):
        """Mark a job as started (no-op for simple logger)."""
        pass
