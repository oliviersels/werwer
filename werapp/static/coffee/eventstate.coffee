werServices = angular.module 'werEventState', []

werServices.factory 'eventStateFactory', ['$q', '$http', '$resource', '$filter', ($q, $http, $resource, $filter) ->
  class EventPhase
    constructor : (@name, @completed, @active) ->
      @displayName = @name
      if (@displayName != null)
        @displayName = @displayName.toLowerCase();
        @displayName = @displayName.substring(0,1).toUpperCase()+@displayName.substring(1);

  Object.defineProperty(EventPhase.prototype, 'disabled',
    enumerable: true
    get: () ->
     !@completed && !@active
  )

  class EventState
    constructor : (@event) ->

    getPhase: (name) ->
      for phase in @phases
        if phase.name == name
          return phase

  Object.defineProperty(EventState.prototype, 'currentPhase',
    enumerable: true
    get: () ->
      for phase in @phases
        if phase.active
          return phase
  )

  Object.defineProperty(EventState.prototype, 'phases',
    enumerable: true
    configurable: true
    get: () ->

  )

  class SimpleDraftState extends EventState
    constructor: (event) ->
      super event
      @_phases

  Object.defineProperty(SimpleDraftState.prototype, 'phases',
    enumerable: true
    get: () ->
      if not @_phases
        phaseNames = ['planning', 'draft', 'rounds', 'conclusion']
        @_phases = ((new EventPhase(phase, phaseNames.indexOf(phase) < phaseNames.indexOf(@event.state), phase == @event.state) for phase in phaseNames))
      return @_phases
  )

  {
    createEventState: (event) ->
      # Return the correct event state based on the type of event
      switch event.event_type
        when 'casual_limited' then new SimpleDraftState(event)
        when 'casual_constructed' then new CasualConstructed(event)
  }
]
