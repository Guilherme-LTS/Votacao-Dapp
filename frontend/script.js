function votar() {
  const eleitor_id = document.getElementById('eleitor_id').value;
  const candidato = document.getElementById('candidato').value;

  fetch('/votar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ eleitor_id, candidato })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('mensagem').innerText = data.mensagem;
  });
}

function minerar() {
  fetch('/minerar')
    .then(response => response.json())
    .then(data => {
      document.getElementById('mensagem').innerText = data.mensagem;
    });
}

function verResultados() {
  fetch('/resultados')
    .then(response => response.json())
    .then(data => {
      const resultadosDiv = document.getElementById('resultados');
      resultadosDiv.innerHTML = "<h3>Resultados:</h3>";
      for (const [candidato, votos] of Object.entries(data.resultados)) {
        resultadosDiv.innerHTML += `<p>${candidato}: ${votos} voto(s)</p>`;
      }
    });
}

function sincronizar() {
  fetch('/nodes/resolve')
    .then(response => response.json())
    .then(data => {
      document.getElementById('mensagem').innerText = data.mensagem;
    });
}

function registrarNo() {
  const url = document.getElementById('node_url').value;
  if (!url) {
    document.getElementById('mensagem').innerText = "Por favor, insira uma URL válida.";
    return;
  }

  fetch('/nodes/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ nodes: [url] })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('mensagem').innerText = data.mensagem;
    document.getElementById('node_url').value = '';
  })
  .catch(() => {
    document.getElementById('mensagem').innerText = "Erro ao registrar o nó.";
  });
}
