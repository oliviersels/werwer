
werControllers = angular.module 'werControllers', ['werServices']


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

werControllers.controller 'PlayerController', ['$scope', 'werApi', ($scope, werApi) ->
  werApi.Player.then (Player) ->
    $scope.players = Player.query()
    $scope.admin = Player.get(id: 1)
  werApi.Game.then (Game) ->
    $scope.games = Game.query()
  #$scope.players = Player.query()
#  $scope.players = ['a', 'b']
]
