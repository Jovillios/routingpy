# -*- coding: utf-8 -*-
# Copyright (C) 2019 GIS OPS UG
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

"""
Core client functionality, common across all API requests.
"""
from .base import Router
from routingpy import convert

from operator import itemgetter

class Graphhopper(Router):
    """Performs requests to the Graphhopper API services."""

    _DEFAULT_BASE_URL = "https://graphhopper.com/api/1"

    def __init__(self, api_key=None, base_url=_DEFAULT_BASE_URL, user_agent=None, timeout=None,
                 retry_timeout=None, requests_kwargs={}, retry_over_query_limit=False):

        """
        Initializes an graphhopper client.

        :param key: GH API key. Required if https://graphhopper.com/api is used.
        :type key: str

        :param base_url: The base URL for the request. Defaults to the GH API
            server. Should not have a trailing slash.
        :type base_url: str

        :param timeout: Combined connect and read timeout for HTTP requests, in
            seconds. Specify "None" for no timeout.
        :type timeout: int

        :param retry_timeout: Timeout across multiple retriable requests, in
            seconds.
        :type retry_timeout: int

        :param requests_kwargs: Extra keyword arguments for the requests
            library, which among other things allow for proxy auth to be
            implemented. See the official requests docs for more info:
            http://docs.python-requests.org/en/latest/api/#main-interface
        :type requests_kwargs: dict

        :param queries_per_minute: Number of queries per second permitted.
            If the rate limit is reached, the client will sleep for the
            appropriate amount of time before it runs the current query.
            Note, it won't help to initiate another client. This saves you the
            trouble of raised exceptions.
        :type queries_per_minute: int
        """

        if base_url == self._DEFAULT_BASE_URL and api_key is None:
            raise KeyError("API key must be specified.")
        self.key = api_key
     
        super(Graphhopper, self).__init__(base_url, user_agent, timeout, retry_timeout, requests_kwargs, retry_over_query_limit)

    def directions(self, coordinates, profile, format, optimize=None, instructions=None, locale=None,
                   elevation=None, points_encoded=None, calc_points=None, debug=None,
                   point_hint=None, details=None, ch_disable = None, 
                   weighting=None, heading=None, heading_penalty=None, 
                   pass_through=None, block_area=None, avoid=None, algorithm=None, round_trip_distance=None, round_trip_seed = None,
                   alternative_route_max_paths = None, alternative_route_max_weight_factor = None, 
                   alternative_route_max_share_factor = None, dry_run=None):
        """Get directions between an origin point and a destination point.

        For more information, visit https://openrouteservice.org/documentation/.

        :param coordinates: The coordinates tuple the route should be calculated
            from in order of visit.
        :type coordinates: list, tuple

        :param profile: The vehicle for which the route should be calculated. 
            Default "car".
            Other vehicle profiles are listed here: 
            https://graphhopper.com/api/1/docs/supported-vehicle-profiles/
        :type profile: str

        :param format: Specifies the resulting format of the route, for json the content type will be application/json. 
            Default "json".
        :type format: str

        :param language: Language for routing instructions. The locale of the resulting turn instructions. 
            E.g. pt_PT for Portuguese or de for German. Default "en".
        :type language: str

        :param optimize: If false the order of the locations will be identical to the order of the point parameters. 
            If you have more than 2 points you can set this optimize parameter to true and the points will be sorted 
            regarding the minimum overall time - e.g. suiteable for sightseeing tours or salesman. 
            Keep in mind that the location limit of the Route Optimization API applies and the credit costs are higher! 
            Note to all customers with a self-hosted license: this parameter is only available if your package includes 
            the Route Optimization API. Default False.
        :type geometry: bool

        :param instructions: Specifies whether to return turn-by-turn instructions.
            Default True.
        :type instructions: bool

        :param elevation: If true a third dimension - the elevation - is included in the polyline or in the GeoJson. 
            IMPORTANT: If enabled you have to use a modified version of the decoding method or set points_encoded to false. 
            See the points_encoded attribute for more details. Additionally a request can fail if the vehicle does not 
            support elevation. See the features object for every vehicle.
            Default False.
        :type elevation: bool

        :param points_encoded: If false the coordinates in point and snapped_waypoints are returned as array using the order 
            [lon,lat,elevation] for every point. If true the coordinates will be encoded as string leading to less bandwith usage. 
            Default True
        :type elevation: bool

        :param calc_points: If the points for the route should be calculated at all printing out only distance and time.
            Default True
        :type elevation: bool

        :param debug: If true, the output will be formated.
            Default False
        :type elevation: bool
        
        :param point_hint: Optional parameter. Specifies a hint for each point parameter to prefer a certain street for the 
            closest location lookup. E.g. if there is an address or house with two or more neighboring streets you can control 
            for which street the closest location is looked up.
        :type point_hint: bool

        :param details: Optional parameter. Optional parameter to retrieve path details. You can request additional details for the 
            route: street_name and time. For all motor vehicles we additionally support max_speed, toll (no, all, hgv), 
            road_class (motorway, primary, ...), road_environment, and surface. The returned format for one details 
            is [fromRef, toRef, value]. The ref references the points of the response. Multiple details are possible 
            via multiple key value pairs details=time&details=toll
        :type details: list of str

        :param ch_disable: Always use ch_disable=true in combination with one or more parameters of this table. 
            Default False.
        :type ch_disable: bool

        :param weighting: Which kind of 'best' route calculation you need. Other options are shortest 
            (e.g. for vehicle=foot or bike) and short_fastest if not only time but also distance is expensive.
            Default "fastest".
        :type weighting: str           
        
        :param heading: Optional parameter. Favour a heading direction for a certain point. Specify either one heading for the start point or as
            many as there are points. In this case headings are associated by their order to the specific points. 
            Headings are given as north based clockwise angle between 0 and 360 degree. 
        :type heading: list of int   

        :param heading_penalty: Optional parameter. Penalty for omitting a specified heading. The penalty corresponds to the accepted time 
            delay in seconds in comparison to the route without a heading.
            Default 120.
        :type heading_penalty: int

        :param pass_through: Optional parameter. If true u-turns are avoided at via-points with regard to the heading_penalty.
            Default False.
        :type pass_through: bool

        :param block_area: Optional parameter. Block road access via a point with the format 
            latitude,longitude or an area defined by a circle lat,lon,radius or a rectangle lat1,lon1,lat2,lon2.
        :type block_area: str

        :param avoid: Optional semicolon separated parameter. Specify which road classes you would like to avoid 
            (currently only supported for motor vehicles like car). Possible values are ferry, motorway, toll, tunnel and ford.
        :type avoid: list of str
        
        :param algorithm: Optional parameter. round_trip or alternative_route.
        :type algorithm: str 

        :param round_trip_distance: If algorithm=round_trip this parameter configures approximative length of the resulting round trip.
            Default 10000.
        :type round_trip_distance: int

        :param round_trip_seed: If algorithm=round_trip this parameter introduces randomness if e.g. the first try wasn't good.
            Default 0.
        :type round_trip_seed: int

        :param alternative_route_max_paths: If algorithm=alternative_route this parameter sets the number of maximum paths
            which should be calculated. Increasing can lead to worse alternatives.
            Default 2.
        :type alternative_route_max_paths: int

        :param alternative_route_max_weight_factor: If algorithm=alternative_route this parameter sets the factor by which the alternatives
            routes can be longer than the optimal route. Increasing can lead to worse alternatives.
            Default 1.4.
        :type alternative_route_max_weight_factor: float

        :param alternative_route_max_share_factor: If algorithm=alternative_route this parameter specifies how much alternatives
            routes can have maximum in common with the optimal route. Increasing can lead to worse alternatives.
            Default 0.6.
        :type alternative_route_max_share_factor: float
       
        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        params = [
            ('profile', profile)
        ]

        for coordinate in coordinates:
            coord_latlng = reversed([convert._format_float(f) for f in coordinate])
            params.append(("point", ",".join(coord_latlng)))

        if self.key is not None:
            params.append(("key", self.key))

        if format is not None:
            params.append(("type", format))

        if optimize is not None:
            params.append(("optimize", convert._convert_bool(optimize)))

        if instructions is not None:
            params.append(("instructions", convert._convert_bool(instructions)))

        if locale is not None:
            params.append(("locale", locale))

        if elevation is not None:
            params.append(("elevation", convert._convert_bool(elevation)))

        if points_encoded is not None:
            params.append(("points_encoded", convert._convert_bool(points_encoded)))

        if calc_points is not None:
            params.append(("calc_points", convert._convert_bool(calc_points)))
    
        if debug is not None:
            params.append(("debug", convert._convert_bool(debug)))

        if point_hint is not None:
            params.append(("point_hint", convert._convert_bool(point_hint)))
        
        ### all below params will only work if ch is disabled
        
        if details is not None:
            params.extend([("details", detail) for detail in details])

        if ch_disable is not None:
            params.append(("ch.disable", convert._convert_bool(ch_disable)))

        if weighting is not None:
            params.append(("weighting", weighting))

        if heading is not None:
            params.append(("heading", convert._delimit_list(heading)))

        if heading_penalty is not None:
            params.append(("heading_penalty", heading_penalty))

        if pass_through is not None:
            params.append(("pass_through", convert._convert_bool(pass_through)))

        if block_area is not None:
            params.append(("block_area", block_area))

        if avoid is not None:
            params.append(("avoid", convert._delimit_list(avoid, ';')))
    
        if algorithm is not None:

            if algorithm == 'round_trip':

                if round_trip_distance is not None:
                    params.append(("round_trip.distance", round_trip_distance))

                if round_trip_seed is not None:
                    params.append(("round_trip.seed", round_trip_seed))

            if algorithm == 'alternative_route':

                if alternative_route_max_paths is not None:
                    params.append(("alternative_route.max_paths", alternative_route_max_paths))

                if alternative_route_max_weight_factor is not None:
                    params.append(("alternative_route.max_weight_factor", alternative_route_max_weight_factor))

        return self._request('/route', get_params=params, dry_run=dry_run)

    def isochrones(self, coordinates, profile, distance_limit=None, time_limit=None, 
                    buckets=None, reverse_flow=None, debug=None, dry_run=None):
        """Gets isochrones or equidistants for a range of time/distance values around a given set of coordinates.

        :param coordinates: One coordinate pair denoting the location.
        :type coordinates: tuple

        :param profile: Specifies the mode of transport. 
            One of bike, car, foot or 
            https://graphhopper.com/api/1/docs/supported-vehicle-profiles/Default.
            Default "car".
        :type profile: str

        :param distance_limit: Specify which time the vehicle should travel. In seconds.
            Default 600.
        :type distance_limit: int

        :param time_limit: Instead of time_limit you can also specify the distance 
            the vehicle should travel. In meter.
        :type time_limit: int

        :param buckets: For how many sub intervals an additional polygon should be calculated.
            Default 1.
        :type buckets: int
    
        :param reverse_flow: If false the flow goes from point to the polygon,
            if true the flow goes from the polygon "inside" to the point. 
            Default False.
        :param reverse_flow: bool
        
        :param debug: If true, the output will be formatted.
            Default False
        :type debug: bool
    
        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """

        params = [
            ('profile', profile)
        ]

        coord_latlng = reversed([convert._format_float(f) for f in coordinates])
        params.append(("point", ",".join(coord_latlng)))

        if self.key is not None:
            params.append(("key", self.key))

        if distance_limit is not None:
            params.append(('distance_limit', distance_limit))

        if time_limit is not None:
            params.append(('time_limit', time_limit))

        if buckets is not None:
            params.append(('buckets', buckets))

        if reverse_flow is not None:
            params.append(('reverse_flow', convert._convert_bool(reverse_flow)))

        if debug is not None:
            params.append(('debug', convert._convert_bool(debug)))

        return self._request("/isochrone", get_params=params, dry_run=dry_run)

    def distance_matrix(self, coordinates, profile, sources=None, destinations=None, out_array=None, debug=None, dry_run=None):
        """ Gets travel distance and time for a matrix of origins and destinations.

        :param coordinates: Specifiy multiple points for which the weight-, route-, time- or distance-matrix should be calculated. 
            In this case the starts are identical to the destinations. 
            If there are N points, then NxN entries will be calculated. 
            The order of the point parameter is important. Specify at least three points. 
            Cannot be used together with from_point or to_point. Is a string with the format latitude,longitude.
        :type coordinates: list, tuple

        :param profile: Specifies the mode of transport. 
            One of bike, car, foot or
            https://graphhopper.com/api/1/docs/supported-vehicle-profiles/Default.
            Default "car".
        :type profile: str

        :param sources: The starting points for the routes. 
            Specifies an index referring to coordinates.
        :type from_coordinates: list

        :param destinations: The destination points for the routes. Specifies an index referring to coordinates.
        :type to_coordinates: list

        :param out_array: Specifies which arrays should be included in the response. Specify one or more of the following 
            options 'weights', 'times', 'distances'.
            The units of the entries of distances are meters, of times are seconds and of weights is arbitrary and it can differ 
            for different vehicles or versions of this API.
            Default "weights".
        :type out_array: list           
    
        :param dry_run: Print URL and parameters without sending the request.
        :param dry_run: bool

        :returns: raw JSON response
        :rtype: dict
        """
        params = [
            ('profile', profile)
        ]

        if self.key is not None:
            params.append(("key", self.key))

        if sources is None and destinations is None:
            coordinates = (reversed([convert._format_float(f) for f in coord]) for coord in coordinates)
            params.extend([('point', ",".join(coord)) for coord in coordinates])

        else:
            sources_out = coordinates
            destinations_out = coordinates
            try:
                for idx in sources:
                    sources_out = []
                    sources_out.append(coordinates[idx])
            except IndexError:
                raise IndexError("Parameter sources out of coordinates range at index {}.".format(idx))
            except TypeError:
                # Raised when sources == None
                pass
            try:
                for idx in destinations:
                    destinations_out = []
                    destinations_out.append(coordinates[idx])
            except IndexError:
                raise IndexError("Parameter destinations out of coordinates range at index {}.".format(idx))
            except TypeError:
                # Raised when destinations == None
                pass

            sources_out = (reversed([convert._format_float(f) for f in coord]) for coord in sources_out)
            params.extend([("from_point", ",".join(coord)) for coord in sources_out])

            destinations_out = (reversed([convert._format_float(f) for f in coord]) for coord in destinations_out)
            params.extend([("to_point", ",".join(coord)) for coord in destinations_out])

        if out_array is not None:
            for e in out_array:
                params.append(("out_array", e))

        if debug is not None:
            params.append(('debug', convert._convert_bool(debug)))

        return self._request('/matrix', get_params=params, dry_run=dry_run)
