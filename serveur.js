var http = require('http');
var fs = require('fs');
const fastcsv = require("fast-csv");
const ws = fs.createWriteStream("res.csv");
var mysql = require('mysql');

// Chargement du fichier index.html affiché au client
var server = http.createServer(function(req, res) {
    fs.readFile('./index.html', 'utf-8', function(error, content) {
        res.writeHead(200, {"Content-Type": "text/html"});
        res.end(content);
    });
});

// Connexion à la base
const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "etudespratiques",
  database: "animal"
});

// Fonction Lecture Base / Ecriture fichier

function demande(rqt){
	
	// ON DEMANDE LES DONNEES A LA BASE
	
	connection.query(rqt, function(error, data, fields) {
		if (error) throw error;
		const jsonData = JSON.parse(JSON.stringify(data));

	// ECRITURE FICHIER
	
		fastcsv.write(jsonData, { headers: true })
		.on("finish", function() {
			console.log("Write to res.csv successfully!");
			})
		.pipe(ws);
	});
}	
// FONCTION UPDATE BASE : param = 0 no_count || param = 1 yes_count

function update(name,question,reponse,param){
	
	let rqt = ""
	if (param == 0) {
		rqt = "UPDATE app_answer SET no_count = ? WHERE question_id = (select id from app_question where id = ?) AND item_id = (select id from app_item where name = ?)";
	} else {
		rqt = "UPDATE app_answer SET yes_count = ? WHERE question_id = (select id from app_question where id = ?) AND item_id = (select id from app_item where name = ?)";
	}
	console.log(rqt)
	connection.query(rqt,[reponse,question,name],function (err,result) {
    if (err) throw err;
	console.log(result.affectedRows + " record(s) updated");
	});
}

// CHARGEMENT DE SOCKET.IO

var io = require('socket.io').listen(server);

io.sockets.on('connection', function (socket) {
	console.log("Connecté \n")
	
	// EVENEMENT REQUETE SQL
	
	socket.on('requetesql', function(rqt) {
		connection.connect(error => {
		if (error) throw error;
		demande(rqt);
		});
	});
	
	// EVENEMENT UPDATE SQL
	
	socket.on('updatesql', ({name,qid,value,param}) => {
		connection.connect(error => {
		if (error) throw error;
		update(name,qid,value,param);
		console.log(name,qid,value,param);
		});
	});
	
	// ON ENVOIE LES LISTES DE PERSONNAGES ET QUESTIONS
	socket.on('tab', function() {
		var pers = []
		var questions = []
		connection.connect(error => {
			if (error) throw error;
			connection.query("Select name from app_item", function(error, data, fields) {
			if (error) throw error;
			console.log(data)
			pers = data
			});
			connection.query("Select title from app_question", function(error, data, fields) {
			if (error) throw error;
			console.log(data)
			questions = data
			});
		});
		socket.emit('restab',{tabpers : pers , tabques : questions});
	});
});

// ON ECOUTE LE PORT

server.listen(8080);