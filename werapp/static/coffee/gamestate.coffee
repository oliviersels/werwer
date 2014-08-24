werServices = angular.module 'werGameState', []

werServices.factory 'gameStateFactory', ['$q', '$http', '$resource', '$filter', ($q, $http, $resource, $filter) ->
  class GamePhase
    constructor : (@name, @completed, @active) ->
      @displayName = @name
      if (@displayName != null)
        @displayName = @displayName.toLowerCase();
        @displayName = @displayName.substring(0,1).toUpperCase()+@displayName.substring(1);

  Object.defineProperty(GamePhase.prototype, 'disabled',
    enumerable: true
    get: () ->
     !@completed && !@active
  )

  class GameState
    constructor : (@game) ->

    getPhase: (name) ->
      for phase in @phases
        if phase.name == name
          return phase

  Object.defineProperty(GameState.prototype, 'currentPhase',
    enumerable: true
    get: () ->
      for phase in @phases
        if phase.active
          return phase
  )

  Object.defineProperty(GameState.prototype, 'phases',
    enumerable: true
    configurable: true
    get: () ->

  )

  class SimpleDraftState extends GameState
    constructor: (game) ->
      super game
      @_phases

  Object.defineProperty(SimpleDraftState.prototype, 'phases',
    enumerable: true
    get: () ->
      if not @_phases
        phaseNames = ['planning', 'draft', 'rounds', 'conclusion']
        @_phases = ((new GamePhase(phase, phaseNames.indexOf(phase) < phaseNames.indexOf(@game.state), phase == @game.state) for phase in phaseNames))
      return @_phases
  )

  {
    createGameState: (game) ->
      # Return the correct game state based on the type of game
      switch game.game_type
        when 'casual_limited' then new SimpleDraftState(game)
        when 'casual_constructed' then new CasualConstructed(game)
  }
]
