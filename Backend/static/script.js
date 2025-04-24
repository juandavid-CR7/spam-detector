
let ultimoMensaje = '';
let ultimaPrediccion = '';

// region  Clasificar
async function clasificar() {
  const asunto = document.getElementById('asunto').value;
  const dominio = document.getElementById('dominio').value;
  const horaEnvio = document.getElementById('hora').value;
  const nivel = document.getElementById('nivel').value;
  const mensaje = document.getElementById('mensaje').value;

  if (!mensaje.trim()) return alert("Escribe un mensaje primero ");

  const res = await fetch('http://192.168.111.241:5001/clasificar', {  
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
 
// region  Feedback
async function enviarFeedback(correcto) {
  // region Ip Server 1
  await fetch('http://192.168.111.241:5001/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      mensaje: ultimoMensaje,
      prediccion: ultimaPrediccion,
      correcto: correcto
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.estado) {
      document.getElementById('mensaje-feedback').textContent = data.estado;
    } else {
      document.getElementById('mensaje-feedback').textContent = "❌ Hubo un error al guardar el feedback.";
    }
  })
  .catch(error => {
    document.getElementById('mensaje-feedback').textContent = "❌ Error en la conexión";
  });

  document.getElementById('feedback').style.display = "none";
  document.getElementById('mensaje').value = "";
  document.getElementById('resultado').innerHTML = "";
}

// region Guardar Correo
async function guardarCorreo() {
  const contenido = document.getElementById("contenido").value;
  const remitente = document.getElementById("remitente").value;
  const etiqueta = document.getElementById("etiqueta").value;
  const mensajeBox = document.getElementById("mensaje");

  if (!contenido.trim() || !remitente.trim()) {
    mensajeBox.textContent = "❗ Por favor completa todos los campos.";
    mensajeBox.style.color = "red";
    return;
  }
  
  // region Ip Server 2
  const response = await fetch("http://192.168.111.241:5001/agregar_correo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ texto: contenido, etiqueta: etiqueta, remitente: remitente })
  });

  const data = await response.json();

  if (response.ok) {
    mensajeBox.textContent = data.mensaje || "✅ Correo guardado exitosamente.";
    mensajeBox.style.color = "green";
  } else {
    mensajeBox.textContent = data.mensaje || "❌ Error al guardar el correo.";
    mensajeBox.style.color = "red";
  }

  document.getElementById("contenido").value = "";
  document.getElementById("remitente").value = "";
  document.getElementById("etiqueta").value = "spam";
}
