import requests
import json
import random
import click
import csv
from settings.settings import *


uri_count = 0
uris = []
random.seed()


def create_file(rdf, output, filename):
    filename = output + '{}.ttl'.format(filename)
    f = open(filename, 'w')
    rdf_utf = rdf.encode('UTF-8')
    rdf_utf = UPDATE_TEMPLATE.format(rdf_utf)
    f.write(rdf_utf)
    f.close()


def generate_uri():
    number = str(random.random()).split('.')[1]
    return u''+URI_PREFIX+'{}'.format(number)


def harvest(authnames, orcid_id=''):
    query_url = ''
    authnames = '"' + authnames.replace('|', '"|"') + '"'
    if authnames:
        query_url += 'contributors.name:{}'.format(authnames)
    if orcid_id:
        query_url += ' OR ' if query_url else query_url
        query_url += 'contributors.sameAs:"{}"'.format(orcid_id)
    r = requests.get(SHARE_URL, params={'q': query_url})
    response = json.loads(r.content)

    return response


def process_document(document, doc_uri):
    rdf = ''
    if document['title']:
        rdf += u'<{}> rdfs:label "{}" .\n'.format(doc_uri, document['title'].replace("\n", " "))
        if document['uris']:
            canonical_uri = document['uris']['canonicalUri']
            if 'http://dx.doi.org/' in canonical_uri:
                begin_index = canonical_uri.index('org/') + 4
                doi = canonical_uri[begin_index:]
                rdf += u'<{}> bibo:doi "{}" .\n'.format(doc_uri, doi)
    if 'tags' in document:
        for tag in document['tags']:
            rdf += u'<{}> vivo:freetextKeyword "{}" .\n'.format(doc_uri, tag)
    if 'description' in document and document['description']:
        rdf += u'<{}> bibo:abstract "{}" .\n'.format(doc_uri, document['description'])
    return rdf


def process_contributor(contributor, contributor_uri):
    vcard_uri = generate_uri()
    name_uri = generate_uri()
    contributor_rdf = u"""<{contributor}> a foaf:Person .
<{contributor}> rdfs:label "{name}" .
<{contributor}> obo:ARG_2000028 <{vcard}>.
<{vcard}> vcard:hasName <{name_uri}> .
<{name_uri}> vcard:familyName "{family_name}" .
<{name_uri}> vcard:givenName "{given_name}" .
"""
    contributor_rdf = contributor_rdf.format(contributor=contributor_uri,
                                             vcard=vcard_uri,
                                             name_uri=name_uri,
                                             name=contributor['name'],
                                             given_name=contributor['givenName'],
                                             family_name=contributor['familyName'])
    if 'email' in contributor and contributor['email']:
        email_uri = generate_uri()
        contributor_rdf += EMAIL_RDF_TEMPLATE.format(contributor=contributor_uri,
                                                     email_uri=email_uri,
                                                     email=contributor['email'])
    if 'affiliation' in contributor and contributor['affiliation']:
        org_uri = generate_uri()
        org_name = contributor['affiliation']['name']
        contributor_rdf += u'{} a foaf:Organization'.format(org_uri)
        contributor_rdf += u'{} foaf:name {}'.format(org_uri, org_name)
        contributor_rdf += u'{} foaf:member {}'.format(contributor_uri, org_uri)
    return contributor_rdf


def generate_rdf(response):
    rdf = ''
    has_email = 0
    if response['count']:
        click.secho('{} documents to be harvested'.format(response['count']), fg='yellow', bold=True)
        contributors_uris = {}
        for document in response['results']:
            doc_uri = generate_uri()
            rdf += process_document(document, doc_uri)
            if document['contributors']:
                for contributor in document['contributors']:
                    authorship_uri = generate_uri()
                    full_name = contributor['givenName'] + '_' + contributor['familyName']
                    contributor_rdf = ''
                    if 'email' in contributor and contributor['email']:
                        has_email += 1
                    if full_name not in contributors_uris:
                        contributors_uris[full_name] = generate_uri()
                        contributor_rdf += process_contributor(contributor, contributors_uris[full_name])
                    contributor_uri = contributors_uris[full_name]
                    contributor_rdf += u"""<{authorship}> a vivo:Authorship .
<{authorship}> vivo:relates <{doc}> .
<{contributor}> vivo:relatedBy <{authorship}> .\n
"""
                    contributor_rdf = contributor_rdf.format(authorship=authorship_uri,
                                                             doc=doc_uri,
                                                             contributor=contributor_uri)
                    rdf += contributor_rdf
    rdf += EMAIL_RDF if has_email else ''
    return rdf


def share2vivo(authnames, orcid, output):
    response = harvest(authnames, orcid)
    rdf = generate_rdf(response)
    create_file(rdf, output, authnames.split('|')[0])


def share2vivo_csv(csv_file, output):
    spamreader = csv.reader(csv_file, delimiter=';', quotechar='"')
    for row in spamreader:
        response = harvest(row[0], row[1])
        rdf = generate_rdf(response)
        create_file(rdf, output, row[0].split('|')[0])

