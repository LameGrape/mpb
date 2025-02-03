# mappy build tool

**mpb** is a build tool I made cause I really didn't want to figure out how to use make, CMake, or anything else that existed for compiling C projects. It is not coded efficiently in any stretch of the imagination, and I don't care to do so. It works for what I need, and if it works for you too, thats cool.

mpb uses a basic timestamp cache to only compile files that have changed since the last build, speeding up compilation times. It can support multiple languages (only two right now), and projects can be configured through a simple, minimal syntax, mostly language agnostic build file.

I'll make prebuilt binaries when I feel like it. The source code can be compiled using (theoretically) any Python exectuable packager. I use PyInstaller set to one file mode.