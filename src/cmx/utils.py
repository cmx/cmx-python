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


# --------------------------------------------------------------------------- #
# Local-filesystem write helpers.
#
# These are the building blocks for ``CommonMark``'s default lifecycle hooks
# (``on_save`` / ``on_flush``). They are plain module functions so the default
# hooks can call them and custom hooks can re-use them (``super().on_save(...)``).
# --------------------------------------------------------------------------- #


def _resolve_full_path(path, wd=None):
    """Join ``path`` under ``wd`` (the document working dir) unless absolute."""
    import os

    if wd and not os.path.isabs(path):
        return os.path.join(wd, path)
    return path


def write_image(image, path, *, wd=None, normalize=False):
    """Write an image array (or PIL image) to ``path`` under ``wd``."""
    import os
    from PIL import Image
    import numpy as np

    full_path = _resolve_full_path(path, wd)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    if isinstance(image, np.ndarray):
        if normalize:
            image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
        elif image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)
        image = Image.fromarray(image)

    image.save(full_path)


def write_video(frames, path, *, wd=None):
    """Write video frames to ``path`` under ``wd`` (``.gif`` only for now)."""
    import os

    full_path = _resolve_full_path(path, wd)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    if path.endswith(".gif"):
        from PIL import Image

        images = [Image.fromarray(frame) if not isinstance(frame, Image.Image) else frame for frame in frames]
        images[0].save(full_path, save_all=True, append_images=images[1:], duration=100, loop=0)
    else:
        raise NotImplementedError(
            f"Video format '{os.path.splitext(path)[1]}' not supported. "
            "Use .gif format or install additional video encoding libraries."
        )


def write_savefig(path, *, wd=None, **kwargs):
    """Save the current matplotlib figure to ``path`` under ``wd``."""
    import os
    import matplotlib.pyplot as plt

    full_path = _resolve_full_path(path, wd)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    plt.savefig(full_path, **kwargs)


def append_text(text, path, *, wd=None, overwrite=False):
    """Append (or overwrite) ``text`` to ``path`` under ``wd`` (mkdir -p)."""
    import os

    full_path = _resolve_full_path(path, wd)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    mode = "w" if overwrite else "a"
    with open(full_path, mode) as f:
        f.write(text)
