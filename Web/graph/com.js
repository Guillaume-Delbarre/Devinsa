			var socket = io.connect('http://92.94.210.93:8080');
			var tabp = [];
			var tabq = [];
			var questiontitle = "";
			var namepers = "";
			var arrayreponses = [];
			
			socket.on('getallpersreponse', function(pers) {
				tabp = pers;
			});
			
			socket.on('getallquesreponse', function(ques) {
				tabq = ques;
			});
			
			socket.on('getallparamreponse', function(tabreponse) {
			});
					
			$('#vctsql').click(function () {
				socket.emit('ecrirevecteursql');
			});
						
			$('#updatesql').click(function () {
				var rqtp = parseInt(prompt('Paramètre à changer ?')); //ICI ON PROMPT LES PARAM DU CHANGEMENT A FAIRE
				var rqtv = parseInt(prompt('Valeur à mettre ?')); //ICI ON PROMPT LES PARAM DU CHANGEMENT A FAIRE	
					
				socket.emit('updatesql', {name :namepers, qname : questiontitle, value: rqtv, param : rqtp}); // ON ENVOIE L'EVENT AU SERVEUR

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
							socket.emit("getvaleursreponse", {qname: questiontitle, name: namepers});
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
						if (namepers != ""){
							socket.emit("getvaleursreponse", {qname: questiontitle, name: namepers});
						}
					}
				});
			});
			
			socket.on('message', function(message) {
				alert(message);
			});
			
			socket.on('valeursreponses', ({y, n, p}) => {	
				var Table = document.getElementById('valeurreponses');
				Table.rows[1].cells[0].innerHTML = y;
				Table.rows[1].cells[1].innerHTML = n;
				Table.rows[1].cells[2].innerHTML = p;
			});