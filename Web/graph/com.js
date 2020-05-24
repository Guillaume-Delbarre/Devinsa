var socket = io.connect('http://127.0.0.1:8080');
var tabp = [];
var tabq = [];
var questiontitle = "";
var namepers = "";
var table;

$(document).ready(function() {
    table = $('#personnages').DataTable( {
		dom: 'Bfrtip',
		buttons: [
			'selectAll',
			'selectNone'
		],
		language: {
			buttons: {
				selectAll: "Select all items",
				selectNone: "Select none"
			}
		}
	});
	$(".selectAll").on( "click", function(e) {
    if ($(this).is(":checked" )) {
        table.rows().select();        
    } else {
        table.rows().deselect(); 
    }
	});
	// La ligne de la table est selectionnée on click
	$('#personnages').on('click', 'tr', function () {
		$(this).toggleClass('selected');
    });
});

socket.on('getallpersreponse', function(pers) {
	tabp = pers;
});

socket.on('getallquesreponse', function(ques) {
	tabq = ques;
});

socket.on("refresh", function() {
	location.reload(true);
});

socket.on('getallparamreponse', function(tabreponse) {
	var t = $('#personnages').DataTable();
	t.clear().draw();
	for(let i = 0; i<tabreponse.length; i++){
		t.row.add([tabreponse[i].nom, tabreponse[i].y, tabreponse[i].n, tabreponse[i].p]).draw(false);
	}
});

$('#vctsql').click(function () {
	socket.emit('ecrirevecteursql');
});

$('#toutlancer').click(function () {
	var nbcluster = parseInt(prompt('Nombre de clusters'));
	var nbquestions = parseInt(prompt('Nombre de questions'));
	socket.emit('toutlancer', ({nbcluster: nbcluster, nbquestions: nbquestions}));
});

$('#lancer2emepartie').click(function () {
	var nbcluster = parseInt(prompt('Nombre de clusters'));
	var nbquestions = parseInt(prompt('Nombre de questions'));
	socket.emit('lancerdeuxièmepartie', ({nbcluster: nbcluster, nbquestions: nbquestions}));
});

$('#increment').click(function () {
	var rqtp = "";
	var parametre = null;
	//On stock le parametre choisi par l'utilisateur
	var ele = document.getElementsByName('Parametre');
	for(i = 0; i < ele.length; i++) { 
		if(ele[i].checked){
			rqtp = ele[i].value;
			parametre = i+1
		}	
	}
	//On incrémente chaque ligne présente dans la table
	if(rqtp != "" && parametre != null){
		//alert(questiontitle);
		for (let i = 0; i<table.rows('.selected').data().length; i++){
			socket.emit('updatesql', ({name: table.rows('.selected').data()[i][0], qname: questiontitle, value: table.rows('.selected').data()[i][parametre]+1, param: rqtp}));
		}
	}
	setTimeout(() => {if (selection1 != []){
			socket.emit("getallpersreponses", {qname: questiontitle, names: selection1});
	}}, 500);

});

$('#updatesql').click(function () {
	alert("ici");
	var rqtp = "";
	var rqtv = null;
	//On garde le parametre choisi du bouton Parametre 
	var ele = document.getElementsByName('Parametre');
	for(i = 0; i < ele.length; i++) { 
		if(ele[i].checked){
			rqtp = ele[i].value;
		}
	}
	//On garde la valeur du bouton Valeur
	var val = document.getElementById('Valeur');
	if (val != null && val.value != ""){
		rqtv = parseInt(val.value);
	}
	//On emet une requete update pour chaque ligne selectionnée aux parametres stockés precedemment dans la fonction
	if(questiontitle != "" && rqtv != null){
		for (let i = 0; i<table.rows('.selected').data().length; i++){
			socket.emit('updatesql', ({name: table.rows('.selected').data()[i][0], qname: questiontitle, value: rqtv, param: rqtp}));
		}
	}
	if (selection1 != []){
			socket.emit("getallpersreponses", {qname: questiontitle, names: selection1});
	}
});

$('#Selectall').click(function () {
	table.rows().select();
});

$('#creerarbre').click(function () {
	var prof = parseInt(prompt("Profondeur de l'arbre ?")); //ICI ON PROMPT LES PARAM DU CHANGEMENT A FAIRE
	socket.emit('creerarbre', {profondeur :prof}); // ON ENVOIE L'EVENT AU SERVEUR
});
	// Case avec autocompletion pour trouver plus facilement les personnages

$( function() {
	$( "#tags" ).autocomplete({
		source: function(request, response) {
			var results = $.ui.autocomplete.filter(tabp, request.term);
			response(results.slice(0, 5));
		},
		select : function(event, ui){
			namepers = ui.item.value ; // On stock la valeur dans le param
			if (questiontitle != ""){
				//socket.emit("getvaleursreponse", {qname: questiontitle, name: namepers});
			}
		}
	});
});

// Case avec autocompletion pour trouver plus facilement les questions
$( function() {
	$( "#tags1" ).autocomplete({
		source: function(request, response) {
			var results = $.ui.autocomplete.filter(tabq, request.term);
				response(results.slice(0, 5));
		},
		select : function(event, ui){
			questiontitle = ui.item.value ; // On stock la valeur dans le param
			if (selection1.length != 0){
				socket.emit("getallpersreponses", {qname: questiontitle, names: selection1});
			}
		}
	});
});

socket.on('message', function(message) {
	alert(message);
});

socket.on('valeursreponses', ({y, n, p}) => {
	table.clear().draw();
	//On ajoute à la table les lignes de valeurs
	table.row.add([namepers,y,n,p]).draw(false);
});
