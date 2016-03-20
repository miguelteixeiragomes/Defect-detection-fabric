/**
 * Created by diogocosta on 20/07/15.
 * config part of the project TOPtxt
 * TOP Docs
 */
// Set the require.js configuration for your application.
    require.config({
        baseUrl: './script',
        paths: {
            // JavaScript folders
            'fixed':        'library',
            'app':          'defectdetection',
            'core':         'defectdetection/core',
            'processing':   'defectdetection/imageprocessing',

            // Libraries
            'base64': "library/base64"
        },

        // Initialize the application with the main application file
        deps: ["defectdetection/main"]
    });