//ExecutionPython
let {PythonShell} = require('python-shell');


//Ecriture fichier
var fs = require('fs');
const fastcsv = require("fast-csv");
const ws = fs.createWriteStream("../donnees/Vecteur.csv");
const as = fs.createWriteStream("../donnees/Arbre.csv");

//Dialogue Base
var mysql = require('mysql');

//Dialogue Site web
var app = require('express')();
var server = app.listen(8080);
var session = require('express-session');

//Jsp truc bizarre
var bodyParser = require('body-parser');
var path = require('path');

// CHARGEMENT DE SOCKET.IO
var io = require('socket.io').listen(server);

// Connexion à la base
const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "etudespratiques",
  database: "animal"
});

// On lance la connexion 
connection.connect(function(err) {
	if (err) throw err;
});


app.use(session({
	secret: 'secret',
	resave: true,
	saveUninitialized: true
}));
app.use(bodyParser.urlencoded({extended : true}));
app.use(bodyParser.json());

app.get('/', function(request, response) {
	response.sendFile(path.join(__dirname + '/login.html'));
});

app.get('/home', function(request, response) {
	if (request.session.loggedin) {
		// Chargement du fichier index.html affiché au client
		console.log('index.html')
		response.sendFile('dialogueServeur.html', {
        root: path.join(__dirname, './')
		})
	} else {
		response.send('Please login to view this page!');
	}
});

app.post('/auth', function(request, response) {
	var username = request.body.username;
	var password = request.body.password;
	if (username && password) {
		connection.query('SELECT * FROM accounts WHERE username = ? AND password = ?', [username, password], function(error, results, fields) {
			if (results.length > 0) {
				request.session.loggedin = true;
				request.session.username = username;
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

io.sockets.on('connection', function (socket) {
	console.log("Connecté \n")
		
	// EVENEMENT REQUETE SQL
	socket.on('message', ({message}) => {
		console.log(message);
	});
	
	socket.on('ecrirevecteursql', function() {
		demande(scriptpca)
	});
	
	socket.on('ecrirearbre', ({profondeur}) => {
		creerarbre(scriptarbre, profondeur);
	});
	
	// EVENEMENT UPDATE SQL
	
	socket.on('updatesql', ({name,qname,value,param}) => {
		update(name,qname,value,param);
	});
	
	socket.on('montrerquestionssql', ({name,persos,nb}) => {
		montrequestion(name,persos,nb);
	});
		
	// ON ENVOIE LES LISTES DE PERSONNAGES ET QUESTIONS
	socket.on('tab', function() {
		var pers = [];
		var questions = [];
		connection.query("Select name from app_item", function(error, data, fields) {
			if (error) throw error;
			console.log(data);
			pers = data;
			});
		connection.query("Select title from app_question", function(error, data, fields) {
			if (error) throw error;
			console.log(data)
			questions = data;
			});
			socket.emit('restab',{tabpers : pers , tabques : questions});
		});
		
	
	// FONCTION UPDATE BASE : param = 0 no_count || param = 1 yes_count

	function update(name,question,value,param){
		let rqt = "";
		if (param == 0) {
			rqt = "UPDATE app_answer SET no_count = ? WHERE question_id = (select id from app_question where title = ?) AND item_id = (select id from app_item where name = ?)";
		} else {
			rqt = "UPDATE app_answer SET yes_count = ? WHERE question_id = (select id from app_question where title = ?) AND item_id = (select id from app_item where name = ?)";
		}
		connection.query(rqt,[value,question,name],function (err,result) {
		if (err) throw err;
			console.log(result.affectedRows + " record(s) updated");
			socket.emit("message","Update Done " + result.affectedRows);
		});
		console.log("Nom : ",name," Titre de la question : ",question," Valeur actuelle : ",value," Paramètre changé : ",param);
	}
	
	// Montre les questions similaires SUREMENT PRB GUILLEMET
	
	function montrequestion(name,persos,nb){
		let rqt = "select * from (select title, avg(yes_count), avg(no_count) from (select * from (select question_id,yes_count,no_count from app_answer where item_id in (select id from app_item where name != ? and name in ?) ) as a1 inner join app_question on app_question.id = a1.question_id) as a2 group by question_id order by sum(yes_count) desc limit ? ) as f1 select * from (select title, avg(yes_count), avg(no_count) from (select * from (	select question_id,yes_count,no_count from app_answer where item_id in (select id from app_item where id != ? and name in ?)) as a1 inner join app_question on app_question.id = a1.question_id) as a2 group by question_id order by sum(no_count) desc limit ? ) as f2;";
		connection.query(rqt,[name,persos,nb,name,persos,nb],function (err,result) {
		if (err) throw err;
			console.log(result.affectedRows + " record(s) extracted");
			// Pas affectedRows je pense
			socket.emit("message","Questions Done " + result.affectedRows);
		});
	}
	
	// Fonction Lecture Base / Ecriture fichier

	function demande(callback){
	// ON DEMANDE LES DONNEES A LA BASE
		var rqt = "SELECT name,yes_tfidf,no_tfidf FROM ( SELECT name,title,id,idg FROM ( SELECT id AS idg, name FROM app_item where id in (Select distinct item_id from app_answer)) AS itemCROSS JOIN (select distinct id,title from app_question where id IN (select distinct question_id from app_answer)) as t0 ) AS t1 LEFT JOIN (select item_id,question_id,yes_tfidf,no_tfidf from app_answer) as a ON t1.id=a.question_id AND t1.idg=a.item_id ORDER BY name,title";
		connection.query(rqt, function(error, data, fields) {
			if (error) throw error
			const jsonData = JSON.parse(JSON.stringify(data));
	// ECRITURE FICHIER
			console.log("Ecriture en cours");
			socket.emit("message","Ecriture en cours");
			var a = 
			fastcsv.write(jsonData, { headers: true }).pipe(ws);
			a.on('finish', function () {
				socket.emit("message","Fichier ecrit");
				console.log("Ecriture Fait faite");
				callback();
			});
		});
	}
	
	function creerarbre(callback = null, profondeur){
	// ON DEMANDE L'ARBRE A LA BASE
		var rqt = "Select title, choice, question_id,parent_id,depth from app_tree inner join app_question on question_id = app_question.id where depth < ? order by depth ;";
		connection.query(rqt, [profondeur], function(error, data, fields) {
			if (error) throw error
			console.log(data)
			const jsonData = JSON.parse(JSON.stringify(data));
	// ECRITURE FICHIER
			console.log("Ecriture Arbre en cours");
			socket.emit("message","Ecriture Arbre en cours");
			var a = 
			fastcsv.write(jsonData, { headers: true }).pipe(as);
			a.on('finish', function () {
				socket.emit("message","Arbre ecrit");
				console.log("Ecriture Arbre faite");
				if (callback != null){
				callback();
				}
			});
			
		});
	}
	
	function scriptarbre(){
		PythonShell.run("../ScriptPython/apptree.py", null, function (err) {
			if (err) throw err;
			console.log('Fichier JS Ecrit');
		});
	}
	
	function scriptpca(){
		PythonShell.run("../ScriptPython/MiseEnPage.py", null, function (err) {
			if (err) throw err;
			console.log('MISE EN PAGE FAITE');
			PythonShell.run("../ScriptPython/ScriptPCA.py", null, function (err) {
			if (err) throw err;
			console.log('finished PCA');
			});
		});
	}
	
	// Main temporaire
	creerarbre(scriptarbre, 10);
});