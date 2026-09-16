import random
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional

app = FastAPI(title="The Extreme GOAT")
templates = Jinja2Templates(directory="templates")

# 38 Jogadores para o Roubo de DNA
JOGADORES = [
    {"nome": "Michael Jordan", "time": "Bulls", "stats": {"arremesso": 93, "playmaking": 88, "defesa": 98, "rebotes": 80, "fisico": 97, "clutch": 99}},
    {"nome": "LeBron James", "time": "Lakers", "stats": {"arremesso": 86, "playmaking": 97, "defesa": 92, "rebotes": 88, "fisico": 99, "clutch": 95}},
    {"nome": "Stephen Curry", "time": "Warriors", "stats": {"arremesso": 99, "playmaking": 91, "defesa": 72, "rebotes": 65, "fisico": 79, "clutch": 96}},
    {"nome": "Kobe Bryant", "time": "Lakers", "stats": {"arremesso": 92, "playmaking": 85, "defesa": 95, "rebotes": 78, "fisico": 92, "clutch": 99}},
    {"nome": "Shaquille O'Neal", "time": "Lakers", "stats": {"arremesso": 45, "playmaking": 70, "defesa": 93, "rebotes": 97, "fisico": 99, "clutch": 90}},
    {"nome": "Dennis Rodman", "time": "Bulls", "stats": {"arremesso": 40, "playmaking": 65, "defesa": 98, "rebotes": 99, "fisico": 93, "clutch": 85}},
    {"nome": "Magic Johnson", "time": "Lakers", "stats": {"arremesso": 82, "playmaking": 99, "defesa": 82, "rebotes": 85, "fisico": 88, "clutch": 94}},
    {"nome": "Larry Bird", "time": "Celtics", "stats": {"arremesso": 96, "playmaking": 94, "defesa": 84, "rebotes": 89, "fisico": 78, "clutch": 98}},
    {"nome": "Hakeem Olajuwon", "time": "Rockets", "stats": {"arremesso": 80, "playmaking": 75, "defesa": 99, "rebotes": 96, "fisico": 95, "clutch": 93}},
    {"nome": "Wilt Chamberlain", "time": "Warriors", "stats": {"arremesso": 60, "playmaking": 78, "defesa": 96, "rebotes": 99, "fisico": 99, "clutch": 88}},
    {"nome": "Bill Russell", "time": "Celtics", "stats": {"arremesso": 55, "playmaking": 80, "defesa": 99, "rebotes": 98, "fisico": 94, "clutch": 97}},
    {"nome": "Kevin Durant", "time": "Suns", "stats": {"arremesso": 97, "playmaking": 86, "defesa": 85, "rebotes": 82, "fisico": 89, "clutch": 94}},
    {"nome": "Nikola Jokic", "time": "Nuggets", "stats": {"arremesso": 90, "playmaking": 99, "defesa": 76, "rebotes": 95, "fisico": 85, "clutch": 95}},
    {"nome": "Giannis Antetokounmpo", "time": "Bucks", "stats": {"arremesso": 72, "playmaking": 84, "defesa": 97, "rebotes": 94, "fisico": 99, "clutch": 91}},
    {"nome": "Kawhi Leonard", "time": "Clippers", "stats": {"arremesso": 90, "playmaking": 80, "defesa": 98, "rebotes": 82, "fisico": 90, "clutch": 96}},
    {"nome": "Tim Duncan", "time": "Spurs", "stats": {"arremesso": 84, "playmaking": 82, "defesa": 97, "rebotes": 96, "fisico": 90, "clutch": 94}},
    {"nome": "Allen Iverson", "time": "76ers", "stats": {"arremesso": 88, "playmaking": 86, "defesa": 83, "rebotes": 55, "fisico": 88, "clutch": 93}},
    {"nome": "Dwyane Wade", "time": "Heat", "stats": {"arremesso": 82, "playmaking": 88, "defesa": 92, "rebotes": 72, "fisico": 94, "clutch": 95}},
    {"nome": "Kevin Garnett", "time": "Celtics", "stats": {"arremesso": 84, "playmaking": 83, "defesa": 98, "rebotes": 95, "fisico": 93, "clutch": 92}},
    {"nome": "Dirk Nowitzki", "time": "Mavericks", "stats": {"arremesso": 95, "playmaking": 76, "defesa": 74, "rebotes": 88, "fisico": 82, "clutch": 95}},
    {"nome": "Steve Nash", "time": "Suns", "stats": {"arremesso": 93, "playmaking": 98, "defesa": 65, "rebotes": 52, "fisico": 74, "clutch": 89}},
    {"nome": "John Stockton", "time": "Jazz", "stats": {"arremesso": 85, "playmaking": 99, "defesa": 92, "rebotes": 60, "fisico": 78, "clutch": 90}},
    {"nome": "Luka Doncic", "time": "Mavericks", "stats": {"arremesso": 91, "playmaking": 97, "defesa": 73, "rebotes": 87, "fisico": 84, "clutch": 96}},
    {"nome": "Damian Lillard", "time": "Bucks", "stats": {"arremesso": 94, "playmaking": 88, "defesa": 68, "rebotes": 62, "fisico": 82, "clutch": 98}},
    {"nome": "Kyrie Irving", "time": "Mavericks", "stats": {"arremesso": 94, "playmaking": 90, "defesa": 72, "rebotes": 60, "fisico": 83, "clutch": 97}},
    {"nome": "Russell Westbrook", "time": "Clippers", "stats": {"arremesso": 74, "playmaking": 88, "defesa": 80, "rebotes": 88, "fisico": 96, "clutch": 81}},
    {"nome": "James Harden", "time": "Clippers", "stats": {"arremesso": 92, "playmaking": 94, "defesa": 70, "rebotes": 75, "fisico": 85, "clutch": 82}},
    {"nome": "Jimmy Butler", "time": "Heat", "stats": {"arremesso": 84, "playmaking": 84, "defesa": 93, "rebotes": 79, "fisico": 88, "clutch": 96}},
    {"nome": "Joel Embiid", "time": "76ers", "stats": {"arremesso": 89, "playmaking": 78, "defesa": 92, "rebotes": 94, "fisico": 95, "clutch": 87}},
    {"nome": "Victor Wembanyama", "time": "Spurs", "stats": {"arremesso": 85, "playmaking": 79, "defesa": 97, "rebotes": 93, "fisico": 90, "clutch": 88}},
    {"nome": "Oscar Schmidt", "time": "Brasil", "stats": {"arremesso": 98, "playmaking": 75, "defesa": 65, "rebotes": 72, "fisico": 80, "clutch": 97}},
    {"nome": "Klay Thompson", "time": "Mavericks", "stats": {"arremesso": 95, "playmaking": 70, "defesa": 87, "rebotes": 64, "fisico": 80, "clutch": 92}},
    {"nome": "Draymond Green", "time": "Warriors", "stats": {"arremesso": 68, "playmaking": 90, "defesa": 96, "rebotes": 86, "fisico": 86, "clutch": 85}},
    {"nome": "Ray Allen", "time": "Heat", "stats": {"arremesso": 97, "playmaking": 78, "defesa": 79, "rebotes": 65, "fisico": 82, "clutch": 96}},
    {"nome": "Rudy Gobert", "time": "Timberwolves", "stats": {"arremesso": 42, "playmaking": 58, "defesa": 96, "rebotes": 95, "fisico": 91, "clutch": 65}},
    {"nome": "Trae Young", "time": "Hawks", "stats": {"arremesso": 91, "playmaking": 93, "defesa": 52, "rebotes": 50, "fisico": 70, "clutch": 88}},
    {"nome": "Kyle Kuzma", "time": "Wizards", "stats": {"arremesso": 78, "playmaking": 72, "defesa": 71, "rebotes": 76, "fisico": 80, "clutch": 68}},
    {"nome": "Ben Simmons", "time": "Nets", "stats": {"arremesso": 40, "playmaking": 88, "defesa": 92, "rebotes": 86, "fisico": 91, "clutch": 45}},
]

