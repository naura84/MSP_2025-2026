CVSS_DATABASE = {
    "CVE-2023-38408": {
        "cvss_score": 9.8,
        "cvss_level": "Critical"
    },
    "CVE-2022-37436": {
        "cvss_score": 7.5,
        "cvss_level": "High"
    },
    "CVE-2021-46850": {
        "cvss_score": 8.6,
        "cvss_level": "High"
    },
    "CVE-2015-1419": {
        "cvss_score": 5.3,
        "cvss_level": "Medium"
    },
    "CVE-2023-22944": {
        "cvss_score": 6.5,
        "cvss_level": "Medium"
    },
    "CVE-2023-2455": {
        "cvss_score": 8.1,
        "cvss_level": "High"
    }
}


def get_cvss_info(cve):
    """
    Retourne les infos CVSS associées à une CVE.
    Si la CVE n'est pas trouvée, retourne un score par défaut.
    """
    return CVSS_DATABASE.get(
        cve,
        {
            "cvss_score": 0.0,
            "cvss_level": "Unknown"
        }
    )