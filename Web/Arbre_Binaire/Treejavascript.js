questionid_1 = {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true};
questionid_2 = {parent: questionid_1, HTMLclass :'light-green', text: { name: ' Personnages restants : 772 Personnage median :123,aa,Abdülhamid II (sultan ottoman)', desc : 'Prochaine question : Ton personnage est-il français ?'}, collapsed : true};
questionid_3 = {parent: questionid_2, HTMLclass :'light-green', text: { name: ' Personnages restants : 423 Personnage median :123,aa,Abel Jabri', desc : 'Prochaine question : Ton personnage est-il décédé ?'}, collapsed : true};
questionid_259552 = {parent: questionid_2, HTMLclass :'light-red', text: { name: ' Personnages restants : 352 Personnage median :Abdülhamid II (sultan ottoman),Abdümalid 2 le Pieu, Sultan de l\'Empire Ottoman,Abe Shinzo ', desc : 'Prochaine question : Ton personnage est-il américain ?'}, collapsed : true};
questionid_782121 = {parent: questionid_1, HTMLclass :'light-red', text: { name: ' Personnages restants : 466 Personnage median :	Onyx , zero (personnage de jeu),aa', desc : 'Prochaine question : Ton personnage est-il un personnage de jeu vidéo ?'}, collapsed : true};
questionid_782122 = {parent: questionid_782121, HTMLclass :'light-green', text: { name: ' Personnages restants : 119 Personnage median : zero (personnage de jeu),Adibou,Agent 47', desc : 'Prochaine question : Ton personnage porte-t-il des chaussures ?'}, collapsed : true};
questionid_1044104 = {parent: questionid_782121, HTMLclass :'light-red', text: { name: ' Personnages restants : 289 Personnage median :Abraracourcix,Aelita Stones ,Akinator', desc : 'Prochaine question : Ton personnage a-t-il des cheveux ?'}, collapsed : true};
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