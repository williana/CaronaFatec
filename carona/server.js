var express = require('express');
var app = express();

app.set('views', __dirname + '/views');

app.use("/static", express.static(__dirname + '/static'));

//Página Inicial
app.get('/', function(req, res){
	res.render('index.jade',
		{
			title: 'Carona Fatec',
			users: ['user1', 'user2', 'user3'],
			user: {name: 'Marcelo'}
		});
});

var port = process.env.PORT || 5000;
server = app.listen(port);

console.log('Server listening on port %d in %s mode', server.address().port, app.settings.env);