werServices = angular.module 'werEventState', []

werServices.factory 'eventStateFactory', ['$q', '$http', '$resource', '$filter', ($q, $http, $resource, $filter) ->
  class EventPhase
    constructor : (@name, @completed, @active, @url) ->
      @displayName = @name
      if (@displayName != null)
        @displayName = @displayName.toLowerCase();
        @displayName = @displayName.substring(0,1).toUpperCase()+@displayName.substring(1);
      if !@url?
        @url = @name

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
        @_phases = []
        @_phases.push(new EventPhase('planning', phaseNames.indexOf('planning') < phaseNames.indexOf(@event.state), 'planning' == @event.state))
        @_phases.push(new EventPhase('draft', phaseNames.indexOf('draft') < phaseNames.indexOf(@event.state), 'draft' == @event.state))

        # Add rounds, this is a little special
        if @event.round_set__ov.length == 0
          @_phases.push(new EventPhase('rounds', phaseNames.indexOf('rounds') < phaseNames.indexOf(@event.state), false))
        for item, index in @event.round_set__ov
          @_phases.push(new EventPhase('round' + (index+1), index + 1 < @event.round_set__ov.length || phaseNames.indexOf('rounds') < phaseNames.indexOf(@event.state), index + 1 == @event.round_set__ov.length && !(phaseNames.indexOf('rounds') < phaseNames.indexOf(@event.state)), 'round/' + (index+1)))


        @_phases.push(new EventPhase('conclusion', phaseNames.indexOf('conclusion') < phaseNames.indexOf(@event.state), 'conclusion' == @event.state))
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
