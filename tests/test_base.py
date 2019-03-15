# -*- coding: utf-8 -*-
# Copyright 2014 Google Inc. All rights reserved.
#
# Modifications Copyright (C) 2019 GIS OPS UG.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#


"""Tests for client module."""

import responses
import time

import routingpy
from routingpy.routers import options, base
from .test_helper import *
import tests as _test


class RouterMock(base.Router):

    def __init__(self, *args, **kwargs): super(RouterMock, self).__init__(*args, **kwargs)

    def directions(self, *args, **kwargs):
        return self._request(*args, **kwargs)

    def isochrones(self):
        pass

    def distance_matrix(self):
        pass


class BaseTest(_test.TestCase):

    def setUp(self):
        self.router = RouterMock("https://httpbin.org")
        self.params = {'c': 'd', 'a': 'b', '1': '2'}

    def test_options(self):
        options.default_user_agent = "my_agent"
        options.default_timeout = 10
        options.default_retry_timeout = 10

        new_router = RouterMock('https://foo.bar')
        req_kwargs = {'timeout': options.default_timeout,
                      'headers': {
                          'User-Agent': options.default_user_agent,
                          'Content-Type': 'application/json'
                      }}
        self.assertEqual(req_kwargs, new_router._requests_kwargs)

    def test_urlencode(self):
        encoded_params = self.router._generate_auth_url('directions', self.params)
        self.assertEqual("directions?1=2&a=b&c=d", encoded_params)

    @responses.activate
    def test_raise_timeout_retriable_requests(self):
        # Mock query gives 503 as HTTP status, code should try a few times to
        # request the same and then fail on Timeout() error.
        retry_timeout = 3
        query = self.params
        responses.add(responses.POST,
                      'https://httpbin.org/post',
                      json=query,
                      status=503,
                      content_type='application/json')

        client = RouterMock("https://httpbin.org", retry_timeout=retry_timeout)

        start = time.time()
        with self.assertRaises(routingpy.exceptions.Timeout):
            client.directions('/post', {}, post_json=self.params)
        end = time.time()
        self.assertTrue(retry_timeout < end-start < 2 * retry_timeout)

    @responses.activate
    def test_dry_run(self):
        # Test that nothing is requested when dry_run is 'true'

        responses.add(responses.GET,
                      'https://api.openrouteservice.org/directions',
                      body='{"status":"OK","results":[]}',
                      status=200,
                      content_type='application/json')

        req = self.client.request(get_params={'format_out': 'geojson'},
                             url='directions/',
                             dry_run='true')

        self.assertEqual(0, len(responses.calls))
    #
    # @responses.activate
    # def test_key_in_header(self):
    #     # Test that API key is being put in the Authorization header
    #     query = ENDPOINT_DICT['directions']
    #
    #     responses.add(responses.POST,
    #                   'https://api.openrouteservice.org/v2/directions/{}/geojson'.format(query['profile']),
    #                   json=ENDPOINT_DICT['directions'],
    #                   status=200,
    #                   content_type='application/json')
    #
    #     resp = self.client.directions(**query)
    #
    #     self.assertDictContainsSubset({'Authorization': self.key}, responses.calls[0].request.headers)