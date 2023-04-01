# Build Instructions

This project can only be used as a Conan package. It does not perform any compilation and merely makes the base class
available to other Conan packages through `python_requires`.

## Getting the Code

To retrieve the code from GitHub:

```cmd
git clone https://github.com/TimZoet/pyreq.git source
```

## Exporting to Conan

To export the `pyreq` package to your local Conan cache:

```cmd
conan export --user timzoet --channel v1.0.0 source
```

Make sure to update the channel when the version is different.

## Including the Package

To include the package from your `conanfile.py`:

```py
class MyConan(ConanFile):
    python_requires = "pyreq/1.0.0@timzoet/v1.0.0"
    python_requires_extend = "pyreq.BaseConan"
    ...
```

You can then start using the base class `BaseConan` in all methods of your class:

```py
class MyConan(ConanFile):
    ...
    def init(self):
        base = self.python_requires["pyreq"].module.BaseConan
        self.options.update(base.options, base.default_options)
```
