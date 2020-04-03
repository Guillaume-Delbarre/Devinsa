questionid_1 = {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true};
questionid_1 = {parent: questionid_None,text: { name: 'Choix : r', desc : 'Titre : Ton personnage est-il réel ? Personnages restants : 2182 Personnage median : Samir Loussif '}, collapsed : true};
questionid_2 = {parent: questionid_1,text: { name: 'Choix : o', desc : 'Titre : Ton personnage est-il français ? Personnages restants : 1416 Personnage median : Samir Loussif '}, collapsed : true};
questionid_3 = {parent: questionid_2,text: { name: 'Choix : o', desc : 'Titre : Ton personnage est-il décédé ? Personnages restants : 1409 Personnage median : Samir Loussif '}, collapsed : true};
questionid_259552 = {parent: questionid_2,text: { name: 'Choix : n', desc : 'Titre : Ton personnage est-il américain ? Personnages restants : 1364 Personnage median : Samir Loussif '}, collapsed : true};
questionid_782121 = {parent: questionid_1,text: { name: 'Choix : n', desc : 'Titre : Ton personnage est-il un personnage de jeu vidéo ? Personnages restants : 1722 Personnage median : Skelita Calaveras '}, collapsed : true};
questionid_782122 = {parent: questionid_782121,text: { name: 'Choix : o', desc : 'Titre : Ton personnage porte-t-il des chaussures ? Personnages restants : 1718 Personnage median : Skelita Calaveras '}, collapsed : true};
questionid_1044104 = {parent: questionid_782121,text: { name: 'Choix : n', desc : 'Titre : Ton personnage a-t-il des cheveux ? Personnages restants : 1629 Personnage median : Skelita Calaveras '}, collapsed : true};
chart_config = [
{container: '#basic-example',
connectors: { type: 'step' },
 node: { HTMLclass: 'nodeExample1' },
 animation: { nodeAnimation: "easeOutBounce", nodeSpeed: 700,connectorsAnimation: "bounce", connectorsSpeed: 700 }},
questionid_1,
questionid_2,
questionid_3,
questionid_259552,
questionid_782121,
questionid_782122,
questionid_1044104];