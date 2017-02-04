var https = require('https');
var fs = require('fs');
var options = {
  key: fs.readFileSync('/var/www/html/.well-known/acme-challenge/private.key'),
  cert: fs.readFileSync('/var/www/html/.well-known/acme-challenge/certificate.crt')
};

var express    = require('express');        // call express
var app        = express();                 // define our app using express
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// set our port

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();              // get an instance of the express Router

router.get('/', function(req, res) {
      res.json(<respone we want to send>);
});
});


// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/api', router);
app.get('/', function( req,res) {
  res.sendfile(<file to send>);
});
https.createServer(options,app).listen(443);
