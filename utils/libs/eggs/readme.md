# Python egg libraries

CentralReport needs external Python libraries. These libs are retrieved and built by
[Buildout](https://github.com/buildout/buildout).


Libraries are already included in the installer package: they are built during the ```make_package.sh``` script,
located at the root of the project.

Libraries are saved into the ```centralreport/libs/``` folder, in egg format.

If you must regenerate them, just run: ```build_dependencies.sh -p```
