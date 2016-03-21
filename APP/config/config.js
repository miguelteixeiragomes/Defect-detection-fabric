/**
 * Created by Joao COsta on 20/03/16.
 */

require.config({
    baseUrl: './APP',
    paths: {
        // JavaScript folders
        'fixed':        "library",
        'app':          "jsapp",
        'core':         "jsapp/core",
        'processing':   "jsapp/imageprocessing",
        'values':       "values",

        // Libraries
        'base64': "library/base64"
    },

    // Initialize the application with the main application file
    deps: ["jsapp/main"]
});