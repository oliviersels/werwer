
werApp = angular.module 'werApp', ['ngRoute', 'ngResource', 'werControllers', 'djangoDynamics']

werApp.config ['$resourceProvider', ($resourceProvider) ->
  $resourceProvider.defaults.stripTrailingSlashes = false
]

werApp.run ["$rootScope", "$location", "$http", "authService", ($rootScope, $location, $http, authService) ->
  $rootScope.$on("$routeChangeError", (event, current, previous, eventResult) ->
    if eventResult.authenticated == false
      $location.path('/login/')
  )
]

loginRequired = {
  auth: ["$q", "authService", "$location", "$route", ($q, authService, $location, $route) ->
    token = authService.getToken()

    if token
      return $q.when(token)
    else
      return $q.reject(authenticated: false)
  ]
}

werApp.config ['$routeProvider', '$locationProvider', 'werwer_root', 'partials_root', ($routeProvider, $locationProvider, werwer_root, partials_root) ->
  $routeProvider
    .when werwer_root,
      templateUrl: partials_root + 'home/',
      controller: 'HomeController',
      resolve: loginRequired
    .when werwer_root + 'players/',
      templateUrl: partials_root + 'players/',
      controller: 'PlayerController'
      resolve: loginRequired
    .when werwer_root + 'edit-player/:playerId/',
      templateUrl: partials_root + 'edit-player/',
      controller: 'EditPlayerController'
      resolve: loginRequired
    .when werwer_root + 'add-player/',
      templateUrl: partials_root + 'add-player/',
      controller: 'AddPlayerController'
      resolve: loginRequired
    .when werwer_root + 'events-overview/',
      templateUrl: partials_root + 'events-overview/',
      controller: 'EventsOverviewController'
      resolve: loginRequired
    .when werwer_root + 'new-event/',
      templateUrl: partials_root + 'new-event/',
      controller: 'NewEventController'
      resolve: loginRequired
    .when werwer_root + 'event/:eventId/',
      templateUrl: partials_root + 'event/',
      controller: 'EventController'
      resolve: loginRequired
    .when werwer_root + 'event/:eventId/planning/',
      templateUrl: partials_root + 'event-planning/',
      controller: 'EventPlanningController'
      resolve: loginRequired
    .when werwer_root + 'event/:eventId/draft/',
      templateUrl: partials_root + 'event-draft/',
      controller: 'EventDraftController'
      resolve: loginRequired
    .when werwer_root + 'event/:eventId/round/:roundId/',
      templateUrl: partials_root + 'event-round/',
      controller: 'EventRoundController'
      resolve: loginRequired
    .when werwer_root + 'event/:eventId/standings/',
      templateUrl: partials_root + 'event-standings/',
      controller: 'EventStandingsController'
      resolve: loginRequired
    .when werwer_root + 'event/:eventId/conclusion/',
      templateUrl: partials_root + 'event-conclusion/',
      controller: 'EventConclusionController'
      resolve: loginRequired
    .when werwer_root + 'login/',
      controller: 'LoginController',
      template: ''
    .otherwise
      redirectTo: werwer_root
  $locationProvider.html5Mode(true)
]
