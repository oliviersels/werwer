
werApp = angular.module 'werApp', ['ngRoute', 'ngResource', 'werControllers']

werApp.config ['$resourceProvider', ($resourceProvider) ->
  $resourceProvider.defaults.stripTrailingSlashes = false
]

werApp.config ['$routeProvider', ($routeProvider) ->
  $routeProvider
    .when '/',
      templateUrl: '/partials/home/',
      controller: 'HomeController'
    .when '/players/',
      templateUrl: '/partials/players/',
      controller: 'PlayerController'
    .otherwise
      redirectTo: '/'
]
