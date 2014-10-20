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

  dynamics.constant('werwer_root', '{% url 'werwer-root' %}')
  dynamics.constant('partials_root', '{% url 'werwer-partials-root' %}')
  dynamics.factory('djangoSettings', function() {
      return {
          'client_id': '{{ client_id }}',
          'oauth2_endpoint': '{{ oauth2_endpoint }}',
      }
  });

}).call(this);