TODAS_FRANQUIAS = [
    {"nome": "Los Angeles Lakers", "status": "Contender", "logo": "🟡🟣"},
    {"nome": "Boston Celtics", "status": "Contender", "logo": "🟢⚪"},
    {"nome": "Golden State Warriors", "status": "Playoffs", "logo": "🔵🟡"},
    {"nome": "Miami Heat", "status": "Cultura Playoff", "logo": "🔴⚪"},
    {"nome": "Chicago Bulls", "status": "Em Reconstrução", "logo": "🔴⚫"},
    {"nome": "San Antonio Spurs", "status": "Jovem Promissor", "logo": "⚪⚫"},
    {"nome": "New York Knicks", "status": "Contender", "logo": "🟠🔵"},
    {"nome": "Dallas Mavericks", "status": "Contender", "logo": "🔵⚪"},
    {"nome": "Denver Nuggets", "status": "Contender", "logo": "🟡🔵"},
    {"nome": "Phoenix Suns", "status": "Supertime", "logo": "🟣🟠"},
    {"nome": "Milwaukee Bucks", "status": "Contender", "logo": "🟢🦌"}
]

class SimularTemporadaReq(BaseModel):
    idade: int
    temporada_num: int
    ovr: int
    posicao: str
    time_atual: str
    arremesso: int
    playmaking: int
    defesa: int
    rebotes: int
    fisico: int
    clutch: int

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"franquias": TODAS_FRANQUIAS}
    )

