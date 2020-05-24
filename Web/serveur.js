//ExecutionPython
let {PythonShell} = require('python-shell');
//Dialogue Site web
var express = require('express');
var session = require('express-session');
const helmet = require('helmet');
var app = express();
app.use(helmet());
var server = require('http').createServer(app);
var scripting = 0;
var scriptingtree = 0;
server.listen(8080, "10.133.33.20", function(){
	console.log("listening at port : 8080");
});
//Ecriture fichier
var fs = require('fs');
const fastcsv = require("fast-csv");

// CHARGEMENT DE SOCKET.IO
var io = require('socket.io')(server);
console.log("Serveur lancé");

//Dialogue Base
var mysql = require('mysql');

// Connexion à la base
const connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "devinsa!",
  database: "devinsa"
});

// On lance la connexion
connection.connect(function(err) {
	if (err) throw err;
});

//Autres
var bodyParser = require('body-parser');
var path = require('path');

// On importe le fichier chemins.js qui permet de router les demandes clients
var Chemins = require('./Chemins');
app.use('/', Chemins);

io.sockets.on('connection', function (socket) {
	//Remplir les tableaux de question et de personnages
	getallques();
	getallpers();

	// EVENEMENT REQUETE SQL
	socket.on('message', ({message}) => {
		console.log(message);
	});

	//AVOIR DES PARAMETRES DE REPONSES
	socket.on('getvaleursreponse', ({qname, name}) => {
		getvaleursreponses(qname, name);
	});

	socket.on('getallpersreponses', ({qname, names}) =>  {
		getvaleursreponsespers(qname, names);
	});


	// EVENEMENT UPDATE SQL
	socket.on('updatesql', ({name,qname,value,param}) => {
		//console.log(qname);
		update(name,qname,value,param);
	});

	socket.on('creerarbre', ({profondeur}) => {
		if (scriptingtree == 0){
			scriptingtree = 1;
			console.log("Finaltree lancé");
			let options = {args: [profondeur], pythonPath: 'python3'};
				PythonShell.run("../ScriptPython/finalTree.py", options, function (err) {
				if (err) {
					console.log("Finaltree.py erreur");
					console.log(err);
				}else{
					console.log("Finaltree fini");
				}
				scriptingtree = 0;
			});
		}
	});

	// LANCER SCRIPTS
	socket.on('ecrirevecteursql', function() {
		if (scripting == 0){
			scripting = 1;
			demande(["MiseEnPage.py"], []);
		}
	});

	socket.on('ecrirequestiondiff', ({liste1, liste2}) => {
		lancerscript(["differences.py"], [liste1, liste2]);
	});

	socket.on('toutlancer', ({nbcluster, nbquestions}) => {
		if (Number.isInteger(nbcluster) && Number.isInteger(nbquestions)){
			if (scripting == 0){
				scripting = 1;
				demande(["MiseEnPage.py", "CHA.py", "questionsCaracteristiques.py", "PCA.py"], [nbcluster, nbquestions]);
			}
		}else{
			socket.emit("message", "paramètres incorrects");
		}
	});

	socket.on('lancerdeuxièmepartie', ({nbcluster, nbquestions}) => {
		if (Number.isInteger(nbcluster) && Number.isInteger(nbquestions)){
			if (scripting == 0){
				scripting = 1;
				lancercalculs(nbcluster, nbquestions);
			}
		}else{
			socket.emit("message", "paramètres incorrects");
		}
	});

	// FONCTION UPDATE BASE : param = 0 no_count || param = 1 yes_count

	function update(persname,questionname,value,param){
		if (!Number.isInteger(value)){
			return 0;
		}
		//console.log(name,question,value,param);
		let rqt = "";
		let insert = "";
		if (persname != null && questionname != null && value != null && param != null){
			if (param == "yes_count"){
				rqt = "UPDATE app_answer SET yes_count = ? WHERE question_id = (select id from app_question where title = ?) AND item_id = (select id from app_item where name = ?)";
				insert = "INSERT INTO app_answer (id, question_id, item_id, yes_count, no_count, pass_count, yes_tfidf, no_tfidf) VALUES(0, ?, ?, ?, 0, 0, 0, 0)";
			}else if(param == "no_count"){
				rqt = "UPDATE app_answer SET no_count = ? WHERE question_id = (select id from app_question where title = ?) AND item_id = (select id from app_item where name = ?)";
				insert = "INSERT INTO app_answer (id, question_id, item_id, yes_count, no_count, pass_count, yes_tfidf, no_tfidf) VALUES(0, ?, ?, 0, ?, 0, 0, 0)";
			}else if(param == "pass_count"){
				rqt = "UPDATE app_answer SET pass_count = ? WHERE question_id = (select id from app_question where title = ?) AND item_id = (select id from app_item where name = ?)";
				insert = "INSERT INTO app_answer (id, question_id, item_id, yes_count, no_count, pass_count, yes_tfidf, no_tfidf) VALUES(0, ?, ?, 0, 0, ?, 0, 0)";
			}else{
				socket.emit("message","mauvais inséré ");
				return 0;
			}
			connection.query(rqt,[value,questionname,persname],function (err,result) {
				if (err) console.log(err);
				if (result.affectedRows != 0){
					//console.log(result.affectedRows + " record(s) updated");
					//socket.emit("message","Update Done " + result.affectedRows);
				}else{
					connection.query("select id from app_question where title = ? UNION select id from app_item where name = ?",[questionname,persname],function (error,res) {
						if (error) console.log(error);
						if (res.length == 2){				
							let questionid = parseInt(res[0].id);
							let itemid = parseInt(res[1].id);
							//console.log(questionid, itemid
							connection.query(insert,[questionid,itemid,value],function (errors,resultats) {
								if (errors) console.log(errors);
								//socket.emit("message","Resultat inséré ");
								//console.log("Résultat inséré");
							});
						}else{
							//console.log("Personnage: " + questionname + " ou " + "Question: " + questionname + "Non present dans la base");
						}
					});
				}
			});
			//console.log("Nom : ",name," Titre de la question : ",question," Valeur actuelle : ",value," Paramètre changé : ",param);
		}else{
			socket.emit("message","parametres incorrects");
		}
	}

	function fileattente(tab, optionsligne){
		route = "../ScriptPython/";
		chemin = route.concat(tab[0]);
		console.log(tab[0] + " lancé");
		let options = {args: optionsligne};
		PythonShell.run(chemin, options, function (err) {
			setTimeout(function(){
				if (err) {
					console.log(err);
					console.log(tab[0] + " : Echec de l'execution");
					scripting = 0;
				}else{
					console.log(tab[0] + ' fini');
					if (tab.length > 1){
						fileattente(tab.slice(1), optionsligne);
					}
				}
				if(tab.length == 1){
					socket.emit("message", "Scripts finis");
					console.log("Scripts finis");
					scripting = 0;
				}
				socket.emit("refresh");
			}, 0000);
		});
	}
	// Fonction Lecture Base / Ecriture fichier

	function demande(script, options){
		const ws = fs.createWriteStream("../Donnees/Vecteur.csv");
		console.log("Extraction des données");
	// ON DEMANDE LES DONNEES A LA BASE
		var rqt = "SELECT name,yes_tfidf,no_tfidf FROM ( SELECT name,title,id,idg FROM ( SELECT id AS idg, name FROM app_item where id in (Select distinct item_id from app_answer)) AS item CROSS JOIN (select distinct id,title from app_question where id IN (select distinct question_id from app_answer)) as t0 ) AS t1 LEFT JOIN (select item_id,question_id,yes_tfidf,no_tfidf from app_answer) as a ON t1.id=a.question_id AND t1.idg=a.item_id ORDER BY name,title";
		const start = Date.now();
		connection.query(rqt, function(error, data, fields) {
			if (error) console.log(error);
			const jsonData = JSON.parse(JSON.stringify(data));
			var a = fastcsv.write(jsonData, { headers: true }).pipe(ws);
			a.on('finish', function () {
				const zs = fs.createWriteStream("../Donnees/QuestionsLigne.txt");
				var rqt1 = "Select title from app_question where id in (select distinct question_id from app_answer) order by title"
				connection.query(rqt1, function(error, rows) {
					if (error) console.log(error);
					const jsonData1 = JSON.parse(JSON.stringify(rows));
					var b = fastcsv.write(jsonData1, { headers: true }).pipe(zs);
					b.on('finish', function () {
						//socket.emit("message","Fichiers écrits");
						//console.log("Ecriture faite");
						const millis = Date.now() - start;
						//console.log("Temps écriture fichier : ", millis/1000, " secondes");
						if (script != []){
							fileattente(script, options);
						}
					});
				});
			});
		});
	}

	function getvaleursreponses(title,name){
		let rqt = "select yes_count, no_count, pass_count from app_answer where question_id in (select id from app_question where title = ?) and item_id in (select id from app_item where name = ?);"
		connection.query(rqt,[title, name],function (err,result) {
		if (err) console.log(err);
			if (result.length != 0){
				socket.emit("valeursreponses", {y: result[0].yes_count, n: result[0].no_count, p: result[0].pass_count});
			}else{
				socket.emit("valeursreponses", {y: 0, n: 0, p: 0});
			}
		});
	}

	function getvaleursreponsespers(title,names){
		let donnees = "("
		for(let i = 0; i<names.length; i++){
			donnees = donnees + '"' + names[i].replace(/"/g, "") + '"';
			if (i != (names.length - 1)){
				donnees = donnees + ",";
			}
		}
		donnees = donnees + ")";
		let rqt = "select name, yes_count, no_count, pass_count from app_answer inner join app_item on app_item.id = app_answer.item_id and question_id in (select id from app_question where title = ?) and name in " + donnees +";"
		connection.query(rqt,[title],function (err,result) {
			let tabreponse = []
			if (err) console.log(err);
			if (result.length != 0){
				for(let j = 0; j <names.length; j++){
					let pushed = 0;
					for(let g = 0; g<result.length; g++){
						if (names[j] == result[g].name){
							tabreponse.push({nom: names[j], y: result[g].yes_count, n: result[g].no_count, p: result[g].pass_count});
							pushed = 1;
						}
					}
					if (pushed == 0){
						tabreponse.push({nom: names[j], y: 0, n: 0, p: 0});
					}
				}
			}else{
				for(let v = 0; v <names.length; v++){
					tabreponse.push({nom: names[v], y: 0, n: 0, p: 0});
				}
			}
			socket.emit("getallparamreponse", tabreponse);
		});
	}

	function getallpers(){
		let rqt = "select name from app_item where id in (select item_id from app_answer where yes_count > 0 or pass_count > 0 or no_count > 0);"
		connection.query(rqt, function (err,result) {
		if (err) console.log(err);
			if (result.length != 0){
				let pers = []
				for (let i = 0; i < result.length; i++) {
					pers.push(result[i].name);
				}
				socket.emit("getallpersreponse", pers);
			}
		});
	}

	function getallques(){
		let rqt = "select title from app_question where id in (select question_id from app_answer where yes_count > 0 or pass_count > 0 or no_count > 0);"
		connection.query(rqt, function (err,result) {
			if (err) console.log(err);
			if (result.length != 0){
				let ques = []
				for (let i = 0; i < result.length; i++) {
					ques.push(result[i].title);
				}
				socket.emit("getallquesreponse", ques);
			}
		});
	}

	//lancerscript(["differences.py"], [liste1, liste2]);
/*
	function lancerscript(nom,optionsligne){
		let options = {
			args: optionsligne
		};
		path = "../ScriptPython/".concat(nom);
		
		console.log("lancement script")

		PythonShell.run(path,options, function (err) {
			if (err) {
				console.log(err)
			}
			socket.emit('finComparaison');
		})
	}
	*/
	function lancerscript(nom, optionsligne){
		console.log(nom + " : Script lancé");
		path = "../ScriptPython/".concat(nom);
		let options = {args: optionsligne};
		PythonShell.run(path, options, function (err) {
			if (err) {
				console.log(err)
				console.log(nom + " : Echec de l'execution");
			}else{
				socket.emit('finComparaison');
			}
		});
	}

	function lancercalculs(nbcluster, nbquestions){
		var stats1 = fs.statSync("../Donnees/Vecteur.csv");
		var fileSizeInBytes1 = stats1["size"];
		var stats2 = fs.statSync("../Donnees/Personnages.csv");
		var fileSizeInBytes2 = stats2["size"];
		if(fileSizeInBytes1 < 1000 || fileSizeInBytes2 < 1000){
			socket.emit("message","Fichiers de base non créés, veuillez lancer la première partie");
			//console.log("Fichiers non écrits");
			scripting = 0;
			return 0;
		}
		fileattente(["CHA.py", "questionsCaracteristiques.py", "PCA.py"], [nbcluster, nbquestions]);
	}
});
