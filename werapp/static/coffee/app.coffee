
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
    .otherwise
      redirectTo: '/'
  $locationProvider.html5Mode(true)
]
