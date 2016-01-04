<ul>
%for mi in m:
    <li> {{mi}} </li>
%end
</ul>

<form action="/send" method=POST>
    <p> Nick <input name="nick" type="text" /> </p>
    <p> Mensagem <input name="message" type="text" /> </p>
    <p> <input value="Enviar" type="submit" /> </p>
</form>


