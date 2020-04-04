questionid_1 = {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true};
questionid_2 = {parent: questionid_1,text: { name: 'Choix : o', desc : 'Titre : Ton personnage est-il français ? Personnages restants : 772 Personnage median :f'}, collapsed : true};
questionid_3 = {parent: questionid_2,text: { name: 'Choix : o', desc : 'Titre : Ton personnage est-il décédé ? Personnages restants : 423 Personnage median :f'}, collapsed : true};
questionid_259552 = {parent: questionid_2,text: { name: 'Choix : n', desc : 'Titre : Ton personnage est-il américain ? Personnages restants : 352 Personnage median :f'}, collapsed : true};
questionid_782121 = {parent: questionid_1,text: { name: 'Choix : n', desc : 'Titre : Ton personnage est-il un personnage de jeu vidéo ? Personnages restants : 466 Personnage median :Le grand schtroumpf'}, collapsed : true};
questionid_782122 = {parent: questionid_782121,text: { name: 'Choix : o', desc : 'Titre : Ton personnage porte-t-il des chaussures ? Personnages restants : 119 Personnage median :Le grand schtroumpf'}, collapsed : true};
questionid_1044104 = {parent: questionid_782121,text: { name: 'Choix : n', desc : 'Titre : Ton personnage a-t-il des cheveux ? Personnages restants : 289 Personnage median :Akinator'}, collapsed : true};
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