const descriptions = {
    client: "Le client initie la résolution DNSSEC en envoyant une requête au résolveur. Il attend une réponse vérifiée avec des signatures DNSSEC.",
    resolveur: "Le résolveur interroge les serveurs DNS hiérarchiquement, vérifie les signatures à chaque étape, et retourne une réponse sécurisée au client.",
    root: "Ce serveur simule un serveur racine DNS capable de signer les réponses avec une signature DNSSEC. Il extrait le TLD d’un domaine, fournit l’adresse IP du serveur TLD correspondant, puis signe cette information.",
    tld: "Le serveur TLD fournit l’adresse du serveur autoritaire correspondant à un domaine de second niveau, et signe cette information.",
    autoritaire: "Ce serveur détient les enregistrements finaux du domaine (comme les A records) et les signe pour garantir leur authenticité."
};

function extractBaseKey(value) {
    return value.split('.')[0];
}

function loadLog() {
    const selector = document.getElementById("log-selector");
    const component = selector.value;
    const logDisplay = document.getElementById("logContent");
    const descBox = document.getElementById("componentDesc");

    if (!component) {
        logDisplay.textContent = "🕓 En attente d'une sélection...";
        descBox.innerHTML = "";
        return;
    }

    const key = extractBaseKey(component);
    descBox.innerHTML = `
        <div class="info-box">
            <strong>${key.charAt(0).toUpperCase() + key.slice(1)} :</strong><br>
            ${descriptions[key] || "Description indisponible pour ce composant."}
        </div>
    `;
}

function getComponent() {
    return document.getElementById("log-selector").value;
}

function afficherLog() {
    const comp = getComponent();
    const display = document.getElementById("logContent");
    if (!comp) {
        display.textContent = "⚠️ Aucune sélection.";
        return;
    }
    fetch(`/logs/${comp}`)
        .then(res => {
            if (!res.ok) throw new Error("Erreur lors de la récupération des logs.");
            return res.text();
        })
        .then(data => {
            display.textContent = data || "⚠️ Aucun contenu à afficher.";
            display.scrollTop = display.scrollHeight;
        })
        .catch(err => {
            display.textContent = `❌ ${err.message}`;
        });
}

function telechargerLog() {
    const comp = getComponent();
    if (comp) {
        window.location.href = `/logs/${comp}/download`;
    }
}

function viderTousLesLogs() {
    if (confirm("⚠️ Es-tu sûr de vouloir vider tous les logs ?")) {
        fetch('/logs/clear_all', { method: 'POST' })
            .then(res => res.text())
            .then(msg => alert(msg))
            .catch(err => alert("❌ " + err.message));
    }
}
