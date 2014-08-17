
werControllers = angular.module 'werControllers', ['werServices', 'ngRoute', 'ui.bootstrap', 'djangoDynamics']


werControllers.controller 'HomeController', ['$scope', ($scope) ->
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

werControllers.controller 'NewGameController', ['$scope', '$filter', 'werApi', 'djangoEnums',
  ($scope, $filter, werApi, djangoEnums) ->
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
      console.log $scope.game
      $scope.game.date = $filter('date')($scope.game.date, 'yyyy-MM-dd')
      $scope.game.$save()
]
