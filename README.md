# Template for a web application

Template for the application that uses:
- `FastApi` + `Jinja` (Python) on backend
- `htmx` + `Lit components` on the frontend

## Backend

## Frontend

Frontend uses the mixture of plain `html` (in `app/templates`) that uses the `htmx` (for basic interactivity) and custom web components, created using `Lit components` (where more interactivity is required).

To create custom web components, we are using `TypeScript` + `Vite`.
Inside `index.jinja` there is a switch that changes the source from which the scripts are loaded:
- on development - from `Vite` HMR server, that compiles the sources on the fly and makes it possible to develop using hot-reloading.
- on production - from `static` dir, that will be created by `vite build` command.

Note that `fronted/index.html` exists only for `Vite` development server purposes - it is not used by the application. 

Read more about this approach [here](https://www.lorenstew.art/blog/eta-htmx-lit-stack)

## Development

Application is meant to be developed inside the provided *devcontainer*. This ensures that development and production environments have the same dependencies.

To spin-up the dev container TBD
