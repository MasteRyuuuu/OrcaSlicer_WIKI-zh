# Build Overview

OrcaSlicer builds from source on Windows, macOS, and Linux. Each platform has its own tools and build script:

- [Build on Windows]({{L1}})
- [Build on macOS]({{L2}})
- [Build on Linux]({{L3}})
- [Compiler Caching]({{L4}})

## Build Stages

Every platform builds in the same two stages, and each build script can run either on its own:

1. **Dependencies.** Third-party libraries such as Boost, wxWidgets, TBB and OpenCV are compiled once under `deps/` and installed into a prefix there.
2. **OrcaSlicer.** The application is compiled and linked against that prefix.

The dependency stage is skipped on later builds unless you delete its build directory, so the first build takes far longer than later ones. It is also why a dependency change has to be rebuilt on its own; each platform page explains how.

## Running the Tests

See [How to Test]({{L5}}).

## Portable User Configuration

Place a folder named `data_dir` next to the OrcaSlicer executable and OrcaSlicer uses it as its configuration directory. That gives you a portable installation on a USB stick, or several profile sets kept isolated.

Nothing needs recompiling, and each copy set up this way keeps its own user data.

### Example Folder Structure

{{C1}}
