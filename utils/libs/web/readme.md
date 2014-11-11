# Frontend web assets

CentralReport includes a web server, used to display data. This web server use some assets (Javascript, CSS, templates).
These assets are already generated in the installer package.

If you must regenerate them, just run: ```build_dependencies.sh -w```

They are generated into the ```centralreport/cr/web/static/``` folder. Raw Javascript and templates are located under
the ```centralreport/cr/web/static_dev/``` folder (this folder is not included in the packaged version).

## NodeJS

The right tool for the right use. We use NodeJS to compile web assets: it must be available on your host if you
want to generate them.

Note: NodeJS is not mandatory if you use the packaged version.
