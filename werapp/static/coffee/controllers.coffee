
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

werControllers.controller 'PlayerController', ['$scope', '$location', 'werApi', 'werwer_root', ($scope, $location, werApi, werwer_root) ->
  werApi.Player.then (Player) ->
    $scope.players = Player.query()

  $scope.editPlayer = (player) ->
    $location.path(werwer_root + 'edit-player/' + player.id + '/')
]

werControllers.controller 'EditPlayerController', ['$scope',
                                                   '$location',
                                                   'werApi',
                                                   'werwer_root',
                                                   'partials_root',
                                                   '$routeParams',
                                                   '$modal',
  ($scope, $location, werApi, werwer_root, partials_root, $routeParams, $modal) ->
    werApi.Player.then (Player) ->
      Player.get({id: $routeParams.playerId}, (player, response) ->
        $scope.player = player
      , (response) ->
        $scope.player = null
        $scope.error = response.status
      )

    $scope.submit = () ->
      $scope.player.$update({}, (data) ->
        $location.path(werwer_root + 'players/')
      )

    $scope.confirmDelete = () ->
      modal = $modal.open(
        templateUrl: partials_root + "edit-player-confirm/",
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
        $location.path(werwer_root + 'players/')
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

werControllers.controller 'AddPlayerController', ['$scope', 'werApi', 'werwer_root', '$location'
  ($scope, werApi, werwer_root, $location) ->
    werApi.Player.then (Player) ->
      $scope.player = new Player()

    $scope.submit = () ->
      $scope.player.username = $scope.player.first_name + '.' + $scope.player.last_name
      $scope.player.$save({}, () ->
        $location.path(werwer_root + 'players/')
      )
]

werControllers.controller 'EventsOverviewController', ['$scope', '$location', 'werApi', 'werwer_root'
  ($scope, $location, werApi, werwer_root) ->
    werApi.Player.then (Player) ->
      Player.get({id: 'me'}, (me) ->
        me.event_set.then (events) ->
          $scope.events = events
      )

    $scope.openEvent = (event) ->
      $location.path(werwer_root + 'event/' + event.id + '/')
]

werControllers.controller 'NewEventController', ['$scope', '$filter', '$location', 'werApi', 'djangoEnums', 'werwer_root'
  ($scope, $filter, $location, werApi, djangoEnums, werwer_root) ->
    werApi.Event.then (Event) ->
      # Create a new event with sensible defaults
      $scope.event = new Event(
        event_type: 'casual_limited',
        pairing_method: 'swiss',
        date: new Date(),
        price_support: 2.5,
        price_support_min_points: 3
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
        $location.path(werwer_root + 'event/' + $scope.event.id + '/')
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
                                                     'werwer_root',
                                                     'partials_root',
                                                     'eventStateFactory'
  ($scope, $location, $routeParams, $modal, werApi, werwer_root, partials_root, eventStateFactory) ->
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
            $scope.event.participant_set__v.push(resourceParticipant)
            player.participant_set__v.push(resourceParticipant)
          )
      else
        modal = $modal.open(
          templateUrl: partials_root + "confirm-cancel-modal/",
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
      if !$scope.event
        return true
      return !(participant1.url in (participant2.url for participant2 in $scope.event.participant_set__v) for participant1 in player.participant_set__v).some((x) -> x)

    $scope.startEventConfirm = () ->
      modal = $modal.open(
        templateUrl: partials_root + "start-event-confirm/",
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
        $location.path(werwer_root + 'event/' + data.id + '/draft/')
      )
      return
]

werControllers.controller 'StartEventConfirmController', ['$scope',
                                                          '$modalInstance',
                                                          'event'
  ($scope, $modalInstance, event) ->
    $scope.event = event
    event.participant_set.then (participants) ->
      $scope.recommended_rounds = Math.max(3, Math.floor(Math.log(participants.length) / Math.log(2)))
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
                                                  'eventStateFactory',
                                                  'werwer_root',
                                                  'partials_root',
  ($scope, $location, $routeParams, $q, $modal, werApi, eventStateFactory, werwer_root, partials_root) ->
    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        $scope.event = event
      , (response) ->
        $scope.event = null
        $scope.error = response.status
      )

    $scope.seatingsRandom = (confirm) ->
      if confirm || !$scope.seatings
        $scope.event.participant_set.then((participants) ->
          $q.all((p.player for p in participants)).then(() ->
            $scope.seatings = fisherYates((p.player__v for p in participants))
          )
        )
      else
        modal = $modal.open(
          templateUrl: partials_root + "confirm-cancel-modal/",
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
        $scope.event.round_set.then (rounds) ->
          if rounds.length == 0
            werApi.Round.then((Round) ->
              newRound = new Round(
                event: $scope.event.url
              )
              newRound.$save({}, () ->
                $location.path(werwer_root + 'event/' + data.id + '/round/1/')
              )
            )
          else
            $location.path(werwer_root + 'event/' + data.id + '/round/1/')
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
                                                   'werwer_root',
  ($scope, $location, $routeParams, $filter, $timeout, werApi, eventStateFactory, djangoEnums, werwer_root) ->
    $scope.selectedMatch = null
    $scope.done = false
    $scope.lastRound = false

    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        $scope.event = event
        event.round_set.then((rounds) ->
          $scope.round = rounds[parseInt($routeParams.roundId) - 1]
          $scope.round.roundNr = $routeParams.roundId
          if parseInt($scope.round.roundNr) == $scope.event.nr_of_rounds
            $scope.lastRound = true
          $scope.round.match_set.then (matches) ->
            $scope.done = true
            for match in matches
              match.done = match.bye || match.wins != 0 || match.losses != 0 or match.draws != 0
              if !match.done
                $scope.done = false
        )
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
                $scope.round.$get(() ->
                  $scope.round.roundNr = $routeParams.roundId
                  $scope.round.match_set.then (matches) ->
                    $scope.done = true
                    for match in matches
                      match.done = match.bye || match.wins != 0 || match.losses != 0 or match.draws != 0
                      if !match.done
                        $scope.done = false
                )
              else
                $timeout(checkResults, 1000)
            )
          checkResults()
        )

    $scope.updateScore = (matchNr, wins, losses, draws) ->
      $scope.round.match_set.then (matches) ->
        match = matches[matchNr]
        match.wins = wins ? 0
        match.losses = losses ? 0
        match.draws = draws ? 0
        matchPostable = match.postable()
        matchPostable.$update();

        match.done = true
        for match in $scope.round.match_set__v
          if !match.done
            return

        $scope.done = true

    $scope.nextRound = () ->
      # If the round exists, just move to it
      $scope.event.round_set.then (rounds) ->
        roundNr = parseInt($scope.round.roundNr)
        if rounds.length > roundNr
          $location.path(werwer_root + 'event/' + $scope.event.id + '/round/' + (roundNr + 1) + '/')
        else
          werApi.Round.then((Round) ->
            newRound = new Round(
              event: $scope.event.url
            )
            newRound.$save({}, () ->
              $location.path(werwer_root + 'event/' + $scope.event.id + '/round/' + (roundNr + 1) + '/')
            )
          )

    $scope.endEvent = () ->
      $scope.event.state = 'conclusion'
      postableEvent = $scope.event.postable()
      postableEvent.$update({}, (data) ->
        $location.path(werwer_root + 'event/' + $scope.event.id + '/conclusion/')
      )
]

werControllers.controller 'EventStandingsController' , ['$scope',
                                                        '$location',
                                                        '$routeParams',
                                                        'werApi',
                                                        'eventStateFactory',
                                                        'djangoEnums',
  ($scope, $location, $routeParams, werApi, eventStateFactory, djangoEnums) ->
    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        $scope.event = event
      )
]

werControllers.controller 'EventConclusionController' , ['$scope',
                                                         '$location',
                                                         '$routeParams',
                                                         'werApi',
                                                         'eventStateFactory',
                                                         'djangoEnums',
  ($scope, $location, $routeParams, werApi, eventStateFactory, djangoEnums) ->
    werApi.Event.then (Event) ->
      Event.get({id: $routeParams.eventId}, (event, response) ->
        event.eventState = eventStateFactory.createEventState(event)
        $scope.event = event
      )

    $scope.endOfEventMailing = () ->
      werApi.EndOfEventMailingRequest.then (EndOfEventMailingRequest) ->
        endOfEventMailingRequest = new EndOfEventMailingRequest(
          event: $scope.event.url
        )
        endOfEventMailingRequest.$save({})
]

werControllers.controller 'LoginController', ['$scope',
                                              '$location',
                                              '$window',
                                              'authService',
                                              'werwer_root',
  ($scope, $location, $window, authService, werwer_root) ->
    hash = $location.hash()
    if hash == ''
      $window.location.href = authService.getAuthUrl()
    else
      authService.parseOauthResult(hash)
      $location.path(werwer_root)
]
