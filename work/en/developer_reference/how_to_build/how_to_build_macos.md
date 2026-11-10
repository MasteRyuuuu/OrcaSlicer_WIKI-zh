# Build on macOS

How to building with Xcode on MacOS 64-bit.

{{T1}}

## MacOS Tools Required

- Xcode
- CMake
- Git
- gettext
- libtool
- automake
- autoconf
- texinfo
- pkgconf

> [!TIP]
> You can install most of them by running:
>
{{C1}}

> [!IMPORTANT]
> If you've recently upgraded Xcode, be sure to open Xcode at least once and install the required macOS build support.

Point the command-line tools at your Xcode installation and accept the license:

{{C2}}

## MacOS Instructions

1. Clone the repository:

   {{C3}}

2. Build the application:

   {{C4}}

   > [!TIP]
   > If you're on the latest macOS and Xcode, set the deployment target explicitly so the build targets a supported SDK, e.g.:
   >
   > ```bash
   > ./build_release_macos.sh -s -t 15.4
   > ```

3. Open the application:

   {{C5}}

## Debugging in Xcode

To build and debug directly in Xcode:

1. Open the Xcode project:

   {{C6}}

2. In the menu bar:
    - **Product > Scheme > OrcaSlicer**
    - **Product > Scheme > Edit Scheme...**
        - Under **Run > Info**, set **Build Configuration** to `RelWithDebInfo`
        - Under **Run > Options**, uncheck **Allow debugging when browsing versions**
    - **Product > Run**
