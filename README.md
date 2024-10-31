[![PyPI](https://img.shields.io/pypi/v/basilisp-blender.svg?style=flat-square)](https://pypi.org/project/basilisp-blender/) [![CI](https://github.com/ikappaki/basilisp-blender/actions/workflows/tests-run.yml/badge.svg)](https://github.com/ikappaki/basilisp-blender/actions/workflows/tests-run.yml)

# Basilisp Blender Integration

[Basilisp](https://github.com/basilisp-lang/basilisp) is a Python-based Lisp implementation that offers broad compatibility with Clojure. For more details, refer to the [documentation](https://basilisp.readthedocs.io/en/latest/index.html).

## Overview
`basilisp-blender` is a Python library designed to facilitate the execution of Basilisp Clojure code within [Blender](https://www.blender.org/) and manage an nREPL server for interactive programming. 
This library provides functions to evaluate Basilisp code from Blender's Python console, file or Text Editor and to start an nREPL server, allowing seamless integration and communication with Basilisp.

## Installation
To install `basilisp-blender`, use `pip` from Blender's Python console:

```python
import pip
pip.main(['install', 'basilisp-blender'])
```

## Setup

### nREPL server control panel

The library includes an nREPL server control panel accessible in Blender’s properties editor, under the Output panel (icon resembling a printer). From here, users can:
- Start and stop the server.
- Configure the local interface address and port.
- Set the location of the `.nrepl-port` file for editor connections.


![nrepl cntrl pnael output - ready](examples/nrepl-ctrl-panel-output-ready.png)

![nrepl cntrl pnael output - ready](examples/nrepl-ctrl-panel-output-serving.png)

Note: The control panel does not appear automatically and must be activated manually via Blender's Python console within the `Scripting` workspace. To activate, run:

```python
import basilisp_blender
basilisp_blender.control_panel_create()
```

To autoload the panel automatically at Blender’s startup, create a startup file in Blender's `<blender-version>/scripts/startup/` directory. For example, save the code below, say as `bb.py`, in that directory:

```python
import basilisp_blender
basilisp_blender.control_panel_create()

def register():
    pass
def unregister():
    pass
if __name__ == "__main__":
    register()
```

## Usage
### Evaluating Basilisp Code

#### From a Code String
To evaluate a Basilisp code string:

```python
from basilisp_blender.eval import eval_str

eval_str("(+ 1 2)")
# => 3
```

#### From a File
To evaluate Basilisp code from a file:

```python
from basilisp_blender.eval import eval_file

eval_file("path/to/your/code.lpy")
```

#### From Blender’s Text Editor
To evaluate Basilisp code contained in a Blender text editor block:

```python
from basilisp_blender.eval import eval_editor

# Replace `text_block` with your Blender text block name
eval_editor("<text-block-name>")
```

#### Starting an nREPL Server
To start an nREPL server manually within Blender:

```python
from basilisp_blender.nrepl import server_start

shutdown_fn = server_start(host="127.0.0.1", port=8889)
```

The `host` and `port` arguments are optional.
If not provided, the server will bind to a random local port.
It will also creates an `.nrepl-port` file in the current working directory containing the port number it bound to.

The return value is a function that you can call without arguments to shut down the server.
Note that all nREPL client sessions must be closed before this function can succesfullyl shutdown the server.

For a more convenient setup, you can specify to output `.nrepl-port` file to your Basilisp's project's root directory.
This allows some Clojure editor extensions (such as [CIDER](https://docs.cider.mx/cider/index.html) or [Calva](https://calva.io/)) to automatically detect the port when `connect`'ing to the server:

```python
from basilisp_blender.nrepl import server_start

shutdown_fn = server_start(nrepl_port_filepath="<project-root-path>/.nrepl-port")
```

Replace `<project-root-path>` with the path to your project's root directory.

# Examples

Also see the [examples](examples/) directory of this repository.

Here is an example of Basilisp code to create a torus pattern using the bpy Blender Python library:

```clojure
(ns torus-pattern
  "Creates a torus pattern with randomly colored materials."
  (:import bpy
           math))

(defn clear-mesh-objects []
  (.select-all     bpy.ops/object ** :action "DESELECT")
  (.select-by-type bpy.ops/object ** :type "MESH")
  (.delete         bpy.ops/object))

(clear-mesh-objects)

(defn create-random-material []
  (let [mat  (.new bpy.data/materials ** :name "RandomMaterial")
        _    (set! (.-use-nodes mat) true)
        bsdf (aget (.. mat -node-tree -nodes) "Principled BSDF")]

    (set! (-> bsdf .-inputs (aget "Base Color") .-default-value)
          [(rand) (rand) (rand) 1])
    mat))

(defn create-torus [radius tube-radius location segments]
  (.primitive-torus-add bpy.ops/mesh **
                        :major-radius radius
                        :minor-radius tube-radius
                        :location location
                        :major-segments segments
                        :minor-segments segments)
  (let [material (create-random-material)]
    (-> bpy.context/object .-data .-materials (.append material))))

#_(create-torus 5, 5, [0 0 0] 48)

(defn create-pattern [{:keys [layers-num radius tube-radius]
                       :or {layers-num 2
                            radius 2
                            tube-radius 0.2}}]
  (let [angle-step (/ math/pi 4)]
    (dotimes [i layers-num]
      (let [layer-radius (* radius (inc i))
            objects-num (* 12 (inc i))]
        (dotimes [j objects-num]
          (let [angle (* j angle-step)
                x (* layer-radius (math/cos angle))
                y (* layer-radius (math/sin angle))
                z (* i 0.5)]
            (create-torus (/ radius 2) tube-radius [x y z] 48)))))))

(create-pattern {:layers-num 5})
```

![torus pattern example img](examples/torus-pattern.png)

# Troubleshooting

If you encounter unexplained errors, enable `DEBUG` logging and save the output to a file for inspection. For example:

```python
import logging
from basilisp_blender import log_level_set

log_level_set(logging.DEBUG, filepath="bblender.log")
```

Blender scripting [is not hread safe](https://docs.blender.org/api/current/info_gotcha.html#strange-errors-when-using-the-threading-module). 
As a result, the nREPL server cannot be started into a background thread and still expect calling `bpy` functions to work without corrupting its state.

To work around this limitation, the nREPL server is started in a thread, but client requests are differed into a queue that will be executed later by a `bpy` custom timer function. 
The function is run in the main Blender loop at intervals of 0.1 seconds, avoiding parallel operations that could affect Blender's state.

If necessary, you can adjust this interval to better suit your needs by passing the `interval_sec` argument to the `server_start` function:

```python
from basilisp_blender.nrepl import server_start

shutdown_fn = server_start(port=8889, interval_sec=0.05)
```

# Development

This package uses the [Poetry tool](https://python-poetry.org/docs/) for managing development tasks.

## Testing

You can run tests using the following command:

```bash
$ poetry run pytest 
```
### Integration testing

To run integration tests, set the `$BB_BLENDER_TEST_HOME` environment variable to the root directory of the Blender installation where the development package is installed. See next section on how to facilitate the installation.

```bash
$ export BB_BLENDER_TEST_HOME="~/blender420"
# or on MS-Windows
> $env:BB_BLENDER_TEST_HOME="c:\local\blender420"
```
Then run the integration tests with

```bash
$ poetry run pytest --integration -v
```

### Installing Blender and the Development Package

To download and install Blender in the directory specified by `$BB_BLENDER_TEST_HOME`, use:

```bash
$ poetry run python scripts/blender_install.py 4.2.0
```

To install the development version of the package at the same location, use:

```bash
$ poetry build                                    # build the package
$ poetry run python scripts/bb_package_install.py # install it in Blender
```

# License

This project is licensed under the Eclipse Public License 2.0. See the [LICENSE](LICENSE) file for details.

# Acknowledgments

The nREPL server is a spin-off of [Basilisp](https://github.com/basilisp-lang/basilisp)'s `basilisp.contrib.nrepl-server` namespace.
