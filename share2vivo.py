# -*- coding: utf-8 -*-
import click
import time
import share2vivo.SHAREharvester as harvester

WELCOME_MSJ = """SHARE to VIVO v0.0:
Command line interface to harvest SHARE data and covert it to VIVO RDF format."""


@click.command()
@click.option('--uri_prefix', help='Prefix pattern to VIVO URIs')
@click.option('--csv', type=click.File('rb'), help='CSV file with two columns one with the set of authnames\n' +
                                                   ' for a given author and another one for the ORCID')
@click.option('--output', default='./', type=click.Path(exists=True))
@click.option('--authnames', help='Pipe separated list of authnames'
                                  'eg. "M. Conlon|Mike Conlon|Conlon, Mike"')
@click.option('--orcid', help='ORCID')
def cli(uri_prefix, authnames, orcid, csv, output):
    click.secho(WELCOME_MSJ, fg='blue', bold=True)
    start_time = time.time()

    if not (csv or authnames):
        click.secho("You must provide and author name or a csv file.", fg='red', bold=True)
        return
    if csv:
        harvester.share2vivo_csv(csv, output)
    else:
        harvester.share2vivo(authnames, orcid, output)
    elapsed_time = time.time() - start_time
    click.secho("Elapsed time {}.".format(elapsed_time), fg='green')


if __name__ == '__main__':
    cli()
