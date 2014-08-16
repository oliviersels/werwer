
werControllers = angular.module 'werControllers', ['werServices', 'ngRoute']


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
  ($scope, $location, werApi, $routeParams) ->
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
]

#    $scope.admin = Player.get(id: 1)
#  werApi.Game.then (Game) ->
#    $scope.games = Game.query()
  #$scope.players = Player.query()
#  $scope.players = ['a', 'b']
