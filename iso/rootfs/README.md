# RootFS Staging

This directory can be used to stage root filesystem files for the live ISO.
The build script currently generates a temporary rootfs in the build directory.
If you want to customize the live environment, place files here and update
`iso/build-iso.sh` to merge them into the build rootfs.
