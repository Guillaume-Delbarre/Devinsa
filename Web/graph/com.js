var socket = io.connect('http://127.0.0.1:8080');
var tabp = [];
var tabq = [];
var questiontitle = "";
var namepers = "";
var table;

$(document).ready(function() {
    table = $('#personnages').DataTable();
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
	var ele = document.getElementsByName('Parametre');
	for(i = 0; i < ele.length; i++) { 
		if(ele[i].checked){
			rqtp = ele[i].value;
			parametre = i+1
		}
	}
	if(rqtp != "" && parametre != null){
		for (let i = 0; i<table.rows().data().length; i++){
			socket.emit('updatesql', ({name: table.rows().data()[i][0], qname: questiontitle, value: table.rows().data()[i][parametre], param: rqtp}));
		}
	}
});



$('#updatesql').click(function () {
	var rqtp = "";
	var rqtv = null;
	var ele = document.getElementsByName('parametre')
	for(i = 0; i < ele.length; i++) { 
		if(ele[i].checked){
			rqtp = ele[i].name
		}
	}
	var val = document.getElementById('Valeur');
	if (val != null && val.value != ""){
		rqtv = parseInt(val.value);
	}
	if(questiontitle != "" && rqtv != null){
		for (let i = 0; i<table.rows('.selected').data().length; i++){
			socket.emit('updatesql', ({name: table.rows('.selected').data()[i][0], qname: questiontitle, value: rqtv, param: rqtp}));
		}
	}
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
			if (nomSelectionne.length != 0){
				socket.emit("getallpersreponses", {qname: questiontitle, names: nomSelectionne});
			}
		}
	});
});

socket.on('message', function(message) {
	alert(message);
});

socket.on('valeursreponses', ({y, n, p}) => {
	var t = $('#personnages').DataTable();
	t.clear().draw();
	t.row.add([namepers,y,n,p]).draw(false);
});
