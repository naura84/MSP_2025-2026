import requests
import json
from core.logger import get_logger

logger = get_logger("ai")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def generate_recommendations(scan_result):
    """Génère un résumé + des recommandations à partir d'un résultat de scan."""

    # On ne transmet que les faits issus du scan
    services = scan_result.get("services_found", [])
    vulns = scan_result.get("vulnerabilities", [])

    facts = {
        "host": scan_result.get("host"),
        "risk_score": scan_result.get("risk_score"),
        "risk_level": scan_result.get("risk_level"),
        "open_ports": [
            {"port": s["port"], "service": s.get("service")}
            for s in services if s.get("state") == "open"
        ],
        "vulnerabilities": [
            {
                "service": v.get("service"),
                "cve": v.get("vulnerability", {}).get("cve"),
                "severity": v.get("vulnerability", {}).get("severity"),
                "cvss": v.get("vulnerability", {}).get("cvss_score"),
                "description": v.get("vulnerability", {}).get("description"),
            }
            for v in vulns
        ],
    }

    prompt = f"""Tu es un expert en cybersécurité. Voici les résultats FACTUELS d'un scan de sécurité.
N'invente aucune vulnérabilité ni CVE : appuie-toi UNIQUEMENT sur les données fournies.

Données du scan :
{json.dumps(facts, indent=2, ensure_ascii=False)}

Rédige en français, de façon claire et concise :
1. Un résumé en 2-3 phrases compréhensible par un non-technicien.
2. Une liste de recommandations concrètes, classées de la plus urgente à la moins urgente.

Réponds directement, sans préambule."""

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 400}
        }, timeout=300)
        response.raise_for_status()
        text = response.json().get("response", "").strip()
        logger.info(f"AI recommendations generated for {facts['host']}")
        return {"recommendations": text}
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        return {"error": "Recommandations indisponibles pour le moment."}