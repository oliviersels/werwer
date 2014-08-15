werServices = angular.module 'werServices', ['ngResource']

werServices.factory 'werApi', ['$q', '$http', '$resource', ($q, $http, $resource) ->
  createService = (serviceName, serviceUrl) ->
    $resource serviceUrl + ':id/', id: "@id", {
      update:
        method: 'PUT'
    }

  createResource = (resourceName) ->
    deferred = $q.defer()

    $http
      method: 'GET'
      url: '/api/',
      cache: true
    .success (data) ->
      deferred.resolve(createService resourceName, data[resourceName])
    .error (data) ->
      deferred.reject("Error retrieving API endpoint: " + data)

    deferred.promise

  Player: createResource 'players'
  Game: createResource 'games'
  Match: createResource 'matches'
]
