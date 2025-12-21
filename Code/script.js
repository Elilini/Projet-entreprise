let chartLine = null;
let chartScore = null;
let chartBar = null;

async function lancerAnalyse() {
    const siren = document.getElementById("sirenInput").value.trim();
    if(siren.length !== 9) return alert("Le SIREN doit faire 9 chiffres.");

    document.getElementById("loader").classList.remove("hidden");
    document.getElementById("resultats").classList.add("hidden");

    try {
        const res = await fetch(`http://127.0.0.1:8000/diagnostic/${siren}`);
        const data = await res.json();

        // Remplissage des textes
        document.getElementById("titreEntreprise").innerText = data.entreprise || "Entreprise Inconnue";
        document.getElementById("sourceDonnees").innerText = "Source : " + (data.source || "N/A");
       document.getElementById("contenuRapport").innerHTML = data.rapport_ia.texte.replace(/\n/g, '<br>');
        // Remplissage des News
        const ul = document.getElementById("listeNews");
        ul.innerHTML = "";
        (data.news_titres || []).forEach(n => {
            let li = document.createElement("li");
            li.innerText = n;
            ul.appendChild(li);
        });

        // Affichage et Graphiques
        document.getElementById("loader").classList.add("hidden");
        document.getElementById("resultats").classList.remove("hidden");

        if (data.graph) {
            setTimeout(() => updateCharts(data.graph), 300);
        }
    } catch (e) {
        console.error(e);
        alert("Erreur de connexion au serveur.");
        document.getElementById("loader").classList.add("hidden");
    }
}

function updateCharts(graphData) {
    if (typeof Chart === 'undefined') return console.error("Chart.js non chargé");

    // 1. Graphique Projection 2050
    const ctxLine = document.getElementById('graphPrevision').getContext('2d');
    if(chartLine) chartLine.destroy();
    chartLine = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: graphData.labels,
            datasets: [
                { 
                    label: 'Historique', 
                    data: graphData.historique, 
                    borderColor: '#3498db', 
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    fill: true,
                    spanGaps: true 
                },
                { 
                    label: 'Projection 2050', 
                    data: graphData.prevision, 
                    borderColor: '#e74c3c', 
                    borderDash: [5, 5], 
                    fill: false,
                    spanGaps: true 
                }
            ]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: false } }
        }
    });

    // 2. Score de Santé (Doughnut)
    const ctxScore = document.getElementById('graphScore').getContext('2d');
    if(chartScore) chartScore.destroy();
    document.getElementById('scoreValue').innerText = (graphData.score || 70) + "%";
    chartScore = new Chart(ctxScore, {
        type: 'doughnut',
        data: {
            datasets: [{ data: [graphData.score || 70, 100 - (graphData.score || 70)], backgroundColor: ['#2ecc71', '#eee'] }]
        },
        options: { cutout: '80%', maintainAspectRatio: false }
    });

    // 3. Trajectoire Carbone (Barres)
    const ctxBar = document.getElementById('graphPie').getContext('2d'); 
    if (chartBar) chartBar.destroy();
    chartBar = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: graphData.co2_labels || ["2024", "2030", "2040", "2050"],
            datasets: [{
                label: 'Émissions CO2 (Tonnes)',
                data: graphData.co2_data || [100, 70, 40, 5],
                backgroundColor: '#1abc9c'
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } }
        }
    });
}