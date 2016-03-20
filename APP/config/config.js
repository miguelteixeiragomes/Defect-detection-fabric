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
            'fixed': "library",
            'app': "topeditor",
            'core': 'topeditor/core',
            'docx': 'topeditor/docx',
            'gui': 'topeditor/gui',
            'operation': 'topeditor/operation',
            'values': 'values',

            // Libraries
            'base64': "library/base64",
            'detect': "library/detect",
            'filesaver': "library/filesaver-min",
            'openxml': "library/openxml",
            'jszipDeflate': "library/jszip-deflate",
            'jszipInflate': "library/jszip-inflate",
            'jszipLoad': "library/jszip-load",
            'jszip': "library/jszip",
            'linq' : "library/linq",
            'ltxml': "library/ltxml",
            'ltxml-extensions': "library/ltxml-extensions"
        },

        shim:{
            'jszipDeflate':{
                deps:['jszip']
            },
            'jszipInflate':{
                deps:['jszip']
            },
            'jszipLoad':{
                deps:['jszip']
            },
            'openxml':{
                exports:'openXml'
            },
            'linq':{
                exports:'Enumerable'
            },
            'ltxml':{
                exports:'Ltxml'
            },
            'ltxml-extensions':{
                exports:'XEnumerable'
            }
        },
        // Initialize the application with the main application file
        deps: ["topeditor/main"]
    });