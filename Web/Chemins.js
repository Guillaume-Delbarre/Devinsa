//Jsp truc bizarre
var bodyParser = require('body-parser');
var path = require('path');
var session = require('express-session');
var express = require('express');
var app = express();
var router = express.Router();
var mysql = require('mysql');
const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "devinsa!",
  database: "devinsa"
});

router.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));

router.use(express.static(__dirname + '/graph'));
router.use(express.static(__dirname + '/Arbre_Binaire'));

router.use(bodyParser.urlencoded({extended : true}));
router.use(bodyParser.json());

router.get('/', function(request, response) {
	if (request.session.loggedin){
		response.redirect('/home');
	}else{
		response.sendFile(path.join(__dirname + '/login.html'));
	}
});

router.get('/home', function(request, response) {
	if (request.session.loggedin) {
		// Chargement du fichier acceuil.html affiché au client
		response.sendFile(path.join(__dirname + '/graph/acceuil.html'));
	} else {
		// On retourne au login
		response.sendFile(path.join(__dirname + '/login.html'));
	}
});

router.get('/resPCA.csv', function(request, response) {
	if (request.session.loggedin) {
		// Chargement du fichier acceuil.html affiché au client
		response.sendFile(path.join(__dirname + '../Donnees/resPCA.csv'));
	} else {
		// On retourne au login
		response.sendFile(path.join(__dirname + '/login.html'));
	}
});

router.post('/Arbre', function(request, response) {
	if (request.session.loggedin){
		response.sendFile(path.join(__dirname + '/Arbre_Binaire/Treeweb.html'));
	}else{
		response.sendFile(path.join(__dirname + '/login.html'));
	}
});

router.post('/acceuil', function(request, response) {
	if (request.session.loggedin){
		response.sendFile(path.join(__dirname + '/graph/acceuil.html'));
	}else{
		response.sendFile(path.join(__dirname + '/login.html'));
	}
});

router.post('/acceuil', function(request, response) {
	if (request.session.loggedin){
		response.sendFile(path.join(__dirname + '/graph/acceuil.html'));
	}else{
		response.sendFile(path.join(__dirname + '/login.html'));
	}
});

router.post('/auth', function(request, response) {
	var username = request.body.username;
	var password = request.body.password;
	// On confirme les informations
	if (username && password) {
		connection.query('SELECT * FROM accounts WHERE login = ? AND password = ?', [username, password], function(error, results, fields) {
			if (results.length > 0) {
				request.session.loggedin = true;
				request.session.username = username;
				console.log("Connection depuis l'adresse : " + request.connection.remoteAddress);
				response.redirect('/home');
			} else {
				response.send('Incorrect Username and/or Password!');
			}			
			response.end();
		});
	} else {
		response.send('Please enter Username and Password!');
		response.end();
	}
});

module.exports = router;
