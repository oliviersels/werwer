// Generated by CoffeeScript 1.4.0
(function() {
  var werControllers;

  werControllers = angular.module('werControllers', ['werServices', 'ngRoute', 'ui.bootstrap', 'djangoDynamics']);

  werControllers.controller('HomeController', [
    '$scope', function($scope) {
      return werApi.Match.then(function(Match) {
        return $scope.previousMatches = Match.query();
      });
    }
  ]);

  werControllers.controller('PlayerController', [
    '$scope', '$location', 'werApi', function($scope, $location, werApi) {
      werApi.Player.then(function(Player) {
        return $scope.players = Player.query();
      });
      return $scope.editPlayer = function(player) {
        return $location.path('/edit-player/' + player.id + '/');
      };
    }
  ]);

  werControllers.controller('EditPlayerController', [
    '$scope', '$location', 'werApi', '$routeParams', '$modal', function($scope, $location, werApi, $routeParams, $modal) {
      werApi.Player.then(function(Player) {
        return Player.get({
          id: $routeParams.playerId
        }, function(player, response) {
          return $scope.player = player;
        }, function(response) {
          $scope.player = null;
          return $scope.error = response.status;
        });
      });
      $scope.submit = function() {
        return $scope.player.$update({}, function(data) {
          return $location.path('/players/');
        });
      };
      $scope.confirmDelete = function() {
        var modal;
        modal = $modal.open({
          templateUrl: "/partials/edit-player-confirm/",
          controller: 'EditPlayerConfirmController',
          resolve: {
            player: function() {
              return $scope.player;
            }
          }
        });
        return modal.result.then(function() {
          return $scope["delete"]();
        });
      };
      return $scope["delete"] = function() {
        return $scope.player.$delete({}, function(data) {
          return $location.path('/players/');
        });
      };
    }
  ]);

  werControllers.controller('EditPlayerConfirmController', [
    '$scope', '$modalInstance', 'player', function($scope, $modalInstance, player) {
      $scope.player = player;
      $scope["delete"] = function() {
        return $modalInstance.close();
      };
      return $scope.close = function() {
        return $modalInstance.dismiss('cancel');
      };
    }
  ]);

  werControllers.controller('AddPlayerController', [
    '$scope', 'werApi', '$location', function($scope, werApi, $location) {
      werApi.Player.then(function(Player) {
        return $scope.player = new Player();
      });
      return $scope.submit = function() {
        $scope.player.username = $scope.player.first_name + '.' + $scope.player.last_name;
        return $scope.player.$save({}, function() {
          return $location.path('/players/');
        });
      };
    }
  ]);

  werControllers.controller('NewGameController', [
    '$scope', '$filter', 'werApi', 'djangoEnums', function($scope, $filter, werApi, djangoEnums) {
      werApi.Game.then(function(Game) {
        return $scope.game = new Game({
          game_type: 'casual_limited',
          pairing_method: 'swiss',
          date: new Date()
        });
      });
      $scope.datepickerOpened = false;
      $scope.openDatepicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        return $scope.datepickerOpened = true;
      };
      $scope.optionsGameType = djangoEnums.GameType;
      $scope.optionsPairingMethod = djangoEnums.PairingMethod;
      return $scope.submit = function() {
        console.log($scope.game);
        $scope.game.date = $filter('date')($scope.game.date, 'yyyy-MM-dd');
        return $scope.game.$save();
      };
    }
  ]);

}).call(this);
