werServices = angular.module 'werServices', ['ngResource']

werServices.factory 'werApi', ['$q', '$http', '$resource', ($q, $http, $resource) ->
  createService = (serviceName, serviceUrl, linkedResources) ->
    _convertDate = (obj, key) ->
      value = Date.parse(obj[key])
      obj[key] = new Date(value) if !isNaN(value)

    searchAndconvertDates = (obj) ->
#      console.log(obj)
      _convertDate(obj, key) for key of obj when obj.hasOwnProperty(key) && toString.call(obj[key]) == '[object String]'

    createLazyProperty = (oldValue, options, value) ->
      () ->
        if !value
          if options.isArray
            value = $q.all(($http.get(res) for res in oldValue)).then((results) ->
              if options.resource
                options.resource.then((Resource) ->
                  value = (new Resource(result.data) for result in results)
                )
              else
                value = (result.data for result in results)

            )
          else
            value = $http.get(oldValue).success((data) ->
              if options.resource
                options.resource.then((Resource) ->
                  value = new Resource(data)
                )
              else
                value = data
            )
        else
          value

    convertLinkedResources = (obj, linkedResources) ->
      for resourceName, options of linkedResources
        # Create a getter for the resources
        Object.defineProperty(obj, resourceName,
          get: createLazyProperty(obj[resourceName], options)
          enumerable: true

        )

    convertResponse = (linkedResources, isArray) ->
      (response) ->
        convertObj = (obj) ->
          searchAndconvertDates(obj)
          convertLinkedResources(obj, linkedResources)

        if isArray
          convertObj(obj) for obj in response.resource
        else
          convertObj(response.resource)
        response.resource

    $resource serviceUrl + ':id/', id: "@id", {
      update:
        method: 'PUT'
      query:
        method: 'GET'
        isArray: true
        interceptor:
          response: convertResponse(linkedResources, true)
      get:
        method: 'GET'
        interceptor:
          response: convertResponse(linkedResources, false)
    }

  createResource = (resourceName, linkedResources) ->
    deferred = $q.defer()

    $http
      method: 'GET'
      url: '/api/',
      cache: true
    .success (data) ->
      deferred.resolve(createService resourceName, data[resourceName], linkedResources)
    .error (data) ->
      deferred.reject("Error retrieving API endpoint: " + data)

    deferred.promise

  # Create the resources
  GamePlayer = createResource('game-players', {})

  Player: createResource('players',
    gameplayer_set:
      isArray: true
      resource: GamePlayer
  )
  Game: createResource('games',
    gameplayer_set:
      isArray: true
      resource: GamePlayer
  )
  Match: createResource('matches', {})
  GamePlayer: GamePlayer
]
