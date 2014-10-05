
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
    .when '/events-overview/',
      templateUrl: '/partials/events-overview/',
      controller: 'EventsOverviewController'
    .when '/new-event/',
      templateUrl: '/partials/new-event/',
      controller: 'NewEventController'
    .when '/event/:eventId/',
      templateUrl: '/partials/event/',
      controller: 'EventController'
    .when '/event/:eventId/planning/',
      templateUrl: '/partials/event-planning/',
      controller: 'EventPlanningController'
    .when '/event/:eventId/draft/',
      templateUrl: '/partials/event-draft/',
      controller: 'EventDraftController'
    .when '/event/:eventId/round/:roundId/',
      templateUrl: '/partials/event-round/',
      controller: 'EventRoundController'
    .when '/event/:eventId/rounds/',
      redirectTo: '/event/:eventId/round/1/'
    .when '/event/:eventId/standings/',
      templateUrl: '/partials/event-standings/',
      controller: 'EventStandingsController'
    .when '/event/:eventId/conclusion/',
      templateUrl: '/partials/event-conclusion/',
      controller: 'EventConclusionController'

    .otherwise
      redirectTo: '/'
  $locationProvider.html5Mode(true)
]