@app.get("/api/sortear-opcoes/{atributo}")
async def sortear_opcoes(atributo: str):
    escolhidos = random.sample(JOGADORES, 4)
    return [
        {"nome": j["nome"], "time": j["time"], "valor": j["stats"].get(atributo, 75)}
        for j in escolhidos
    ]

@app.post("/api/simular-ano")
async def simular_ano(req: SimularTemporadaReq):
    # Envelhecimento / Evolução do OVR
    novo_ovr = req.ovr
    if req.idade < 27:
        novo_ovr += random.choice([1, 2])
    elif req.idade > 33:
        novo_ovr -= random.choice([1, 2])
    novo_ovr = max(60, min(99, novo_ovr))

    potencial = novo_ovr / 100.0

    # 1. Estatísticas Médias da Temporada Regular
    jogos = random.randint(70, 82)
    
    # Pontos por jogo (PPG)
    base_pts = (req.arremesso * 0.28) + (novo_ovr * 0.12)
    ppg = round(max(8.0, base_pts + random.uniform(-2.5, 4.0)), 1)
    
    # Rebotes por jogo (RPG)
    base_reb = (req.rebotes * 0.11) + (req.fisico * 0.04)
    if req.posicao in ["PF", "C"]:
        base_reb += 4.5
    rpg = round(max(2.0, base_reb + random.uniform(-1.0, 2.0)), 1)
    
    # Assistências por jogo (APG)
    base_ast = (req.playmaking * 0.10)
    if req.posicao == "PG":
        base_ast += 4.0
    apg = round(max(1.5, base_ast + random.uniform(-1.0, 2.0)), 1)

    pts_totais_ano = int(ppg * jogos)

    # 2. Prêmios da Temporada
    all_star = random.random() < (potencial ** 1.3) * 0.95
    mvp = (novo_ovr >= 92) and (random.random() < (potencial ** 3.3) * 0.45)

    # Campanha do time (Vitórias e Derrotas)
    vitorias = int(min(68, max(25, (novo_ovr * 0.6) + random.randint(-8, 14))))
    derrotas = 82 - vitorias

    # 3. Playoffs & Jogo Decisivo do Ano
    foi_playoffs = vitorias >= 41
    campeao = False
    finals_mvp = False
    jogo_decisivo_pts = 0
    resumo_playoff = "Não foi aos Playoffs"

    if foi_playoffs:
        # Pontuação no Jogo Decisivo dos Playoffs
        jogo_decisivo_pts = int(ppg + random.randint(-4, 16))
        
        # Chance de Anel (Influenciada por Clutch e OVR)
        fator_titulo = (req.clutch * 0.5 + novo_ovr * 0.5) / 100
        if vitorias >= 50 and random.random() < (fator_titulo ** 2.1) * 0.48:
            campeao = True
            finals_mvp = random.random() < 0.85
            resumo_playoff = f"🏆 CAMPEÃO DA NBA! (Você anotou {jogo_decisivo_pts} pts no Jogo 7 das Finais!)"
        else:
            fase = random.choice(["1ª Rodada", "Semifinais de Conferência", "Finais de Conferência", "Vice-campeão nas Finais"])
            resumo_playoff = f"Eliminado ({fase}) • Você fez {jogo_decisivo_pts} pts no jogo eliminatório."

    # 4. Propostas de Mercado para a Offseason
    outras_franquias = [f for f in TODAS_FRANQUIAS if f["nome"] != req.time_atual]
    propostas_times = random.sample(outras_franquias, 3)
    salario_base = int((novo_ovr * 0.45) + random.randint(5, 15))
    
    propostas = [
        {"time": req.time_atual, "salario": f"${salario_base}M / ano", "status": "Renovação (Permanecer Leal)"}
    ]
    for p in propostas_times:
        sal = int(salario_base + random.randint(-5, 8))
        propostas.append({"time": p["nome"], "salario": f"${sal}M / ano", "status": p["status"]})

    return {
        "novo_idade": req.idade + 1,
        "novo_ovr": novo_ovr,
        "jogos": jogos,
        "ppg": ppg,
        "rpg": rpg,
        "apg": apg,
        "pts_totais_ano": pts_totais_ano,
        "campanha": f"{vitorias}-{derrotas}",
        "all_star": all_star,
        "mvp": mvp,
        "campeao": campeao,
        "finals_mvp": finals_mvp,
        "jogo_decisivo_pts": jogo_decisivo_pts,
        "resumo_playoff": resumo_playoff,
        "propostas_offseason": propostas
    }