/*
    CentralReport Gruntfile

    This file is used by Grunt to compile the front assets.
    You need:
        - Node.js
        - Grunt installed globally

    To run init, just call "grunt" inside the current directory.
*/

module.exports = function(grunt) {

    // Load grunt tasks automatically
    require('load-grunt-tasks')(grunt);

    // Displays the time taken for each task
    require('time-grunt')(grunt);

    // Project configuration.
    grunt.initConfig({
        cr: {
            dirs: {
                cwd: './',
                crDesign: '<%= cr.dirs.cwd %>node_modules/CentralReport_design/dist',
                web: '<%= cr.dirs.cwd %>centralreport/cr/web',
                webDev: '<%= cr.dirs.web %>/static_dev',
                webDist: '<%= cr.dirs.web %>/static',
                vendor: '<%= cr.dirs.cwd %>bower_components'
            },
            js: [
                '<%= cr.dirs.vendor %>/angular/angular.js',
                '<%= cr.dirs.vendor %>/angular-route/angular-route.js',
                '<%= cr.dirs.webDev %>/js/centralreport.js',
                '<%= cr.dirs.webDev %>/js/app/app.js',
                '<%= cr.dirs.webDev %>/js/app/controllers.js',
                '<%= cr.dirs.webDev %>/js/app/directives.js'
            ]
        },

        pkg: grunt.file.readJSON('package.json'),

        bower: {
            install: {
                options: {
                    copy: false,
                    verbose: true
                }
            }
        },

        uglify: {
            development: {
                options: {
                    banner: '/*! <%= pkg.name %> - DEV - <%= grunt.template.today("yyyy-mm-dd") %> */\n',
                    beautify: true,
                    mangle: false
                },
                files: {
                    '<%= cr.dirs.webDist %>/js/centralreport.js' : ['<%= cr.js %>']
                }
            },
            production: {
                options: {
                    banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
                },
                files: {
                    '<%= cr.dirs.webDist %>/js/centralreport.js' : ['<%= cr.js %>']
                }
            }
        },

        copy: {
            main: {
                expand: true,
                flatten: true,
                filter: 'isFile',
                cwd: '<%= cr.dirs.crDesign %>/fonts',
                src: '**',
                dest: '<%= cr.dirs.webDist %>/fonts'
            },

            img: {
                expand: true,
                filter: 'isFile',
                cwd: '<%= cr.dirs.webDev %>/img',
                src: '**',
                dest: '<%= cr.dirs.webDist %>/img'
            },

            styles: {
                expand: true,
                cwd: '<%= cr.dirs.crDesign %>/css',
                src: '**',
                dest: '<%= cr.dirs.webDist %>/css'
            },

            partials: {
                expand: true,
                cwd: '<%= cr.dirs.webDev %>/partials',
                src: '**',
                dest: '<%= cr.dirs.webDist %>/partials'
            },
        },

        // Watches files for changes and runs tasks based on the changed files
        watch: {
            js: {
                files: ['<%= cr.dirs.webDev %>/js/**.js', '<%= cr.dirs.webDev %>/js/app/**.js'],
                tasks: ['uglify:development']
            },
            static: {
                files: ['<%= cr.dirs.webDev %>/**'],
                tasks: ['copy']
            },
            gruntfile: {
                files: ['Gruntfile.js']
            },
        }
    });

    // Default task(s).
    grunt.registerTask('default', [
        'bower',
        'uglify:development',
        'copy'
    ]);

    grunt.registerTask('prod', [
        'bower',
        'uglify:production',
        'copy'
    ]);

    grunt.registerTask('serve', [
        'uglify:development',
        'copy',
        'watch'
    ]);

};
