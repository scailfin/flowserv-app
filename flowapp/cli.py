"""Command line interface for the administrative tasks to configure the
environment, intialize the underlying database, and the create and maintain
workflows in the repository.
"""

import click

from flowserv.app import install_app, list_apps

from flowserv.model.database import DB

import flowserv.config.app as config


@click.group()
def cli():
    """Command line interface for administrative tasks."""
    pass


@cli.command(name='install')
@click.option(
    '-b', '--basedir',
    type=click.Path(exists=True, dir_okay=True, readable=True),
    help='Base directory for API files (overrides FLOWSERV_API_DIR).'
)
@click.option(
    '-c', '--initdb',
    is_flag=True,
    default=False,
    help='Create a fresh database.'
)
@click.option(
    '-n', '--name',
    required=False,
    help='Application title.'
)
@click.option(
    '-d', '--description',
    required=False,
    help='Application sub-title.'
)
@click.option(
    '-i', '--instructions',
    type=click.Path(exists=False),
    required=False,
    help='File containing detailed instructions.'
)
@click.option(
    '-s', '--src',
    type=click.Path(exists=True, file_okay=False, readable=True),
    required=False,
    help='Workflow template directory.'
)
@click.option(
    '-r', '--url',
    required=False,
    help='Workflow template Git repository name or URL.'
)
@click.option(
    '-t', '--specfile',
    type=click.Path(exists=True, dir_okay=False, readable=True),
    required=False,
    help='Optional path to workflow specification file.'
)
def install_workflow(
    basedir=None, initdb=False, name=None, description=None, instructions=None,
    src=None, url=None, specfile=None
):
    """Initialize database and base directories for the flowApp API. The
    configuration parameters for the database are taken from the respective
    environment variables. Creates the API base directory if it does not exist.
    """
    if initdb:
        click.echo('This will erase an existing database.')
        click.confirm('Continue?', default=True, abort=True)
        # Create a new instance of the database
        DB().init()
    # Install the application from the given workflow template.
    app_key = install_app(
        name=name,
        description=description,
        instructions=instructions,
        sourcedir=src,
        repourl=url,
        specfile=specfile,
        basedir=basedir
    )
    click.echo('export {}={}'.format(config.FLOWSERV_APP, app_key))


@cli.command(name='list')
def list_applications():
    """Print listing of installed applications."""
    for name, key in list_apps():
        click.echo('{}\t{}'.format(key, name))
