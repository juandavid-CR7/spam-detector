let ultimoMensaje = '';
let ultimaPrediccion = '';

async function clasificar() {
  const asunto = document.getElementById('asunto').value;
  const dominio = document.getElementById('dominio').value;
  const horaEnvio = document.getElementById('hora').value;
  const nivel = document.getElementById('nivel').value;
  const mensaje = document.getElementById('mensaje').value;

  if (!mensaje.trim()) return alert("Escribe un mensaje primero ");

  const res = await fetch('http://192.168.100.37:5001/clasificar', {  // Cambié localhost:5000 por 192.168.100.37:5001
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mensaje, asunto, dominio, horaEnvio, nivel })
  });

  const data = await res.json();

  let html = `<strong>Resultado:</strong> ${data.resultado}<br>`;
  html += `<strong>Palabras clave:</strong> ${data.palabras_clave.join(', ')}<br>`;

  if (data.razones && data.razones.length > 0) {
    html += `<strong>Factores detectados:</strong><ul>`;
    data.razones.forEach(r => {
      html += `<li>${r}</li>`;
    });
    html += `</ul>`;
  } else {
    html += `<em>No se detectaron factores de spam adicionales.</em>`;
  }

  document.getElementById('resultado').innerHTML = html;
  document.getElementById('feedback').style.display = "block";
  document.getElementById('mensaje-feedback').textContent = "";

  ultimoMensaje = mensaje;
  ultimaPrediccion = data.prediccion;
}

async function enviarFeedback(correcto) {
  await fetch('http://192.168.100.37:5001/feedback', {  // Cambié localhost:5000 por 192.168.100.37:5001
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      mensaje: ultimoMensaje,
      prediccion: ultimaPrediccion,
      correcto: correcto
    })
  });

  document.getElementById('mensaje-feedback').textContent = "✅ ¡Gracias por tu feedback!";
  document.getElementById('feedback').style.display = "none";
  document.getElementById('mensaje').value = "";
  document.getElementById('resultado').innerHTML = "";
}
