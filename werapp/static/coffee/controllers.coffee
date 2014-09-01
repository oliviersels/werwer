
werControllers = angular.module 'werControllers', ['werServices', 'werEventState', 'ngRoute', 'ui.bootstrap', 'djangoDynamics']

# Shuffle array in place
fisherYates = (arr) ->
    i = arr.length;
    if i == 0 then return false

    while --i
        j = Math.floor(Math.random() * (i+1))
        tempi = arr[i]
        tempj = arr[j]
        arr[i] = tempj
        arr[j] = tempi
    return arr

werControllers.controller 'NavbarController', ['$scope', '$location',
  ($scope, $location) ->
    $scope.isActive = (urls...) ->
      (new RegExp(url).test $location.path() for url in urls).some((x) -> x)
]

werControllers.controller 'HomeController', ['$scope', 'werApi', ($scope, werApi) ->
  werApi.Match.then (Match) ->
    $scope.previousMatches = Match.query()
]

werControllers.controller 'PlayerController', ['$scope', '$location', 'werApi', ($scope, $location, werApi) ->
  werApi.Player.then (Player) ->
    $scope.players = Player.query()

  $scope.editPlayer = (player) ->
    $location.path('/edit-player/' + player.id + '/')
]

werControllers.controller 'EditPlayerController', ['$scope',
                                                   '$location',
                                                   'werApi',
                                                   '$routeParams',
                                                   '$modal',
  ($scope, $location, werApi, $routeParams, $modal) ->
    werApi.Player.then (Player) ->
      Player.get({id: $routeParams.playerId}, (player, response) ->
        $scope.player = player
      , (response) ->
        $scope.player = null
        $scope.error = response.status
      )

    $scope.submit = () ->
      $scope.player.$update({}, (data) ->
        $location.path('/players/')
      )

    $scope.confirmDelete = () ->
      modal = $modal.open(
        templateUrl: "/partials/edit-player-confirm/",
        controller: 'EditPlayerConfirmController',
        resolve:
          player: () ->
            $scope.player
      )

      modal.result.then(
        () ->
          $scope.delete()
      )


    $scope.delete = () ->
      $scope.player.$delete({}, (data) ->
        $location.path('/players/')
      )
]

werControllers.controller 'EditPlayerConfirmController', ['$scope',
                                                          '$modalInstance',
                                                          'player',
  ($scope, $modalInstance, player) ->
    $scope.player = player

    $scope.delete = () ->
      $modalInstance.close()

    $scope.close = () ->
      $modalInstance.dismiss('cancel')
]

werControllers.controller 'AddPlayerController', ['$scope', 'werApi', '$location'
  ($scope, werApi, $location) ->
    werApi.Player.then (Player) ->
      $scope.player = new Player()

    $scope.submit = () ->
      $scope.player.username = $scope.player.first_name + '.' + $scope.player.last_name
      $scope.player.$save({}, () ->
        $location.path('/players/')
      )
]

werControllers.controller 'EventsOverviewController', ['$scope', '$location', 'werApi',
  ($scope, $location, werApi) ->
    werApi.Event.then (Event) ->
      $scope.events = Event.query()

    $scope.openEvent = (event) ->
      $location.path('/event/' + event.id + '/')
]

werControllers.controller 'NewEventController', ['$scope', '$filter', '$location', 'werApi', 'djangoEnums',
  ($scope, $filter, $location, werApi, djangoEnums) ->
    werApi.Event.then (Event) ->
      # Create a new event with sensible defaults
      $scope.event = new Event(
        event_type: 'casual_limited',
        pairing_method: 'swiss',
        date: new Date()
      )

    $scope.datepickerOpened = false

    $scope.openDatepicker = ($event) ->
      $event.preventDefault();
      $event.stopPropagation();
      $scope.datepickerOpened = true

    $scope.optionsEventType = djangoEnums.EventType
    $scope.optionsPairingMethod = djangoEnums.PairingMethod

    $scope.submit = () ->
      $scope.event.date = $filter('date')($scope.event.date, 'yyyy-MM-dd')
      $scope.event.$save({}, () ->
        $location.path('/event/' + $scope.event.id + '/')
      )
]

werControllers.controller 'EventController', ['$scope',
                                             '$location',
                                             '$routeParams'
                                             'werApi',
                                             'eventStateFactory'
  ($scope, $location, $routeParams, werApi, eventStateFactory) ->
    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        console.log event
        $scope.event = event
      , (response) ->
        $scope.event = null
        $scope.error = response.status
      )
]

