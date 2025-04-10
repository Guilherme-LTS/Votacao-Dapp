const api = 'http://localhost:5000';

async function votar() {
  const eleitor_id = document.getElementById('eleitor_id').value;
  const candidato = document.getElementById('candidato').value;

  const res = await fetch(`${api}/votar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ eleitor_id, candidato })
  });

  const data = await res.json();
  document.getElementById('mensagem').innerText = data.mensagem;
}

async function minerar() {
  const res = await fetch(`${api}/minerar`);
  const data = await res.json();
  alert(data.mensagem);
}

async function verResultados() {
  const res = await fetch(`${api}/resultados`);
  const data = await res.json();

  const resultadosDiv = document.getElementById('resultados');
  resultadosDiv.innerHTML = '<h3>Resultados:</h3>';

  for (const [candidato, votos] of Object.entries(data.resultados)) {
    resultadosDiv.innerHTML += `<p>${candidato}: ${votos} voto(s)</p>`;
  }
}
