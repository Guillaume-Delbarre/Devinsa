//ExecutionPython
let {PythonShell} = require('python-shell');

//Dialogue Site web
var express = require('express');
var session = require('express-session');
var app = express();
var server = app.listen(8080);

//Ecriture fichier
var fs = require('fs');
const fastcsv = require("fast-csv");
const ws = fs.createWriteStream("../donnees/Vecteur.csv");
const as = fs.createWriteStream("../donnees/Arbre.csv");

// CHARGEMENT DE SOCKET.IO
var io = require('socket.io').listen(server);
console.log("Serveur lancé");

//Dialogue Base
var mysql = require('mysql');

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

//Jsp truc bizarre
var bodyParser = require('body-parser');
var path = require('path');


// On importe le fichier chemins.js qui permet de router les demandes clients
var Chemins = require('./Chemins');
app.use('/', Chemins);

function fileattente(tab){
	route = "../ScriptPython/";
	chemin = route.concat(tab[0]);
	PythonShell.run(chemin, null, function (err) {
		if (err) throw err;
		console.log('Fichier JS Ecrit');
		if (tab.length > 1){
			fileattente(tab.slice(1));
		}
	});
}
	
io.sockets.on('connection', function (socket) {
	console.log("Connecté \n")
	// EVENEMENT REQUETE SQL
	socket.on('message', ({message}) => {
		console.log(message);
	});
	
	socket.on('ecrirevecteursql', function() {
		demande(scriptpca);
	});
	
	// EVENEMENT UPDATE SQL
	
	socket.on('updatesql', ({name,qname,value,param}) => {
		update(name,qname,value,param);
	});
	
	socket.on('montrerquestionssql', ({name,persos,nb}) => {
		montrequestion(name,persos,nb);
	});
	
	socket.on('creerarbre', ({profondeur}) => {
		creerarbre(profondeur,["apptree.py"]);
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
		let insert = "";
		if (name != null && question != null && value != null && param != null){
			if (param == 0) {
				rqt = "UPDATE app_answer SET no_count = ? WHERE question_id = (select id from app_question where title = ?) AND item_id = (select id from app_item where name = ?)";
				insert = "INSERT INTO app_answer (question_id, item_id, yes_count,  no_count, pass_count, yes_tfidf, no_tfidf) VALUES ( ?, ?, 0, ?, 0, 0, 0)";
			} else {
				rqt = "UPDATE app_answer SET yes_count = ? WHERE question_id = (select id from app_question where title = ?) AND item_id = (select id from app_item where name = ?)";
				insert = "INSERT INTO app_answer (question_id, item_id, yes_count,  no_count, pass_count, yes_tfidf, no_tfidf) VALUES ( ?, ?, ?, 0, 0, 0, 0)";
			}
			connection.query(rqt,[value,question,name],function (err,result) {
				if (err) throw err;
				if (result.affectedRows != 0){ 
					console.log(result.affectedRows + " record(s) updated");
					socket.emit("message","Update Done " + result.affectedRows);
				}else{
					connection.query("select id from app_question where title = ? UNION select id from app_item where name = ?",[question,name],function (error,res) {
						if (error) throw error;
						let questionid = res[0].id;
						let itemid = res[1].id;
						connection.query(insert,[questionid,itemid,value],function (errors,resultats) {
							if (errors) throw errors;
							socket.emit("message","Resultat inséré ");
						});
					});
				}
			});
			console.log("Nom : ",name," Titre de la question : ",question," Valeur actuelle : ",value," Paramètre changé : ",param);
		}else{
			socket.emit("message","parametres incorrects");
		}
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
				console.log("Ecriture faite");
				//callback();
			});
		});
	}
	
	function creerarbre(profondeur,fonctions = null){
	// ON DEMANDE L'ARBRE A LA BASE
		var rqt = "Select title, choice, app_tree.id, parent_id, depth from app_tree inner join app_question on question_id = app_question.id where depth < ? order by depth ;";
		connection.query(rqt, [profondeur], function(error, data, fields) {
			if (error) throw error
			const jsonData = JSON.parse(JSON.stringify(data));
			// ECRITURE FICHIER
			console.log("Ecriture Arbre en cours");
			socket.emit("message","Ecriture Arbre en cours");
			var a = 
			fastcsv.write(jsonData, { headers: true }).pipe(as);
			a.on('finish', function () {
				socket.emit("message","Arbre ecrit");
				console.log("Ecriture Arbre faite");
				if (fonctions != null){
				fileattente(fonctions);
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
});