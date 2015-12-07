SHARE_URL = 'https://osf.io/api/v1/share/search/'

URI_PREFIX = 'https://vivo.ufl.edu/individual/n'

UPDATE_TEMPLATE = """PREFIX vivo: <http://vivoweb.org/ontology/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX bibo: <http://purl.org/ontology/bibo/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX vitro: <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX owl:   <http://www.w3.org/2002/07/owl#>

{}
"""

EMAIL_RDF = """vcard:TimeZone  a   owl:Class ;
        rdfs:label  "Time Zone"@en-US .

vcard:Addressing  a  owl:Class ;
        rdfs:label  "Addressing"@en-US .

vcard:Geographical  a  owl:Class ;
        rdfs:label  "Geographical"@en-US .

vcard:Security  a   owl:Class ;
        rdfs:label  "Security"@en-US .

vcard:Communication  a  owl:Class ;
        rdfs:label  "Communication"@en-US .

vcard:Code  a       owl:Class ;
        rdfs:label  "Code"@en-US .

vcard:Explanatory  a  owl:Class ;
        rdfs:label  "Explanatory"@en-US .

vcard:Email  a      owl:Class ;
        rdfs:label  "Email"@en-US .

vcard:Calendar  a   owl:Class ;
        rdfs:label  "Calendar"@en-US .

vcard:Geo  a        owl:Class ;
        rdfs:label  "Geo"@en-US .

vcard:Identification  a  owl:Class ;
        rdfs:label  "Identification"@en-US .

vcard:Work  a       owl:Class ;
        rdfs:label  "Work"@en-US .

owl:Thing  a    owl:Class .

vcard:Type  a       owl:Class ;
        rdfs:label  "Type"@en-US .

vcard:Organizational  a  owl:Class ;
        rdfs:label  "Organizational"@en-US ."""



EMAIL_RDF_TEMPLATE = """<{contributor}>
        a               vcard:Individual , obo:IAO_0000030 , obo:BFO_0000001 , owl:Thing ,
                        vcard:Kind , obo:ARG_2000379 , obo:BFO_0000031 , obo:BFO_0000002 ;
        vcard:hasEmail  <{email_uri}> .

<{email_uri}>
        a            vcard:Email, vcard:Explanatory, vcard:Security, vcard:Geo , owl:Thing , vcard:Geographical ,
                     foaf:Document , vcard:Communication , vcard:Work, vcard:Code , vcard:Addressing,
                     vcard:Identification , vcard:Organizational, vcard:Type, vcard:Calendar, vcard:TimeZone ;
        rdfs:label   "RDF description of {email_uri}" ;
        <http://purl.org/dc/elements/1.1/date>
                "2015-12-06T06:54:14"^^xsd:dateTime ;
        <http://purl.org/dc/elements/1.1/publisher>
                <http://vivo.ufl.edu> ;
        <http://purl.org/dc/elements/1.1/rights>
                <http://vivo.ufl.edu/termsOfUse> ;
        <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#mostSpecificType>
                vcard:Email , vcard:Work ;
        vcard:email  "{email}" .
"""