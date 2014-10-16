
werApp = angular.module 'werApp', ['ngRoute', 'ngResource', 'werControllers']

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

werApp.config ['$routeProvider', '$locationProvider', ($routeProvider, $locationProvider) ->
  $routeProvider
    .when '/',
      templateUrl: '/partials/home/',
      controller: 'HomeController',
      resolve: loginRequired
    .when '/players/',
      templateUrl: '/partials/players/',
      controller: 'PlayerController'
      resolve: loginRequired
    .when '/edit-player/:playerId/',
      templateUrl: '/partials/edit-player/',
      controller: 'EditPlayerController'
      resolve: loginRequired
    .when '/add-player/',
      templateUrl: '/partials/add-player/',
      controller: 'AddPlayerController'
      resolve: loginRequired
    .when '/events-overview/',
      templateUrl: '/partials/events-overview/',
      controller: 'EventsOverviewController'
      resolve: loginRequired
    .when '/new-event/',
      templateUrl: '/partials/new-event/',
      controller: 'NewEventController'
      resolve: loginRequired
    .when '/event/:eventId/',
      templateUrl: '/partials/event/',
      controller: 'EventController'
      resolve: loginRequired
    .when '/event/:eventId/planning/',
      templateUrl: '/partials/event-planning/',
      controller: 'EventPlanningController'
      resolve: loginRequired
    .when '/event/:eventId/draft/',
      templateUrl: '/partials/event-draft/',
      controller: 'EventDraftController'
      resolve: loginRequired
    .when '/event/:eventId/round/:roundId/',
      templateUrl: '/partials/event-round/',
      controller: 'EventRoundController'
      resolve: loginRequired
    .when '/event/:eventId/standings/',
      templateUrl: '/partials/event-standings/',
      controller: 'EventStandingsController'
      resolve: loginRequired
    .when '/event/:eventId/conclusion/',
      templateUrl: '/partials/event-conclusion/',
      controller: 'EventConclusionController'
      resolve: loginRequired
    .when '/login/',
      controller: 'LoginController',
      template: ''
    .otherwise
      redirectTo: '/'
  $locationProvider.html5Mode(true)
]
