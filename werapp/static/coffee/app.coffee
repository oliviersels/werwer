
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
    .when '/new-game/',
      templateUrl: '/partials/new-game/',
      controller: 'NewGameController'
    .otherwise
      redirectTo: '/'
  $locationProvider.html5Mode(true)
]
