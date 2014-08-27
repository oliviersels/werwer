
werApp = angular.module 'werApp', ['ngRoute', 'ngResource', 'werControllers']

werApp.config ['$resourceProvider', ($resourceProvider) ->
  $resourceProvider.defaults.stripTrailingSlashes = false
]

werApp.config ['$routeProvider', '$locationProvider', ($routeProvider, $locationProvider) ->
  $routeProvider
    .when '/',
      templateUrl: '/partials/home/',
      controller: 'HomeController'
    .when '/players/',
      templateUrl: '/partials/players/',
      controller: 'PlayerController'
    .when '/edit-player/:playerId/',
      templateUrl: '/partials/edit-player/',
      controller: 'EditPlayerController'
    .when '/add-player/',
      templateUrl: '/partials/add-player/',
      controller: 'AddPlayerController'
    .when '/games-overview/',
      templateUrl: '/partials/games-overview/',
      controller: 'GamesOverviewController'
    .when '/new-game/',
      templateUrl: '/partials/new-game/',
      controller: 'NewGameController'
    .when '/game/:gameId/',
      templateUrl: '/partials/game/',
      controller: 'GameController'
    .when '/game/:gameId/planning/',
      templateUrl: '/partials/game-planning/',
      controller: 'GamePlanningController'
    .when '/game/:gameId/draft/',
      templateUrl: '/partials/game-draft/',
      controller: 'GameDraftController'
    .when '/game/:gameId/round/:roundId/',
      templateUrl: '/partials/game-round/',
      controller: 'GameRoundController'

    .otherwise
      redirectTo: '/'
  $locationProvider.html5Mode(true)
]
