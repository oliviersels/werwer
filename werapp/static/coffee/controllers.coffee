
werControllers = angular.module 'werControllers', ['werServices', 'ngRoute', 'ui.bootstrap', 'djangoDynamics']

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
                                             'werApi',
                                             '$routeParams'
  ($scope, $location, werApi, $routeParams) ->
    werApi.Game.then (Game) ->
      Game.get({id: $routeParams.gameId}, (game, response) ->
        $scope.game = game
      , (response) ->
        $scope.game = null
        $scope.error = response.status
      )
]

werControllers.controller 'GamePlanningController', ['$scope',
                                                     '$location',
                                                     'werApi',
                                                     '$routeParams'
  ($scope, $location, werApi, $routeParams) ->
    getGame = () ->
      werApi.Game.then (Game) ->
        Game.get({id: $routeParams.gameId}, (game, response) ->
          $scope.game = game
          console.log game
        , (response) ->
          $scope.game = null
          $scope.error = response.status
        )

    getAvailablePlayers = () ->
      werApi.Player.then (Player) ->
        $scope.availablePlayers = Player.query()

    getGame()
    getAvailablePlayers()


    $scope.addPlayer = (player) ->
      werApi.GamePlayer.then (GamePlayer) ->
        gamePlayer = new GamePlayer(
          player: player.url
          magicgame: $scope.game.url
        )
        gamePlayer.$save({}, () ->
          getGame()
          getAvailablePlayers()
        )

    $scope.filterAdded = (player) ->
      !$scope.game || !$scope.game.$resolved || !(gameplayer1 in $scope.game.gameplayer_set for gameplayer1 in player.gameplayer_set).some((x) -> x)
]
