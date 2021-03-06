# Copyright 2017, Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# (c) 2017, Kevin Carter <kevin.carter@rackspace.com>

from flask import jsonify, make_response, request
from flask_restful import reqparse

from cruton.api import v1 as v1_api
from cruton.api.v1 import environment


PARSER = reqparse.RequestParser()


class BaseDevice(environment.Environment):
    """Specific environment, datacenter, row, rack, and host devices endpoint."""

    def __init__(self):
        """TODO"""
        super(BaseDevice, self).__init__()
        self.model = self.models.Entities
        self._load_opts()

    def _get(self, ent_id=None, env_id=None, dev_id=None, **kwargs):
        """Common GET method.

        :param ent_id: Entity ID
        :type ent_id: string
        :param ent_id: Environment ID
        :type ent_id: string
        :param dev_id: Device ID
        :type dev_id: string
        :return: list
        """
        return self.utils.get_device(
            self=self, ent_id=ent_id, env_id=env_id, dev_id=dev_id, **kwargs
        )

    def _put(self, ent_id=None, env_id=None, dev_id=None, **kwargs):
        """Common PUT method.

        :param ent_id: Entity ID
        :type ent_id: string
        :param ent_id: Environment ID
        :type ent_id: string
        :param dev_id: Device ID
        :type dev_id: string
        :return: string, int
        """
        return self.utils.put_device(
            self=self, ent_id=ent_id, env_id=env_id, dev_id=dev_id, **kwargs
        )


class Devices(BaseDevice, v1_api.ApiSkelRoot):
    """Specific environment, datacenter, row, rack, and host devices endpoint."""

    def __init__(self):
        """TODO"""
        super(Devices, self).__init__()

    def get(self, ent_id, env_id):
        try:
            return jsonify(self._get(ent_id=ent_id, env_id=env_id))
        except Exception as exp:
            return make_response(jsonify(str(exp)), 400)

    def head(self, ent_id, env_id):
        resp = make_response()
        resp.headers['Content-Devices'] = len(self._get(ent_id=ent_id, env_id=env_id))
        return resp

    def post(self, ent_id, env_id):
        if not isinstance(request.json, list):
            item_list = [request.json]
        else:
            item_list = request.json

        returns = list()
        for item in item_list:
            dev_id = item.pop('dev_id', None)
            if not dev_id:
                return make_response(
                    '<dev_id> is missing from the POST', 400
                )
            else:
                notice, code = self._put(
                    ent_id=ent_id,
                    env_id=env_id,
                    dev_id=dev_id,
                    args=item
                )
                if code >= 300:
                    return notice, code
                else:
                    returns.append(notice)
        else:
            return returns, 201


class Device(BaseDevice, v1_api.ApiSkelPath):
    """Specific environment, datacenter, row, rack, and host devices endpoint."""

    def __init__(self):
        """TODO"""
        super(Device, self).__init__()
        self._dev_id = None

    @property
    def dev_id(self):
        """Host Identification

        :param host_id: Host ID
        :type host_id: string
        """
        return self._dev_id

    def get(self, ent_id, env_id, dev_id=None):
        try:
            return jsonify(
                self._friendly_return(
                    self._get(ent_id=ent_id, env_id=env_id, dev_id=dev_id)[0]
                )
            )
        except self.exp.InvalidRequest:
            return make_response(jsonify('DoesNotExist'), 404)
        except Exception as exp:
            return make_response(jsonify(str(exp)), 400)

    def head(self, ent_id, env_id, dev_id=None):
        resp = make_response()
        resp.headers['Content-Device-Exists'] = len(self._get(
            ent_id=ent_id, env_id=env_id, dev_id=dev_id)
        ) > 0
        return resp

    def put(self, ent_id, env_id, dev_id=None):
        notice, code = self._put(
            ent_id=ent_id,
            env_id=env_id,
            dev_id=dev_id,
            args=self.args
        )
        if code >= 300:
            return notice, code
        else:
            return notice, 201
