module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    coffee: {
      compile: {
        expand: true,
        flatten: true,
        cwd: 'werapp/static/coffee',
        src: ['**/*.coffee'],
        dest: 'werapp/static/js/compiled',
        ext: '.js'
      }
    }
  });

  // Load the plugin that provides the "coffee" task.
  grunt.loadNpmTasks('grunt-contrib-coffee');

  // Default task(s).
  grunt.registerTask('default', ['coffee']);

};
