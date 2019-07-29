const express = require('express');
const server = express();
const bodyParser = require('body-parser');
const axios = require('axios');

const port = 8555;
const apiUrl = 'http://localhost:5001';


server.use(express.urlencoded({ extended: false }));
server.use(express.json());
server.use(bodyParser.json());
server.use(bodyParser.urlencoded({ extended: false }));
server.use('/static', express.static('static'));
server.use('/templates', express.static('templates'));

server.get('/', function (request, response) {
    response.sendfile('index.html');
});
server.get('/chatroom', function (request, response) {
    response.sendfile('chatroom.html');
});
server.get('/settings', function (request, response) {
    response.sendfile('settings.html');
});
server.get('/connexion', function (request, response) {
    response.sendfile('connexion.html');
});
server.get('/sinscrire', function (request, response){
    response.sendfile('sinscrire.html');
});
server.get('/erreur', function (request, response) {
    response.sendfile('erreur.html');
});
server.get('/deconnexion', function (request, response) {
    response.sendfile('deconnexion.html');
});


server.post('/sinscrire', function (request, response) {
    console.log (request.body);
    axios.post(apiUrl + '/sinscrire', request.body)
        .then
            response.end()
            console.log('ça marche');

});


server.use(function (request, response, next) {
    response.setHeader('Content-Type', 'text/plain; charset=UTF-8');
    response.status(404).send('Page introuvable');
})

server.listen(port, function () {
    console.log('Le serveur fonctionne sur le port ' + port);
});