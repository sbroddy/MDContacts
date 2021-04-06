#!/usr/bin/env python3

from lxml import etree
from urllib.request import urlopen

#Constants
#NS sets up various XML namespaces and loads them
#into a dictionary for reference later.
NS = dict(md="urn:oasis:names:tc:SAML:2.0:metadata",
          ds='http://www.w3.org/2000/09/xmldsig#',
          mdui="urn:oasis:names:tc:SAML:metadata:ui",
          mdattr="urn:oasis:names:tc:SAML:metadata:attribute",
          mdrpi="urn:oasis:names:tc:SAML:metadata:rpi",
          shibmd="urn:mace:shibboleth:metadata:1.0",
          xrd='http://docs.oasis-open.org/ns/xri/xrd-1.0',
          pyff='http://pyff.io/NS',
          xml='http://www.w3.org/XML/1998/namespace',
          saml="urn:oasis:names:tc:SAML:2.0:assertion",
          xs="http://www.w3.org/2001/XMLSchema",
          xsi="http://www.w3.org/2001/XMLSchema-instance",
          ser="http://eidas.europa.eu/metadata/servicelist",
          eidas="http://eidas.europa.eu/saml-extensions",
          remd="http://refeds.org/metadata",
          icmd="http://id.incommon.org/metadata")

#MDOBJ = 'https://mds.edugain.org/edugain-v1.xml'
MDOBJ = "./edugain-v1.xml"

try:
    #root = etree.parse(urlopen(MDOBJ))
    root = etree.parse(MDOBJ)
    print("Retrieved MD from ", MDOBJ)
except:
    print("unable to retrieve MD from ", MDOBJ)
    exit()


for i in root.findall(".//{%s}EntityDescriptor" % NS['md']):
    entityID = i.get('entityID')
    for r in i.findall(".//{%s}RegistrationInfo" % NS['mdrpi']):
        RegBy = r.get('registrationAuthority')
    OrgID = i.find(".//{%s}OrganizationName" % NS['md']).text
    for z in i.findall(".//{%s}ContactPerson" % NS['md']):
        if z is not None:
            contactType = z.get("contactType")
            try:
                address = z.find(".//{%s}EmailAddress" % NS['md']).text
                address = address.replace('mailto:', '')
            except:
                address = "null"
            if contactType == "other":
                try:
                    sec = z.get("{%s}contactType" % NS['icmd'])
                    if sec == "http://id.incommon.org/metadata/contactType/security":
                        contactType = "security"
                except:
                    pass
                try:
                    sec = z.get("{%s}contactType" % NS['remd'])
                    if sec == "http://refeds.org/metadata/contactType/security":
                        contactType = "security"
                except:
                    pass
            print(entityID, RegBy, contactType, address, sep=',')
