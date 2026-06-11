from ddgs import DDGS
from urllib.parse import urlparse

# Fontes aceitas
TRUSTED_DOMAINS = [
    "aosfatos.org",
    "lupa.uol.com.br",
    "projetocomprova.com.br",
    "g1.globo.com",
    "bbc.com",
    "bbc.co.uk",
    "gov.br",
    "reuters.com",
    "apnews.com",
    "cnn.com",
    "cnnbrasil.com.br",
    "uol.com.br",
    "folha.uol.com.br",
    "estadao.com.br",
    "tecmundo.com.br",
    "super.abril.com.br",
]

# Sites proibidos
BLOCKED_DOMAINS = [
    "academia.edu",
    "wiktionary.org",
    "dicio.com.br",
    "michaelis.uol.com.br",
    "significados.com.br",
    "sinonimos.com.br",
]


def search_sources(text):

    query = text

    sources = []
    urls_adicionadas = set()

    try:

        with DDGS() as ddgs:

            results = ddgs.text(
                query,
                max_results=20
            )

            for result in results:

                title = result.get("title", "")
                url = result.get("href", "")

                domain = urlparse(url).netloc.lower()

                # ignora domínios proibidos
                if any(blocked in domain for blocked in BLOCKED_DOMAINS):
                    continue

                # aceita apenas domínios confiáveis
                if not any(trusted in domain for trusted in TRUSTED_DOMAINS):
                    continue

                # evita duplicados
                if url in urls_adicionadas:
                    continue

                urls_adicionadas.add(url)

                sources.append(
                    {
                        "titulo": title,
                        "url": url
                    }
                )

                # limita a 5 resultados finais
                if len(sources) >= 5:
                    break

    except Exception as e:

        print("Erro na busca:", e)

    return sources