
werControllers = angular.module 'werControllers', ['werServices', 'werGameState', 'ngRoute', 'ui.bootstrap', 'djangoDynamics']

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

werControllers.controller 'GamesOverviewController', ['$scope', '$location', 'werApi',
  ($scope, $location, werApi) ->
    werApi.Game.then (Game) ->
      $scope.games = Game.query()

    $scope.openGame = (game) ->
      $location.path('/game/' + game.id + '/')
]

werControllers.controller 'NewGameController', ['$scope', '$filter', '$location', 'werApi', 'djangoEnums',
  ($scope, $filter, $location, werApi, djangoEnums) ->
    werApi.Game.then (Game) ->
      # Create a new game with sensible defaults
      $scope.game = new Game(
        game_type: 'casual_limited',
        pairing_method: 'swiss',
        date: new Date()
      )

    $scope.datepickerOpened = false

    $scope.openDatepicker = ($event) ->
      $event.preventDefault();
      $event.stopPropagation();
      $scope.datepickerOpened = true

    $scope.optionsGameType = djangoEnums.GameType
    $scope.optionsPairingMethod = djangoEnums.PairingMethod

    $scope.submit = () ->
      $scope.game.date = $filter('date')($scope.game.date, 'yyyy-MM-dd')
      $scope.game.$save({}, () ->
        $location.path('/game/' + $scope.game.id + '/')
      )
]

werControllers.controller 'GameController', ['$scope',
                                             '$location',
                                             '$routeParams'
                                             'werApi',
                                             'gameStateFactory'
  ($scope, $location, $routeParams, werApi, gameStateFactory) ->
    werApi.Game.then (Game) ->
      Game.get({id: $routeParams.gameId}, (game, response) ->
        game.gameState = gameStateFactory.createGameState(game)
        console.log game
        $scope.game = game
      , (response) ->
        $scope.game = null
        $scope.error = response.status
      )
]

werControllers.controller 'GamePlanningController', ['$scope',
                                                     '$location',
                                                     '$routeParams',
                                                     '$modal'
                                                     'werApi',
                                                     'gameStateFactory'
  ($scope, $location, $routeParams, $modal, werApi, gameStateFactory) ->
    werApi.Game.then (Game) ->
      Game.get({id: $routeParams.gameId}, (game, response) ->
        game.gameState = gameStateFactory.createGameState(game)
        $scope.game = game
      , (response) ->
        $scope.game = null
        $scope.error = response.status
      )

    werApi.Player.then (Player) ->
      $scope.availablePlayers = Player.query()


    $scope.addPlayer = (player, confirm) ->
      if $scope.game.state == 'planning' || confirm
        werApi.GamePlayer.then (GamePlayer) ->
          gamePlayer = new GamePlayer(
            player: player.url
            magicgame: $scope.game.url
          )
          gamePlayer.$save({}, () ->
            resourceGamePlayer = GamePlayer.createResource(gamePlayer.toJSON())
            $scope.game.gameplayer_set.push(resourceGamePlayer)
            player.gameplayer_set.push(resourceGamePlayer)
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
      !$scope.game || !$scope.game.$resolved || !(gameplayer1.url in (gameplayer2.url for gameplayer2 in $scope.game.gameplayer_set) for gameplayer1 in player.gameplayer_set).some((x) -> x)

    $scope.startEventConfirm = () ->
      modal = $modal.open(
        templateUrl: "/partials/start-event-confirm/",
        controller: 'StartEventConfirmController',
        resolve:
          game: () ->
            $scope.game
      )

      modal.result.then(
        (nr_of_rounds) ->
          $scope.game.nr_of_rounds = nr_of_rounds
          $scope.startEvent()
      )

    $scope.startEvent = () ->
      $scope.game.state = 'draft'
      postableGame = $scope.game.postable()
      postableGame.$update({}, (data) ->
        $location.path('/game/' + data.id + '/draft/')
      )
      return
]

werControllers.controller 'StartEventConfirmController', ['$scope',
                                                          '$modalInstance',
                                                          'game'
  ($scope, $modalInstance, game) ->
    $scope.game = game
    $scope.recommended_rounds = Math.max(3, Math.floor(Math.log(game.gameplayer_set.length) / Math.log(2)))
    $scope.game.nr_of_rounds = $scope.recommended_rounds

    $scope.start = () ->
      $modalInstance.close($scope.game.nr_of_rounds)

    $scope.cancel = () ->
      $modalInstance.dismiss('cancel')
]

werControllers.controller 'GameDraftController', ['$scope',
                                                  '$location',
                                                  '$routeParams',
                                                  '$q',
                                                  '$modal'
                                                  'werApi',
                                                  'gameStateFactory'
  ($scope, $location, $routeParams, $q, $modal, werApi, gameStateFactory) ->
    werApi.Game.then (Game) ->
      Game.get({id: $routeParams.gameId}, (game, response) ->
        game.gameState = gameStateFactory.createGameState(game)
        $scope.game = game
      , (response) ->
        $scope.game = null
        $scope.error = response.status
      )

    $scope.seatingsRandom = (confirm) ->
      doSeatings = (gameplayers) ->
          $scope.seatings = fisherYates((gp.player for gp in gameplayers))

      if confirm || !$scope.seatings
        if 'then' of $scope.game.gameplayer_set
          $scope.game.gameplayer_set.then((gameplayers) ->
            $q.all((gp.player for gp in gameplayers)).then(() ->
              doSeatings(gameplayers)
            )
          )
        else
          doSeatings($scope.game.gameplayer_set)
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
      $scope.game.state = 'rounds'
      postableGame = $scope.game.postable()
      postableGame.$update({}, (data) ->
        # Create the first round
        if !$scope.game.gameround_set || $scope.game.gameround_set.length == 0
          werApi.Round.then((Round) ->
            newRound = new Round(
              game: $scope.game.url
            )
            newRound.$save({}, () ->
              $location.path('/game/' + data.id + '/round/1/')
            )
          )
        else
          $location.path('/game/' + data.id + '/round/1/')
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

werControllers.controller 'GameRoundController' , ['$scope',
                                                   '$location',
                                                   '$routeParams',
                                                   'werApi',
                                                   'gameStateFactory',
  ($scope, $location, $routeParams, werApi, gameStateFactory) ->
    werApi.Game.then (Game) ->
      Game.get({id: $routeParams.gameId}, (game, response) ->
        game.gameState = gameStateFactory.createGameState(game)
        $scope.game = game
        if 'then' of game.gameround_set
          game.gameround_set.then((gamerounds) ->
            $scope.round = gamerounds[parseInt($routeParams.roundId) - 1]
            $scope.round.roundNr = $routeParams.roundId
          )
        else
          $scope.round = game.gameround_set[parseInt($routeParams.roundId) - 1]
          $scope.round.roundNr = $routeParams.roundId
      , (response) ->
        $scope.error = response.status
      )
]
