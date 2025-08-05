# Template for a web application

Template for the application that uses:

- `FastApi` + `Jinja` (Python) on backend
- `htmx` + `Lit components` on the frontend

## Backend

## Frontend

Frontend uses the mixture of plain `html` (in `app/templates`) that uses the `htmx` (for basic interactivity) and custom
web components, created using `Lit components` (where more interactivity is required).

To create custom web components, we are using `TypeScript` + `Vite`.
Inside `index.jinja` there is a switch that changes the source from which the scripts are loaded:

- on development - from `Vite` HMR server, that compiles the sources on the fly and makes it possible to develop using
  hot-reloading.
- on production - from `static` dir, that will be created by `vite build` command.

Note that `fronted/index.html` exists only for `Vite` development server purposes - it is not used by the application.

Read more about this approach [here](https://www.lorenstew.art/blog/eta-htmx-lit-stack)

## Development

**Not valid any more**
Application is meant to be developed inside the provided *devcontainer*. This ensures that development and production
environments have the same dependencies.

To spin-up the dev container:

- Create a new project based on this template
- Clone a new project from Github
- Open Jetbrains Gateway or in Pycharm go `File->Remote Development`
- Select `Connections->Dev Containers->New Dev Container->From Local Project` and provide the path to cloned
  `.devcontainer` file
  ![create_devcontainer.png](docs/create_devcontainer.png)

> [!NOTE]
> You can also use `From VCS Project` option but be aware
> of [this ticket](https://youtrack.jetbrains.com/issue/IJPL-196106). In this mode, project will be cloned ONLY ONCE and
> then reused. You are risking that the devcontainer won't be created with the newest code if you are not managing the
> jetbrains docker volumes manually.

- Select `Build Container and Continue`

**New approach*
Application is meant to be developed locally, with the provided run configuration. Each component of the application has
an associated run configuration — this setup increases the ability to debug the app:

- on the frontend side, we are spinning up the `Vite` dev server, that will handle all of the `TypeScript` code that
  defines the web components
    - in the run configuration, we are launching the `Chrome` browser with the specified debugging port. This port will
      allow to debug `TypeScript/Javascript` code from Pycharm by setting the breakpoints (like any Python code)
- on the backend, we are running the `FastApi` app - to lunch it, we are using the predefined run configuration,
  provided by Pycharm
    - here the debugging is also as simple as setting the breakpoint
- Celery - TBD
- app dependencies like a database—those are defined in a docker compose file and also specified in run configuration.
  Components that require those dependencies will define `Before launch` task(s), that will spin up the docker
  containers specified in the `docker-compose` file.

Finally, all of those run configurations are grouped inside `Compound configuration` called `Full app`. This is really
the main entrypoint for the application. Once started in debug mode, it will allow setting the breakpoints in all
components of the system, without reloading or adding additional config.

#### About existing configurations

##### `Database`

Spins up the database, defined in the docker container. To work correctly with Pycharm, there are two important points:

- custom healthcheck for `db` service in `compose.yml`. It is necessary because by default, `postgres` user is used to
  perform the health check. Since we are defining custom user, we need to tell postgres service to use it. Otherwise,
  Pycharm will not know that service is healthy and will keep waiting for it forever.
- docker run needs to have `--detached` option. Otherwise, the run configuration task will never finish and all
  dependant configurations (like `Backend`) will keep waiting.
  ![db_run_config.png](docs/db_run_configuration.png)

#### `Backend`

#### `Frontend`

Setups the `Vite` development HMR server.

- the actual config for the frontend is in the `app/frontend/package.json` file
- run configuration selects `dev` command, defined in the `package.json`

  ![frontend_run_configuration](docs/frontend_run_configuration_main.png)
- Pycharm also spins up browser (Chrome) + `Frontend Javascript` run configuration. This way Pycharm is able to allow
  debugging the `JavaScript` code inside the IDE.

  ![frontend_run_configuration_browser](docs/frontend_run_configuration_browser.png)

### Why local development without devcontainer?

Devcontainer integration was evaluated in the context of the local development. Investigation is indicating that usage
of devcontainers with Pycharm has some limitations that make them a less convenient option, compared to *raw* local
development.
To name a few:

- You cannot run the browser with debugging port, to which pycharm will attach to (for `Javascript` debugging)
- Gateway UI is buggy and often hangs. For example, sometimes you are not able to rebuild/remove the devcontainer
- IDE settings are not preserved between different dev containers
- The whole process of creating the devcontainer takes some time
- AI integration in devcontainers is poor—for example, you cannot use AI features in the terminal

... and more.

Truly local development, based on the Python virtual envs and node modules, downloaded for the project, makes it much
easier to develop.
The downside is the fact that when working on a production version of your app, there is a risk that the environment
will not match. This can be minimized by using os that is close to production target, like `Ubuntu`.
In this approach there is still a gap between development and production setup.

How can we address it? TBD

## Handling the database

Project uses `SqlAlchemy` as a main ORM. In addition, it uses `Alembic` to perform automatic database migrations.

To set up `Alembic` following customizations were needed:

- in `alembic/env.py` we are overwriting static url to the database, defined in `alembic.ini` file, to the value created
  in `config`, based on the content of `.env` file.
- in `alembic/env.py` we are pointing to `Base` class for our table models. This will allow automatically creating the
  migration revisions.

To perform migration (move the database to the newest state defined by the migration file):

```commandline
alembic upgrade head
```

To create a migration file (create `Python` script that will perform SQL operations to reflect the current state of data
models):

```commandline
alembic revision --autogenerate -m "migration message"
```

To be decided:

- when to perform the migrations during development? Maybe create a bash script and run configuration based on it. This
  run configuration can be added to `Before launch` of `Backend` run configuration.
- when to perform the migrations on a production environment? As a *fake container*, that is executed before the app
  actually starts? Airflow does something similar.

## ToDo

- `docker-compose` shall contain only production settings - deployment from the image. `devcontainer` file(s) are build
  based on the Dockerfile, not `docker-compose`. `.env` file is shared - is this possible?
- remove devcontainer dependencies
- add datapoints to db
- create chart web component