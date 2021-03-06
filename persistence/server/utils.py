#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
'''
Faraday Penetration Test IDE
Copyright (C) 2016  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''
import re
import logging

logger = logging.getLogger(__name__)


from persistence.server.server_io_exceptions import MoreThanOneObjectFoundByID


def force_unique(lst):
    """Takes a list and return its only member if the list len is 1,
    None if list is empty or raises an MoreThanOneObjectFoundByID error
    if list has more than one element.
    """
    if len(lst) == 1:
        return lst[0]
    elif len(lst) == 0:
        return None
    else:
        raise MoreThanOneObjectFoundByID(lst)


def get_object_properties(obj):
    # this sometimes is the metadata object and sometimes its a dictionary
    # a better fix awaits in a brighter future
    metadata = obj.getMetadata()
    if not isinstance(obj.getMetadata(), dict):
        metadata = metadata.toDict()

    return {
        'name': obj.getName(),
        'description': obj.getDescription(),
        'metadata': metadata,
        'owned': obj.isOwned(),
        'owner': obj.getOwner()
    }


def get_host_properties(host):
    host_dict = {
        'os': host.getOS(),
        'hostnames': host.getHostnames()
    }
    if host.getDefaultGateway():
        host_dict['default_gateway'] = host.getDefaultGateway()
    host_dict.update(get_object_properties(host))
    # name was removed from host and changed to ip
    ip = host_dict.pop('name')
    if 'ip' not in host_dict and ip:
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip) is None:
            logger.warn('Host with invalid IP address detected.')
        host_dict['ip'] = ip
    return host_dict


def get_service_properties(service):
    service_dict = {
        'ports': service.getPorts(),
        'protocol': service.getProtocol(),
        'status': service.getStatus(),
        'version': service.getVersion(),
        'parent': service.getParent()
    }
    service_dict.update(get_object_properties(service))
    return service_dict


def get_vuln_properties(vuln):
    vuln_dict = {
        'confirmed': vuln.getConfirmed(),
        'data': vuln.getData(),
        'refs': vuln.getRefs(),
        'severity': vuln.getSeverity(),
        'resolution': vuln.getResolution(),
        'desc': vuln.getDesc(),
        'status': vuln.getStatus(),
        'policyviolations': vuln.getPolicyViolations(),
        'parent': vuln.getParent(),
        'parent_type': vuln.getParentType(),
    }
    vuln_dict.update(get_object_properties(vuln))
    return vuln_dict


def get_vuln_web_properties(vuln_web):
    vuln_web_dict = {
        'method': vuln_web.getMethod(),
        'params': vuln_web.getParams(),
        'request': vuln_web.getRequest() or '',
        'response': vuln_web.getResponse() or '',
        'website': vuln_web.getWebsite(),
        'path': vuln_web.getPath(),
        'pname': vuln_web.getPname() or '',
        'query': vuln_web.getQuery(),
        'status': vuln_web.getStatus(),
        'parent': vuln_web.getParent(),
        'parent_type': vuln_web.getParentType(),
    }
    vuln_web_dict.update(get_object_properties(vuln_web))
    vuln_web_dict.update(get_vuln_properties(vuln_web))
    return vuln_web_dict


def get_note_properties(note):
    text = note.getText()
    if note.getName():
        text = '{0}\n{1}'.format(note.getName(), note.getText())
    note_dict = {
        'text': text,
        'object_id': note.getObjectID(),
        'object_type': note.getObjectType()
    }
    note_dict.update(get_object_properties(note))
    return note_dict


def get_credential_properties(credential):
    cred_dict = {
        'username': credential.getUsername(),
        'password': credential.getPassword(),
        'parent': credential.getParent(),
        'parent_type': credential.getParentType(),
    }
    cred_dict.update(get_object_properties(credential))
    return cred_dict


def get_command_properties(command):
    return {
        'command': command.command,
        'tool': command.command,
        'user': command.user,
        'ip': command.ip,
        'hostname': command.hostname,
        'itime': command.itime,
        'duration': command.duration,
        'params': command.params,
        'import_source': command.import_source,
    }
