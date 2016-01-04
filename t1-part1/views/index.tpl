<html>

<head></head>

<body>

<h1> T1.p1: Chat de texto </h1>
<ul>
%for (n, m) in messages:
    <li> <b>{{n}}: </b> {{m}} </li>
%end
</ul>

<form action="/send" method=POST>
    <p> Nick <input name="nick" type="text" value="{{nick}}"/> </p>
    <p> Mensagem <input name="message" type="text" /> </p>
    <p> <input value="Enviar" type="submit" /> </p>
</form>

</body>

</html>