werControllers.controller 'EventPlanningController', ['$scope',
                                                     '$location',
                                                     '$routeParams',
                                                     '$modal'
                                                     'werApi',
                                                     'eventStateFactory'
  ($scope, $location, $routeParams, $modal, werApi, eventStateFactory) ->
    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        $scope.event = event
      , (response) ->
        $scope.event = null
        $scope.error = response.status
      )

    werApi.Player.then (Player) ->
      $scope.availablePlayers = Player.query()


    $scope.addPlayer = (player, confirm) ->
      if $scope.event.state == 'planning' || confirm
        werApi.Participant.then (Participant) ->
          participant = new Participant(
            player: player.url
            event: $scope.event.url
          )
          participant.$save({}, () ->
            resourceParticipant = Participant.createResource(participant.toJSON())
            $scope.event.participant_set.push(resourceParticipant)
            player.participant_set.push(resourceParticipant)
          )
      else
        modal = $modal.open(
          templateUrl: "/partials/confirm-cancel-modal/",
          controller: 'ConfirmCancelModalController',
          resolve:
            title: () ->
              "Add player?"
            body: () ->
              "The event has already started. Are you sure you want to add player " + player.first_name + " " + player.last_name + "?"
        )

        modal.result.then(
          () ->
            $scope.addPlayer(player, true)
        )

    $scope.filterAdded = (player) ->
      !$scope.event || !$scope.event.$resolved || !(participant1.url in (participant2.url for participant2 in $scope.event.participant_set) for participant1 in player.participant_set).some((x) -> x)

    $scope.startEventConfirm = () ->
      modal = $modal.open(
        templateUrl: "/partials/start-event-confirm/",
        controller: 'StartEventConfirmController',
        resolve:
          event: () ->
            $scope.event
      )

      modal.result.then(
        (nr_of_rounds) ->
          $scope.event.nr_of_rounds = nr_of_rounds
          $scope.startEvent()
      )

    $scope.startEvent = () ->
      $scope.event.state = 'draft'
      postableEvent = $scope.event.postable()
      postableEvent.$update({}, (data) ->
        $location.path('/event/' + data.id + '/draft/')
      )
      return
]

werControllers.controller 'StartEventConfirmController', ['$scope',
                                                          '$modalInstance',
                                                          'event'
  ($scope, $modalInstance, event) ->
    $scope.event = event
    $scope.recommended_rounds = Math.max(3, Math.floor(Math.log(event.participant_set.length) / Math.log(2)))
    $scope.event.nr_of_rounds = $scope.recommended_rounds

    $scope.start = () ->
      $modalInstance.close($scope.event.nr_of_rounds)

    $scope.cancel = () ->
      $modalInstance.dismiss('cancel')
]

werControllers.controller 'EventDraftController', ['$scope',
                                                  '$location',
                                                  '$routeParams',
                                                  '$q',
                                                  '$modal'
                                                  'werApi',
                                                  'eventStateFactory'
  ($scope, $location, $routeParams, $q, $modal, werApi, eventStateFactory) ->
    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        $scope.event = event
      , (response) ->
        $scope.event = null
        $scope.error = response.status
      )

    $scope.seatingsRandom = (confirm) ->
      doSeatings = (participants) ->
          $scope.seatings = fisherYates((p.player for p in participants))

      if confirm || !$scope.seatings
        if 'then' of $scope.event.participant_set
          $scope.event.participant_set.then((participants) ->
            $q.all((p.player for p in participants)).then(() ->
              doSeatings(participants)
            )
          )
        else
          doSeatings($scope.event.participant_set)
      else
        modal = $modal.open(
          templateUrl: "/partials/confirm-cancel-modal/",
          controller: 'ConfirmCancelModalController',
          resolve:
            title: () ->
              "New seatings?"
            body: () ->
              "Seatings have already been generated. Are you sure you want to generate new seatings?"
        )

        modal.result.then(
          () ->
            $scope.seatingsRandom(true)
        )

    $scope.endDraft = () ->
      $scope.event.state = 'rounds'
      postableEvent = $scope.event.postable()
      postableEvent.$update({}, (data) ->
        # Create the first round
        if !$scope.event.round_set || $scope.event.round_set.length == 0
          werApi.Round.then((Round) ->
            newRound = new Round(
              event: $scope.event.url
            )
            newRound.$save({}, () ->
              $location.path('/event/' + data.id + '/round/1/')
            )
          )
        else
          $location.path('/event/' + data.id + '/round/1/')
      )
      return
]

werControllers.controller 'ConfirmCancelModalController', ['$scope',
                                                           '$modalInstance',
                                                           'title',
                                                           'body'
  ($scope, $modalInstance, title, body) ->
    $scope.title = title
    $scope.body = body

    $scope.confirm = () ->
      $modalInstance.close()

    $scope.cancel = () ->
      $modalInstance.dismiss('cancel')
]

werControllers.controller 'EventRoundController' , ['$scope',
                                                   '$location',
                                                   '$routeParams',
                                                   '$filter',
                                                   '$timeout',
                                                   'werApi',
                                                   'eventStateFactory',
                                                   'djangoEnums',
  ($scope, $location, $routeParams, $filter, $timeout, werApi, eventStateFactory, djangoEnums) ->
    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        $scope.event = event
        if 'then' of event.round_set
          event.round_set.then((rounds) ->
            $scope.round = rounds[parseInt($routeParams.roundId) - 1]
            $scope.round.roundNr = $routeParams.roundId
          )
        else
          $scope.round = event.round_set[parseInt($routeParams.roundId) - 1]
          $scope.round.roundNr = $routeParams.roundId
      , (response) ->
        $scope.error = response.status
      )

    $scope.createMatchesRandom = () ->
      # 1) Create the random creation request.
      # 2) Do polling to see when it is ready.
      # 3) Display the results
      werApi.RandomMatchesRequest.then (RandomMatchesRequest) ->
        randomMatchesRequest = new RandomMatchesRequest(
          round: $scope.round.url
        )
        randomMatchesRequest.$save({}, () ->
          checkResults = () ->
            RandomMatchesRequest.get({id: randomMatchesRequest.id}, (result) ->
              if result.state == 'completed'
                console.log 'done'
              else
                $timeout(checkResults, 1000)
            )
          checkResults()
        )

]
