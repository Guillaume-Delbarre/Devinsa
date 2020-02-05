questionid_1 = {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true};
questionid_2 = {parent: questionid_1,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il français ?' }, collapsed : true};
questionid_782121 = {parent: questionid_1,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage est-il un personnage de jeu vidéo ?' }, collapsed : true};
questionid_3 = {parent: questionid_2,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il décédé ?' }, collapsed : true};
questionid_259552 = {parent: questionid_2,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage est-il américain ?' }, collapsed : true};
questionid_782122 = {parent: questionid_782121,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage porte-t-il des chaussures ?' }, collapsed : true};
questionid_1044104 = {parent: questionid_782121,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage a-t-il des cheveux ?' }, collapsed : true};
questionid_4 = {parent: questionid_3,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il un écrivain ?' }, collapsed : true};
questionid_85898 = {parent: questionid_3,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage a-t-il un rapport avec le milieu du sport ?' }, collapsed : true};
questionid_259553 = {parent: questionid_259552,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il acteur/actrice ?' }, collapsed : true};
questionid_344112 = {parent: questionid_259552,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage est-il anglais ?' }, collapsed : true};
questionid_782123 = {parent: questionid_782122,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage possède-t-il des armes ?' }, collapsed : true};
questionid_869940 = {parent: questionid_782122,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage est-il méchant ? ' }, collapsed : true};
questionid_1044105 = {parent: questionid_1044104,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il un personnage de série télévisée ?' }, collapsed : true};
questionid_1132315 = {parent: questionid_1044104,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage est-il méchant ? ' }, collapsed : true};
questionid_5 = {parent: questionid_4,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage a-t-il un prénom hors du commun ?' }, collapsed : true};
questionid_27267 = {parent: questionid_4,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage fait-il de la politique ?' }, collapsed : true};
questionid_85899 = {parent: questionid_85898,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il un footballeur ?' }, collapsed : true};
questionid_112048 = {parent: questionid_85898,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage est-il devenu connu grâce à Internet ?' }, collapsed : true};
questionid_259554 = {parent: questionid_259553,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage a-t-il plus de 35 ans ?' }, collapsed : true};
questionid_286441 = {parent: questionid_259553,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage est-il musicien ?' }, collapsed : true};
questionid_344113 = {parent: questionid_344112,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il acteur/actrice ?' }, collapsed : true};
questionid_372089 = {parent: questionid_344112,text: { name: 'Choix : Non', desc : 'Titre : La célébrité de ton personnage est-elle en rapport avec le monde du football ?' }, collapsed : true};
questionid_782124 = {parent: questionid_782123,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il masculin ?' }, collapsed : true};
questionid_811648 = {parent: questionid_782123,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage a-t-il la peau blanche ?' }, collapsed : true};
questionid_869941 = {parent: questionid_869940,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage a-t-il la peau blanche ?' }, collapsed : true};
questionid_897020 = {parent: questionid_869940,text: { name: 'Choix : Non', desc : 'Titre : Est-ce que ton personnage est un animal ?' }, collapsed : true};
questionid_1044106 = {parent: questionid_1044105,text: { name: 'Choix : Oui', desc : 'Titre : Ton personnage est-il policier ou détective ?' }, collapsed : true};
questionid_1073435 = {parent: questionid_1044105,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage possède-t-il des armes ?' }, collapsed : true};
questionid_1132316 = {parent: questionid_1132315,text: { name: 'Choix : Oui', desc : 'Titre : Est-ce que ton personnage est un animal ?' }, collapsed : true};
questionid_1161678 = {parent: questionid_1132315,text: { name: 'Choix : Non', desc : 'Titre : Ton personnage porte-t-il des chaussures ?' }, collapsed : true};
chart_config = [
{container: '#basic-example',
connectors: { type: 'step' },
 node: { HTMLclass: 'nodeExample1' },
 animation: { nodeAnimation: "easeOutBounce", nodeSpeed: 700,connectorsAnimation: "bounce", connectorsSpeed: 700 }},
 questionid_1,questionid_2,
questionid_782121,
questionid_3,
questionid_259552,
questionid_782122,
questionid_1044104,
questionid_4,
questionid_85898,
questionid_259553,
questionid_344112,
questionid_782123,
questionid_869940,
questionid_1044105,
questionid_1132315,
questionid_5,
questionid_27267,
questionid_85899,
questionid_112048,
questionid_259554,
questionid_286441,
questionid_344113,
questionid_372089,
questionid_782124,
questionid_811648,
questionid_869941,
questionid_897020,
questionid_1044106,
questionid_1073435,
questionid_1132316,
questionid_1161678];