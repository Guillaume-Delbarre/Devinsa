function readTextFile(file) {
    var reponse;
    var rawFile = new XMLHttpRequest(); // XMLHttpRequest (often abbreviated as XHR) is a browser object accessible in JavaScript that provides data in XML, JSON, but also HTML format, or even a simple text using HTTP requests.
    rawFile.open("GET", file, false); // open with method GET the file with the link file ,  false (synchronous)
    rawFile.onreadystatechange = function ()

    {
        if(rawFile.readyState === 4) // readyState = 4: request finished and response is ready
        {
            if(rawFile.status === 200) // status 200: "OK"
            {
                reponse = rawFile.responseText
                //  Returns the response data as a string
            }
        }
    }
    rawFile.send(null);
    return reponse;
}

function createArrayLine(text){
    var ArrayLigne = [];
    var compteur = 0;
    ArrayLigne[0] = "";
    for (let i =0; i<text.length; i++){
        ArrayLigne[compteur] = ArrayLigne[compteur] + ArrayLigne[i];
        if(text[i]==";"){
            compteur = compteur + 1;
            ArrayLigne[compteur] = "";

        }
    }

    return ArrayLigne;

}

var Text;
var Tree;

config = {container: '#tree-simple', connectors: {
        type: 'step'
    },
    node: {
        HTMLclass: 'nodeExample1'
    }};
questionid_1 = {text: { name: 'Ton personnage est-il réel ?' }};
questionid_2 = {parent: questionid_1,text: { name: 'Choix : Oui || Titre : Ton personnage est-il français ?' }};
questionid_782121 = {parent: questionid_1,text: { name: 'Choix : Non || Titre : Ton personnage est-il un personnage de jeu vidéo ?' }};
questionid_3 = {parent: questionid_2,text: { name: 'Choix : Oui || Titre : Ton personnage est-il décédé ?' }};
questionid_259552 = {parent: questionid_2,text: { name: 'Choix : Non || Titre : Ton personnage est-il américain ?' }};
questionid_782122 = {parent: questionid_782121,text: { name: 'Choix : Oui || Titre : Ton personnage porte-t-il des chaussures ?' }};
questionid_1044104 = {parent: questionid_782121,text: { name: 'Choix : Non || Titre : Ton personnage a-t-il des cheveux ?' }};
questionid_4 = {parent: questionid_3,text: { name: 'Choix : Oui || Titre : Ton personnage est-il un écrivain ?' }};
questionid_85898 = {parent: questionid_3,text: { name: 'Choix : Non || Titre : Ton personnage a-t-il un rapport avec le milieu du sport ?' }};
questionid_259553 = {parent: questionid_259552,text: { name: 'Choix : Oui || Titre : Ton personnage est-il acteur/actrice ?' }};
questionid_344112 = {parent: questionid_259552,text: { name: 'Choix : Non || Titre : Ton personnage est-il anglais ?' }};
questionid_782123 = {parent: questionid_782122,text: { name: 'Choix : Oui || Titre : Ton personnage possède-t-il des armes ?' }};
questionid_869940 = {parent: questionid_782122,text: { name: 'Choix : Non || Titre : Ton personnage est-il méchant ? ' }};
questionid_1044105 = {parent: questionid_1044104,text: { name: 'Choix : Oui || Titre : Ton personnage est-il un personnage de série télévisée ?' }};
questionid_1132315 = {parent: questionid_1044104,text: { name: 'Choix : Non || Titre : Ton personnage est-il méchant ? ' }};
questionid_5 = {parent: questionid_4,text: { name: 'Choix : Oui || Titre : Ton personnage a-t-il un prénom hors du commun ?' }};
questionid_27267 = {parent: questionid_4,text: { name: 'Choix : Non || Titre : Ton personnage fait-il de la politique ?' }};
questionid_85899 = {parent: questionid_85898,text: { name: 'Choix : Oui || Titre : Ton personnage est-il un footballeur ?' }};
questionid_112048 = {parent: questionid_85898,text: { name: 'Choix : Non || Titre : Ton personnage est-il devenu connu grâce à Internet ?' }};
questionid_259554 = {parent: questionid_259553,text: { name: 'Choix : Oui || Titre : Ton personnage a-t-il plus de 35 ans ?' }};
questionid_286441 = {parent: questionid_259553,text: { name: 'Choix : Non || Titre : Ton personnage est-il musicien ?' }};
questionid_344113 = {parent: questionid_344112,text: { name: 'Choix : Oui || Titre : Ton personnage est-il acteur/actrice ?' }};
questionid_372089 = {parent: questionid_344112,text: { name: 'Choix : Non || Titre : La célébrité de ton personnage est-elle en rapport avec le monde du football ?' }};
questionid_782124 = {parent: questionid_782123,text: { name: 'Choix : Oui || Titre : Ton personnage est-il masculin ?' }};
questionid_811648 = {parent: questionid_782123,text: { name: 'Choix : Non || Titre : Ton personnage a-t-il la peau blanche ?' }};
questionid_869941 = {parent: questionid_869940,text: { name: 'Choix : Oui || Titre : Ton personnage a-t-il la peau blanche ?' }};
questionid_897020 = {parent: questionid_869940,text: { name: 'Choix : Non || Titre : Est-ce que ton personnage est un animal ?' }};
questionid_1044106 = {parent: questionid_1044105,text: { name: 'Choix : Oui || Titre : Ton personnage est-il policier ou détective ?' }};
questionid_1073435 = {parent: questionid_1044105,text: { name: 'Choix : Non || Titre : Ton personnage possède-t-il des armes ?' }};
questionid_1132316 = {parent: questionid_1132315,text: { name: 'Choix : Oui || Titre : Est-ce que ton personnage est un animal ?' }};
questionid_1161678 = {parent: questionid_1132315,text: { name: 'Choix : Non || Titre : Ton personnage porte-t-il des chaussures ?' }};

chart_config = [
    config,
    questionid_1,
    questionid_2,
    questionid_782121,
    questionid_3,
    questionid_259552,
    questionid_782122,
    questionid_1044104
];


Text = readTextFile("TreeJs.txt"); //<= Call function ===== don't need "file:///..." just the path
Tree = createArrayLine(Text);


