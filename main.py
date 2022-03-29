import collections
import pprint
from requests import Session
from requests_negotiate_sspi import HttpNegotiateAuth
import xmltodict
import zeep

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
SRV_WSDL = 'http://dirinteg.rimera.com:3300/IntegrationService.svc?wsdl'


def parse_requisite(item: list):
    res_dict = {}
    for it in item:
        if isinstance(it, dict):
            text = it.get('#text')
            name = it.get('@Name', 'Noname')
            val = None
            if text:
                req_type = it.get('@Type', 'String')
                if req_type in ('String', 'Pick'):
                    val = text
                elif req_type == 'Integer':
                    val = int(text)
                elif req_type == 'Reference':
                    val = it.get('@DisplayValue')
                else:
                    print(f"Name = {name}, type={req_type}, value={text}, all_value={it}")
                    val = text
                res_dict[name] = val
    return res_dict


def get_requisite(item: dict, level: int = 0):
    reqs = []
    for k, v in item.items():
        if k == 'Requisite':
            req_dict = parse_requisite(v)
            reqs += [req_dict]
        elif isinstance(v, dict):
            child = get_requisite(v, level+1)
            if child:
                reqs += child
    return reqs


def parse(xml: str) -> list:
    dct = xmltodict.parse(xml)
    return get_requisite(dct)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    session = Session()
    auth = HttpNegotiateAuth()
    session.auth = auth
    client = zeep.Client(wsdl=SRV_WSDL, transport=zeep.Transport(session=session))
    # client = zeep.Client(wsdl=SRV_WSDL)
    # client_token = client.bind('IntegrationServices', 'HTTPTokenSrv')
    # token = client_token.OpenUserToken()
    # print(token)
    # print(dir(client.service))
    # print(session.get('https://directum.rimera.com/', verify=False))
    # xml = client.service.GetReferenceRequisite(ReferenceName='ОРГ')
    xml = client.service.GetReferenceChangedFrom(ReferenceName='ОРГ', DateFrom='2020-01-01T00:00:00')     # RecordKey=2587928)
    print(xml)
    dct = parse(xml)
    pprint.pprint(dct)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
