/**
 * Created by JoaoCosta on 20/03/16.
 */
var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic(__dirname)).listen(8000);