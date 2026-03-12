import csv
import json
from pathlib import Path


DATA_DIR = Path("dados")
OUTPUT_FILE = "atuacao.json"


def read_csv(filename):
    path = DATA_DIR / filename
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_coeficientes(rows):
    result = {}
    for r in rows:
        nome = r["coeficiente"].strip().lower()
        peso = float(r["peso"])
        result[nome] = peso
    return result


def parse_regras(rows):
    result = {}

    for r in rows:
        regra = r["regra"].strip().lower().replace(" ", "_")
        valor = r["valor"]
        prioridade = int(r["prioridade"])

        if valor.lower() == "true":
            valor = True
        elif valor.lower() == "false":
            valor = False
        else:
            try:
                valor = int(valor)
            except:
                pass

        result[regra] = {
            "valor": valor,
            "prioridade": prioridade
        }

    return result

def parse_musicos(rows):
    musicos = []
    for r in rows:
        musicos.append({
            "id": r["id"],
            "genero": r["genero"],
            "vocal_min": r["vocal_min"],
            "vocal_max": r["vocal_max"],
            "classificacao_vocal": r["classificacao_vocal"],
            "volume_voz_db": float(r["volume_voz_db"].replace(",", ".").replace("\"", "")),
            "instrumento": r["instrumento"],
            "vol_inst_dedilhado_db": float(r["vol_inst_dedilhado_db"].replace(",", ".").replace("\"", "")),
            "vol_inst_corrido_db": float(r["vol_inst_corrido_db"].replace(",", ".").replace("\"", "")),
            "hierarquia": r["hierarquia"]
        })
    return musicos

def parse_instrumentos(rows):
    instrumentos = []
    for r in rows:
        instrumentos.append({
            "nome": r["nome"],
            "tipo": r["tipo"],
            "direcionalidade": r["direcionalidade"],
            "tamanho": r["tamanho"],
            "posicao": r["posicao"],
            "vol_medio_dedilhado_db": float(r["vol_medio_dedilhado_db"].replace(",", ".").replace("\"", "")),
            "vol_medio_corrido_db": float(r["vol_medio_corrido_db"].replace(",", ".").replace("\"", ""))
        })
    return instrumentos


def main():

    coeficientes_rows = read_csv("Dados RaussTuna - Acustica.csv")
    regras_rows = read_csv("Dados RaussTuna - Tradicoes.csv")
    musicos_rows = read_csv("Dados RaussTuna - MusicosPresentes.csv")
    instrumentos_rows = read_csv("Dados RaussTuna - InstrumentosPresentes.csv")

    atuacao = {
        "coeficientes": parse_coeficientes(coeficientes_rows),
        "regras": parse_regras(regras_rows),
        "musicos": parse_musicos(musicos_rows),
        "instrumentos": parse_instrumentos(instrumentos_rows)
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(atuacao, f, indent=2, ensure_ascii=False)

    print(f"Arquivo {OUTPUT_FILE} gerado com sucesso.")


if __name__ == "__main__":
    main()