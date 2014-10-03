werServices = angular.module 'werServices', ['ngResource']

werServices.factory 'werApi', ['$q', '$http', '$resource', '$filter', ($q, $http, $resource, $filter) ->
  resourceCache = {}

  class LazyPropertyResult
    constructor: (@oldValue, @options) ->
      @value = null
      @promise = null

    hasResult: () ->
      return @value != null or @promise != null

    getPromise: () ->
      if !@hasResult()
        @retrieveValue()
        @promise.then (value) =>
          @value = value
      return @promise

    setPromise: (promise) ->
      @promise = promise
      promise.then (data) ->
        @value = data

    getValue: () ->
      if !@hasResult()
        @retrieveValue()
        @promise.then (value) =>
          @value = value
      return @value

    retrieveValue: () ->
      deferred = $q.defer()
      if @options.isArray
        $q.all(($http.get(res) for res in @oldValue)).then((results) =>
          if @options.resource
            resourceCache[@options.resource].then((Resource) ->
              deferred.resolve((Resource.createResource(result.data) for result in results))
            )
          else
            deferred.resolve((result.data for result in results))

        )
      else
        $http.get(@oldValue).success((data) =>
          if @options.resource
            resourceCache[@options.resource].then((Resource) ->
              deferred.resolve(Resource.createResource(data))
            )
          else
            deferred.resolve(data)
        )
      @setPromise(deferred.promise)

  createService = (serviceName, serviceUrl, linkedResources, postableHandler) ->
    _convertDate = (obj, key) ->
      value = Date.parse(obj[key])
      obj[key] = new Date(value) if !isNaN(value)

    searchAndconvertDates = (obj) ->
#      console.log(obj)
      _convertDate(obj, key) for key of obj when obj.hasOwnProperty(key) && toString.call(obj[key]) == '[object String]'

    createLazyProperty = (lazyPropertyResult) ->
      () ->
        lazyPropertyResult.getPromise()

    createLazyPropertyValues = (lazyPropertyResult) ->
      () ->
        return lazyPropertyResult.getValue()

    convertLinkedResources = (obj, linkedResources) ->
      for resourceName, options of linkedResources
        lazyPropertyResult = new LazyPropertyResult(obj[resourceName], options)
        # Create a getter for the resources
        Object.defineProperty(obj, resourceName,
          get: createLazyProperty(lazyPropertyResult)
          enumerable: false
          configurable: true
          set: (value) ->
            delete obj[resourceName]
            obj[resourceName] = value
        )

        # Create a getter for the resource values
        Object.defineProperty(obj, resourceName + '__v',
          enumerable: false
          configurable: true
          get: createLazyPropertyValues(lazyPropertyResult)
          set: (value) ->
            delete obj[resourceName]
            obj[resourceName] = value
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

    resourceClass = $resource serviceUrl + ':id/', id: "@id", {
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

    resourceClass.createResource = (args) ->
      resource = new this(args)
      convertLinkedResources(resource, linkedResources)
      resource

    resourceClass.prototype['postable'] = () ->
      result = {}
      for prop, value of this.toJSON()
        if not (prop of linkedResources)
          result[prop] = if postableHandler then postableHandler(prop, value) else value
        else if linkedResources[prop].isArray
          result[prop] = (p.url for p in value)
        else
          result[prop] = value.url
      new resourceClass(result)

    resourceClass

  createResource = (resourceName, linkedResources, postableHandler) ->
    deferred = $q.defer()

    $http
      method: 'GET'
      url: '/api/',
      cache: true
    .success (data) ->
      deferred.resolve(createService resourceName, data[resourceName], linkedResources, postableHandler)
    .error (data) ->
      deferred.reject("Error retrieving API endpoint: " + data)

    deferred.promise

  # Create the resources
  resourceCache.Participant = createResource('participants',
    player:
      isArray: false
      resource: "Player"
    event:
      isArray: false
      resource: "Event"
  )

  resourceCache.Player = createResource('players',
    participant_set:
      isArray: true
      resource: "Participant"
  )
  resourceCache.Event = createResource('events',
    participant_set:
      isArray: true
      resource: "Participant"
    round_set:
      isArray: true
      resource: "Round",
    (prop, value) ->
      if prop == 'date'
        $filter('date')(value, 'yyyy-MM-dd')
      else if prop == 'eventState'
        undefined
      else
        value
  )
  resourceCache.Match = createResource('matches',
    round:
      isArray: false
      resource: "Round"
    participant_set:
      isArray: true
      resource: "Participant"
  )
  resourceCache.Round = createResource('rounds',
    event:
      isArray: false
      resource: "Event"
    match_set:
      isArray: true
      resource: "Match"
  )

  resourceCache.RandomMatchesRequest = createResource('random-matches-request',
    round:
      isArray: false
      resource: "Round"
  )

  resourceCache
]

