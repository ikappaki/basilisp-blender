# Table of contents
-  [`basilisp-blender.bpy-utils`](#basilisp-blender.bpy-utils) 
    -  [`nrepl-server-start`](#basilisp-blender.bpy-utils/nrepl-server-start) - Starts the nrepl-server in async mode according to <code>opts</code>, using a bpy timer to schedule any pending client work.
-  [`basilisp-blender.utils`](#basilisp-blender.utils) 
    -  [`class-make*`](#basilisp-blender.utils/class-make*) - Creates and returns a Python class with the given <code></code>class-name<code></code>, inheriting from the list of <code></code>class-and-interfaces<code></code>.

-----
# <a name="basilisp-blender.bpy-utils">basilisp-blender.bpy-utils</a>






## <a name="basilisp-blender.bpy-utils/nrepl-server-start">`nrepl-server-start`</a><a name="basilisp-blender.bpy-utils/nrepl-server-start"></a>
``` clojure

(nrepl-server-start {:keys [host port nrepl-port-dir interval-sec], :as opts, :or {port 0, interval-sec 0.2}})
```
Function.

Starts the nrepl-server in async mode according to `opts`, using a
  bpy timer to schedule any pending client work.

  `opts` is a map that can have the following keys

  `:host` The interface address the server should be bound to. It
  defaults to 127.0.0.1 if not given or empty.

  `:interval-sec` The interval in seconds for executing pending
  work. Defaults to 200ms.

  `:port` The port number the server should listen to. It defaults to
  0, which indicates a random available port number.

  `:nrepl-port-dir` The directory where the `.nrepl-port` file should
  be created at. It defaults to the current working directory if not
  given or empty.

  It returns a map with the following keys

  `:error` An error message in case the server could not be started.

  `:host` The address the server is bound to.

  `:nrepl-port-file` The path to the `.nrepl-port` file with the port
  number the server is listening to.

  `:port` The port the server is listening to.

  `:shutdown!` A function to shutdown the server and stop the bpy
  timer.
<p><sub><a href="https://github.com/ikappaki/basilisp-blender/blob/master/src/basilisp_blender/bpy_utils.lpy#L10-L83">Source</a></sub></p>

-----
# <a name="basilisp-blender.utils">basilisp-blender.utils</a>






## <a name="basilisp-blender.utils/class-make*">`class-make*`</a><a name="basilisp-blender.utils/class-make*"></a>
``` clojure

(class-make* class-name class-and-interfaces fields & fns)
```
Macro.

Creates and returns a Python class with the given ``class-name``,
  inheriting from the list of ``class-and-interfaces``. The class is
  defined with the given ``fields`` and ``fns`` methods.

  Each field in ``fields`` must include at least one of the following
  metadata keys, otherwise, an error will be signaled:

  `:default` The default value for the field.

  `:tag` A type annotation for the field.

  Within the ``fns`` methods, field names can be accessed directly as
  functions by prefixing them with `-`, e.g., `(-field)`.

  The ``fns`` parameter defines the methods of the class. Each method
  should be specified in the following form:

  (method-name1 docstring-maybe [args...] body)

  Inside the method body, the `self` symbol is available to refer to
  the instance of the class.

  Methods can accept Python keyword arguments by specifying the
  `:kwargs` option in the method's metadata. For example:

  ^{:kwargs :collect} (method-name [args... {:as kwargs}]).
<p><sub><a href="https://github.com/ikappaki/basilisp-blender/blob/master/src/basilisp_blender/utils.lpy#L4-L91">Source</a></sub></p>
