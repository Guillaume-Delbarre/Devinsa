questionid_1 = {text: { name: 'Ton personnage est-il réel ?' }, collapsed : true};
questionid_2 = {parent: questionid_1,level : green,text: { name: ' Personnages restants : 772  Personnage median :f', desc : 'Prochaine question : Ton personnage est-il français ?'}, collapsed : true};
chart_config = [
{container: '#basic-example',
connectors: { type: 'step' },
 node: { HTMLclass: 'nodeExample1' },
 animation: { nodeAnimation: "easeOutBounce", nodeSpeed: 700,connectorsAnimation: "bounce", connectorsSpeed: 700 }},
questionid_1,
questionid_2,];