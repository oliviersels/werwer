
werControllers = angular.module 'werControllers', ['werServices', 'ngRoute', 'ui.bootstrap']


werControllers.controller 'HomeController', ['$scope', ($scope) ->
#  $scope.players = Player.query()
#
#  # Some fun with updating an instance
#  admin = Player.get(id: 1, ->
#    admin.first_name = 'Olivier'
#    admin.last_name = 'Sels'
#    admin.$update()
#  )
#
#  # Some fun with creating a new player
#  newPlayer = new Player(
#    first_name: 'Olivier',
#    last_name: 'Sels',
#    email: 'test@mail.com',
#    username: 'test'
#  )
#  newPlayer.$save()
  $scope.welcome = 'Welcome!'
]

werControllers.controller 'PlayerController', ['$scope', '$location', 'werApi', ($scope, $location, werApi) ->
  werApi.Player.then (Player) ->
    $scope.players = Player.query()
    $scope.$watchCollection(player, (newPlayer) ->
      newPlayer.$update()
    ) for player in $scope.players

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
