(function() {
  var dynamics = angular.module('djangoDynamics', []);

  dynamics.factory('djangoEnums', function() {
      return {
          {% for enum in enums %}
          {{enum.name}}: {
              {% for choice in enum.choices %}
                  {{choice.0}}: '{{choice.1}}'{% if not forloop.last %},{% endif %}
              {% endfor %}
          }{% if not forloop.last %},{% endif %}
          {% endfor %}
      }
  });

}).call(this);
