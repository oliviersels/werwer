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

  dynamics.factory('djangoSettings', function() {
      return {
          'client_id': '{{ client_id }}',
          'oauth2_endpoint': '{{ oauth2_endpoint }}'
      }
  });

}).call(this);
