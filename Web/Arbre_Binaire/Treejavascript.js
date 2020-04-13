questionid_1 = {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true};
questionid_2 = {parent: questionid_1, HTMLclass :'light-green', text: { name: ' Personnages restants : 772 Personnage median :f,Passe-partout', desc : 'Prochaine question : Ton personnage est-il français ?'}, collapsed : true};
questionid_3 = {parent: questionid_2, HTMLclass :'light-green', text: { name: ' Personnages restants : 423 Personnage median :Booba ,Lorenzo', desc : 'Prochaine question : Ton personnage est-il décédé ?'}, collapsed : true};
questionid_259552 = {parent: questionid_2, HTMLclass :'light-red', text: { name: ' Personnages restants : 352 Personnage median :Adam Ondra', desc : 'Prochaine question : Ton personnage est-il américain ?'}, collapsed : true};
questionid_782121 = {parent: questionid_1, HTMLclass :'light-red', text: { name: ' Personnages restants : 466 Personnage median :Aelita Stones ,Alex Vaus (Personnage de serie TV:Orange is the new black)', desc : 'Prochaine question : Ton personnage est-il un personnage de jeu vidéo ?'}, collapsed : true};
questionid_782122 = {parent: questionid_782121, HTMLclass :'light-green', text: { name: ' Personnages restants : 119 Personnage median :Arthas (Roi-Liche de Warcraft),Bart', desc : 'Prochaine question : Ton personnage porte-t-il des chaussures ?'}, collapsed : true};
questionid_1044104 = {parent: questionid_782121, HTMLclass :'light-red', text: { name: ' Personnages restants : 289 Personnage median :Aelita Stones ,Alex Vaus (Personnage de serie TV:Orange is the new black)', desc : 'Prochaine question : Ton personnage a-t-il des cheveux ?'}, collapsed : true};
chart_config = [
{container: '#basic-example',
connectors: { type: 'straight' },
 node: { HTMLclass: 'nodeExample1' },
 animation: { nodeAnimation: "easeOutBounce", nodeSpeed: 700,connectorsAnimation: "bounce", connectorsSpeed: 700 }},
questionid_1,
questionid_2,
questionid_3,
questionid_259552,
questionid_782121,
questionid_782122,
questionid_1044104];