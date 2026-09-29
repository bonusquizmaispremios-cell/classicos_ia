import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CLÁSSICOS IA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_classicos():
    return {"perfis": {}}

_cache = get_cache_classicos()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_consultas', 'consultas_salvas',
    'veiculo_padrao', 'diario_restauracao', 'quiz_pontuacao', 'quiz_nivel_atual',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_consulta(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_consultas.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_consultas': [], 'consultas_salvas': [],
    'veiculo_padrao': "", 'diario_restauracao': [], 'quiz_pontuacao': 0, 'quiz_nivel_atual': "Iniciante",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO DE HONESTIDADE TÉCNICA — compartilhado ---
PRINCIPIO_HONESTIDADE = """
PRINCÍPIO OBRIGATÓRIO DE HONESTIDADE TÉCNICA — siga isso em TODA resposta:
- Você é um especialista em carros clássicos, mas trabalha apenas com DESCRIÇÕES EM TEXTO fornecidas pela pessoa —
  você não recebe fotos reais nem tem acesso a bancos de dados de chassi, leilões ou cotações em tempo real
- Para análises de originalidade, peças e autenticidade: baseie-se no que foi DESCRITO pela pessoa, sempre deixando claro
  que é uma orientação educativa, e que avaliação presencial por especialista é necessária para decisões de compra,
  venda ou certificação
- Para Placa Preta: explique os critérios GERAIS normalmente considerados, mas seja claro que a certificação oficial
  é feita por entidades específicas (como clubes de marca filiados à FBVA) com vistoria presencial — sua análise é
  apenas uma pré-avaliação educativa, nunca uma garantia de aprovação
- Para valores e valorização de mercado: você NÃO tem acesso a cotações atuais nem dados de leilões em tempo real.
  Baseie-se em padrões históricos conhecidos do mercado de clássicos e tendências gerais, sempre recomendando
  confirmar valores com tabelas especializadas (ex: Tabela FIPE Collection), avaliadores profissionais e anúncios reais
  do mercado antes de qualquer decisão financeira
- Nunca afirme um valor exato de mercado como fato — sempre apresente faixas e como estimativas
- Para diagnóstico mecânico: sempre recomende confirmação com mecânico especializado em clássicos antes de intervenções,
  especialmente em itens de segurança (freios, suspensão, direção)
- Seja apaixonado e didático — você é um conhecedor que genuinamente ama carros clássicos, não um robô burocrático
- Português do Brasil
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Importante:</strong> esta análise é educativa, baseada na descrição fornecida — não substitui avaliação
presencial por especialista, perito ou avaliador profissional. Para decisões de compra, venda, restauração ou
certificação, sempre confirme com profissionais qualificados.
</div>
"""

DISCLAIMER_AVALIACAO = """
<div class="disclaimer-avaliacao">
💰 <strong>Sobre valores de mercado:</strong> esta é uma estimativa educativa baseada em padrões históricos gerais —
não reflete cotações em tempo real. Antes de comprar, vender ou negociar, consulte a Tabela FIPE Collection,
avaliadores especializados e anúncios reais de veículos similares no mercado atual.
</div>
"""

# --- MOTOR DE IA ---
def classicos_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é o maior especialista em carros antigos e clássicos do Brasil — um misto de restaurador
experiente, historiador automotivo, mecânico especializado e avaliador de mercado.
Usuário: {st.session_state.usuario}. Veículo de interesse: {st.session_state.veiculo_padrao or 'não informado'}.
{PRINCIPIO_HONESTIDADE}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def renderizar_indice(texto: str, titulo_indice: str = "ÍNDICE"):
    percentuais = re.findall(r'(\d+)\s*/\s*100|(\d+)%', texto)
    valores = [int(a or b) for a, b in percentuais if a or b]
    indice = valores[0] if valores else 50

    if indice >= 70:
        classe, emoji, label = "indice-alto", "🟢", "ALTO"
    elif indice >= 40:
        classe, emoji, label = "indice-medio", "🟡", "MÉDIO"
    else:
        classe, emoji, label = "indice-baixo", "🔴", "BAIXO"

    st.markdown(f"""
    <div class="indice-box {classe}">
        <div style="font-size:2.2em;">{emoji}</div>
        <div class="indice-titulo">{titulo_indice}: {indice}/100</div>
        <div style="font-size:0.95em;color:#444;font-weight:600;">Nível: {label}</div>
        <div style="font-size:0.82em;color:#555;margin-top:6px;">Estimativa educativa baseada na descrição fornecida</div>
    </div>
    """, unsafe_allow_html=True)

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_consultas)
    diario = len(st.session_state.diario_restauracao)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FEF3E2;border:1px solid #B45309;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} consultas geradas · {diario} entradas no diário de restauração</span>"
            f"</div>", unsafe_allow_html=True
        )
    with col_btn:
        st.download_button("💾 SALVAR MEUS DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"classicos_ia_{nome_usuario}.json", mime="application/json", use_container_width=True,
        key="dl_classico_1"
    )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'consultas_salvas' not in st.session_state: st.session_state['consultas_salvas'] = []
if 'diario_restauracao' not in st.session_state: st.session_state['diario_restauracao'] = None
if 'historico_consultas' not in st.session_state: st.session_state['historico_consultas'] = []
if 'quiz_nivel_atual' not in st.session_state: st.session_state['quiz_nivel_atual'] = None
if 'quiz_pontuacao' not in st.session_state: st.session_state['quiz_pontuacao'] = None
if 'veiculo_padrao' not in st.session_state: st.session_state['veiculo_padrao'] = None

def chamar_ia(prompt, sistema="Você é um assistente inteligente. Responda em português do Brasil."):
    try:
        from groq import Groq as _GrCI
        client = _GrCI(api_key=st.session_state.api_key)
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role":"system","content":sistema},{"role":"user","content":prompt}],
            max_tokens=2048
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 CLÁSSICOS IA")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS
    _tab_Home, _tab_Identificacao, _tab_Originalidade, _tab_Detector, _tab_Cores, _tab_Indice, _tab_Avaliacao, _tab_Restauracao, _tab_Diagnostico, _tab_Pecas, _tab_Documentacao, _tab_PlacaPreta, _tab_Radar, _tab_Timeline, _tab_Historia, _tab_Diario, _tab_Som, _tab_Quiz, _tab_Engenharia, _tab_DNA, _tab_Consultor = st.tabs(['🏠 Painel Principal', '🚘 Identificação Comp', '📸 Scanner de Origina', '🔎 Detector de Peças ', '🎨 Cores Originais', '🏆 Índice do Colecion', '💰 Avaliação Intelige', '🛠️ Planejamento da Re', '🔧 Diagnóstico Mecâni', '📦 Guia de Peças', '🧾 Documentação', '🏅 Simulador de Placa', '💎 Radar do Coleciona', '🏁 Linha do Tempo', '🌎 História do Modelo', '🏕️ Diário da Restaura', '🔊 Som Original', '🧠 Quiz do Colecionad', '🔬 Engenharia Explica', '🧬 DNA do Automóvel', '🤖 Consultor 24 Horas'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_classico")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_classico", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🚗")
            st.markdown("<span class='badge'>Garagem Aberta</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="classico3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_consultas) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        st.session_state.veiculo_padrao = st.text_input("🚗 Seu veículo (modelo e ano):",
            value=st.session_state.veiculo_padrao, placeholder="ex: Fusca 1974, Opala 1980, Maverick GT 1976...", key="ti_classico_101")


        modulos_count = {}
        for c in st.session_state.historico_consultas:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_consultas)}</div><div>Consultas geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_restauracao)}</div><div>Registros de restauração</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.consultas_salvas)}</div><div>Salvas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.quiz_pontuacao}</div><div>Pontos no Quiz</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'Um carro clássico não é apenas transporte do passado — é uma máquina do tempo que ainda funciona.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "🚘 Identificação": "História, especificações, motorização e curiosidades de qualquer modelo/ano",
            "📸 Scanner de Originalidade": "Descreva o veículo e receba índice educativo de originalidade",
            "🔎 Detector de Peças": "Identifica possíveis incompatibilidades com base na descrição",
            "🎨 Cores Originais": "Cores de fábrica, códigos de tinta e combinações por ano",
            "🏆 Índice do Colecionador": "Nota completa considerando originalidade, conservação e raridade",
            "💰 Avaliação Inteligente": "Estimativa de valor considerando múltiplos fatores do mercado de clássicos",
            "🛠️ Planejamento da Restauração": "Ordem ideal de serviços, tempo e custos estimados",
            "🔧 Diagnóstico Mecânico": "Descreva um problema e receba possíveis causas",
            "📦 Guia de Peças": "Originais vs reproduzidas, compatibilidade e onde procurar",
            "🧾 Documentação": "Transferência, placa preta, regularização, importados",
            "🏅 Simulador de Placa Preta": "Pré-avaliação educativa dos critérios de certificação",
            "💎 Radar do Colecionador": "Tendências, valorização e oportunidades no mercado de clássicos",
            "🏁 Linha do Tempo": "Evolução do modelo ano a ano",
            "🌎 História do Modelo": "Origem, designers, contexto histórico e curiosidades",
            "🏕️ Diário da Restauração": "Registre fotos, gastos e etapas do seu projeto",
            "🔊 Som Original": "Como era o ronco original do motor de fábrica",
            "🧠 Quiz do Colecionador": "Teste seu conhecimento em 5 níveis de dificuldade",
            "🔬 Engenharia Explicada": "Carburador, distribuidor, suspensão e mais — de forma simples",
            "🧬 DNA do Automóvel": "Viagem no tempo até a época em que o veículo nasceu",
            "🤖 Consultor 24h": "Pergunte qualquer coisa sobre qualquer carro antigo",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        st.header("🚘 Identificação Completa")
        st.markdown("Informe modelo e ano para uma análise histórica e técnica completa.")

        col1, col2 = st.columns(2)
        with col1:
            modelo_id = st.text_input("🚗 Modelo:", value=st.session_state.veiculo_padrao.split(' ')[0] if st.session_state.veiculo_padrao else "", placeholder="ex: Fusca, Opala, Maverick, Dodge Dart...", key="input_modelo_id")
        with col2:
            ano_id = st.text_input("📅 Ano:", placeholder="ex: 1974", key="ti_classico_102")

        if st.button("🚘 IDENTIFICAR VEÍCULO", key="classico4"):
            if modelo_id.strip():
                with st.spinner("Buscando informações..."):
                    prompt = (
                        f"Crie uma identificação completa do veículo: {modelo_id} {ano_id}.\n\n"
                        f"FORMATO:\n\n"
                        f"🚘 {modelo_id.upper()} {ano_id}\n\n"
                        f"📖 HISTÓRIA RESUMIDA:\n[origem e contexto do modelo]\n\n"
                        f"⚙️ ESPECIFICAÇÕES TÉCNICAS:\n[motor, potência, transmissão, dimensões — para esse ano específico]\n\n"
                        f"🔧 VERSÕES E OPCIONAIS:\n[versões disponíveis nesse ano e principais opcionais]\n\n"
                        f"🏭 PRODUÇÃO:\n[quantidade produzida aproximada, se conhecida, e países onde foi vendido]\n\n"
                        f"📈 EVOLUÇÃO:\n[principais diferenças desse ano em relação aos anteriores/seguintes]\n\n"
                        f"💡 CURIOSIDADES:\n[2-3 curiosidades interessantes sobre esse modelo/ano]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Identificacao", f"{modelo_id} {ano_id}", res)
                    st.session_state['ident_temp'] = res
            else:
                st.warning("Informe o modelo.")

        if st.session_state.get('ident_temp'):
            st.markdown(f"<div class='card'>{st.session_state['ident_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['ident_temp'], file_name="identificacao.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_2"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_ident", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Identificacao','tema':f"{modelo_id} {ano_id}" if 'modelo_id' in dir() else '','conteudo':st.session_state['ident_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # SCANNER DE ORIGINALIDADE
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
            st.download_button("💾 Salvar dados (.json)",
                data=_json_sv.dumps(_dados_sv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_sv_classico")
        with _csl2:
            _arq_sv = st.file_uploader("📂 Carregar dados:", type=["json"], key="ul_sv_classico")
            if _arq_sv:
                try:
                    import json as _json_ld
                    for _k, _v in _json_ld.loads(_arq_sv.read().decode()).items():
                        st.session_state[_k] = _v
                    st.success("✅ Dados carregados!")
                    st.rerun()
                except: st.error("Arquivo inválido.")

    with _tab_Identificacao:
        st.header("Identificacao")
        st.markdown("Descreva o contexto para análise:")
        prompt_identificacao = st.text_area("", height=150, key="ta_identificacao1", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="btn_identificacao1", use_container_width=True):
            if prompt_identificacao.strip():
                with st.spinner("Analisando..."):
                    try:
                        resp = chamar_ia(prompt_identificacao)
                        if resp: st.session_state['res_identificaca_classi1'] = str(resp)
                        if resp: st.session_state['res_identifica_classi1'] = resp
                        st.markdown(f"<div class='card'>{resp}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Erro: {e}")
            else:
                st.warning("Preencha o campo.")

    with _tab_Originalidade:
        st.header("📸 Scanner de Originalidade")
        st.markdown("Descreva o veículo em detalhes para uma análise educativa de originalidade.")

        st.info("📝 Este app trabalha por descrição em texto. Quanto mais detalhes você der, melhor a análise.")

        col1, col2 = st.columns(2)
        with col1:
            veiculo_orig = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="ti_classico_103")
        with col2:
            cor_orig = st.text_input("🎨 Cor atual:", placeholder="ex: azul metálico", key="ti_classico_104")

        descricao_orig = st.text_area("📝 Descreva detalhadamente: pintura, rodas, bancos, painel, volante, lanternas, faróis, retrovisores, emblemas, motor:",
            height=180, placeholder="ex: Pintura azul original com alguns retoques no para-choque. Rodas de liga leve (não tenho certeza se são originais). "
                                     "Bancos em couro preto, parecem originais. Painel com instrumentos completos funcionando. Motor original 1.6...", key="classico7")

        if st.button("📸 ANALISAR ORIGINALIDADE", key="classico5"):
            if descricao_orig.strip():
                with st.spinner("Analisando originalidade..."):
                    prompt = (
                        f"Analise a originalidade deste veículo com base na descrição.\n"
                        f"Veículo: {veiculo_orig}. Cor: {cor_orig}.\n"
                        f"Descrição: {descricao_orig}\n\n"
                        f"FORMATO:\n\n"
                        f"📸 ÍNDICE DE ORIGINALIDADE: [X]/100\n"
                        f"[1-2 linhas explicando a estimativa com base no que foi descrito]\n\n"
                        f"✅ ITENS QUE PARECEM ORIGINAIS:\n[com base na descrição]\n\n"
                        f"⚠️ ITENS QUE MERECEM VERIFICAÇÃO:\n[itens com descrição ambígua ou suspeita de não-originalidade]\n\n"
                        f"🔍 O QUE VERIFICAR PRESENCIALMENTE:\n[pontos que só um especialista presencial pode confirmar — números de chassi/motor, código de tinta no local correto, etc]\n\n"
                        f"💡 DICA PARA PRÓXIMA ANÁLISE:\n[que outras informações ajudariam a refinar essa análise]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Originalidade", veiculo_orig, res)
                    st.session_state['orig_temp'] = res
            else:
                st.warning("Descreva o veículo.")

        if st.session_state.get('orig_temp'):
            renderizar_indice(st.session_state['orig_temp'], "ÍNDICE DE ORIGINALIDADE")
            st.markdown(f"<div class='card'>{st.session_state['orig_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['orig_temp'], file_name="originalidade.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_3"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_orig", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Originalidade','tema':veiculo_orig if 'veiculo_orig' in dir() else '','conteudo':st.session_state['orig_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # DETECTOR DE PEÇAS NÃO ORIGINAIS
        # ========================

    with _tab_Detector:
        st.header("🔎 Detector de Peças Não Originais")
        st.markdown("Descreva peças específicas para identificar possíveis incompatibilidades.")

        veiculo_det = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_det")
        pecas_det = st.text_area("🔧 Descreva as peças que quer verificar:", height=150,
            placeholder="ex: Rodas aro 15 esportivas, lanternas traseiras com lente fumê, volante de 3 raios em alumínio, bancos de couro vermelho...", key="classico6")

        if st.button("🔎 VERIFICAR COMPATIBILIDADE", key="classico6_d2"):
            if pecas_det.strip() and veiculo_det.strip():
                with st.spinner("Verificando..."):
                    prompt = (
                        f"Analise se estas peças são compatíveis com a originalidade do veículo.\n"
                        f"Veículo: {veiculo_det}.\nPeças descritas: {pecas_det}\n\n"
                        f"FORMATO:\n\n"
                        f"🔎 ANÁLISE DE COMPATIBILIDADE — {veiculo_det.upper()}\n\n"
                        f"[Para cada peça descrita:]\n"
                        f"🔧 [NOME DA PEÇA]\n"
                        f"Status provável: [Original / Possivelmente não original / Não foi possível avaliar]\n"
                        f"Justificativa: [por que, com base no conhecimento sobre esse modelo/ano]\n\n"
                        f"📋 RESUMO GERAL:\n[conclusão geral sobre o conjunto de peças]\n\n"
                        f"🔍 RECOMENDAÇÃO:\n[o que fazer para confirmar com certeza — pesquisa de catálogo original, comparação com outros exemplares, etc]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Detector", veiculo_det, res)
                    st.session_state['detector_temp'] = res
            else:
                st.warning("Informe o veículo e as peças.")

        if st.session_state.get('detector_temp'):
            st.markdown(f"<div class='card-red'>{st.session_state['detector_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['detector_temp'], file_name="deteccao_pecas.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_4"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_det", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Detector','tema':veiculo_det if 'veiculo_det' in dir() else '','conteudo':st.session_state['detector_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # CORES ORIGINAIS
        # ========================

    with _tab_Cores:
        st.header("🎨 Cores Originais")
        st.markdown("Descubra as cores de fábrica de qualquer modelo.")

        veiculo_cor = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_cor")

        if st.button("🎨 VER CORES ORIGINAIS", key="classico7_d2"):
            if veiculo_cor.strip():
                with st.spinner("Buscando cores..."):
                    prompt = (
                        f"Liste as cores originais de fábrica para: {veiculo_cor}\n\n"
                        f"FORMATO:\n\n"
                        f"🎨 CORES ORIGINAIS — {veiculo_cor.upper()}\n\n"
                        f"[Para cada cor:]\n"
                        f"🎨 [Nome da cor]\n"
                        f"Código de tinta: [se conhecido]\n"
                        f"Anos de utilização: [período]\n"
                        f"Combinação interna usual: [cor do banco/painel que combinava]\n\n"
                        f"⭐ SÉRIES ESPECIAIS:\n[cores exclusivas de versões especiais, se houver]\n\n"
                        f"💡 DICA:\n[como verificar a cor original em um veículo restaurado — local da etiqueta/código]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Cores", veiculo_cor, res)
                    st.session_state['cores_temp'] = res
            else:
                st.warning("Informe o veículo.")

        if st.session_state.get('cores_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['cores_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['cores_temp'], file_name="cores_originais.txt", mime="text/plain",
        key="dl_classico_5"
    )

        # ========================
        # ÍNDICE DO COLECIONADOR
        # ========================

    with _tab_Indice:
        st.header("🏆 Índice do Colecionador")
        st.markdown("Avaliação completa considerando 7 critérios fundamentais.")

        veiculo_idx = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_idx")

        col1, col2 = st.columns(2)
        with col1:
            originalidade_idx = st.slider("⭐ Originalidade (sua avaliação):", 0, 10, 5, key="classico1")
            conservacao_idx = st.slider("⭐ Conservação:", 0, 10, 5, key="classico2")
            raridade_idx = st.slider("⭐ Raridade (sua percepção):", 0, 10, 5, key="classico3_x2")
            mecanica_idx = st.slider("⭐ Estado mecânico:", 0, 10, 5, key="classico4_x2")
        with col2:
            estetica_idx = st.slider("⭐ Estado estético:", 0, 10, 5, key="classico5_x2")
            documentacao_idx = st.slider("⭐ Documentação:", 0, 10, 5, key="classico6_x2")
            notas_idx = st.text_area("📝 Observações adicionais:", height=80, key="classico8")

        if st.button("🏆 CALCULAR ÍNDICE COMPLETO", key="classico9"):
            if veiculo_idx.strip():
                with st.spinner("Calculando..."):
                    prompt = (
                        f"Crie uma avaliação completa de colecionador para este veículo.\n"
                        f"Veículo: {veiculo_idx}.\n"
                        f"Autoavaliação do proprietário: Originalidade {originalidade_idx}/10, Conservação {conservacao_idx}/10, "
                        f"Raridade {raridade_idx}/10, Mecânica {mecanica_idx}/10, Estética {estetica_idx}/10, Documentação {documentacao_idx}/10.\n"
                        f"Observações: {notas_idx or 'nenhuma'}\n\n"
                        f"FORMATO:\n\n"
                        f"🏆 ÍNDICE DO COLECIONADOR: [X]/100\n"
                        f"[Calcule uma nota geral ponderada com base nos 6 critérios + conhecimento sobre raridade real desse modelo]\n\n"
                        f"⭐ ORIGINALIDADE: {originalidade_idx}/10 — [comentário]\n"
                        f"⭐ CONSERVAÇÃO: {conservacao_idx}/10 — [comentário]\n"
                        f"⭐ RARIDADE: [sua avaliação real baseada no modelo]/10 — [comentário, considerando se a autoavaliação do dono está alinhada com a raridade real do modelo]\n"
                        f"⭐ ESTADO MECÂNICO: {mecanica_idx}/10 — [comentário]\n"
                        f"⭐ ESTADO ESTÉTICO: {estetica_idx}/10 — [comentário]\n"
                        f"⭐ DOCUMENTAÇÃO: {documentacao_idx}/10 — [comentário]\n"
                        f"⭐ POTENCIAL DE VALORIZAÇÃO: [X]/10 — [comentário baseado em tendências gerais do modelo]\n\n"
                        f"🎯 O QUE MAIS AUMENTARIA O VALOR DESTE VEÍCULO:\n[1-2 ações prioritárias]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Indice", veiculo_idx, res)
                    st.session_state['indice_temp'] = res
            else:
                st.warning("Informe o veículo.")

        if st.session_state.get('indice_temp'):
            renderizar_indice(st.session_state['indice_temp'], "ÍNDICE DO COLECIONADOR")
            st.markdown(f"<div class='card-gold'>{st.session_state['indice_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['indice_temp'], file_name="indice_colecionador.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_6"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_idx", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Indice','tema':veiculo_idx if 'veiculo_idx' in dir() else '','conteudo':st.session_state['indice_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # AVALIAÇÃO INTELIGENTE
        # ========================

    with _tab_Avaliacao:
        st.header("💰 Avaliação Inteligente")
        st.markdown(DISCLAIMER_AVALIACAO, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            veiculo_aval = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_aval")
            estado_aval = st.selectbox("📊 Estado geral:", ["Original e impecável","Bem conservado","Restaurado","Em restauração","Sucata/projeto","Modificado"], key="classico10")
        with col2:
            documentacao_aval = st.selectbox("🧾 Documentação:", ["Em dia, placa preta","Em dia, comum","Pendências simples","Pendências complexas","Sem documentação"], key="classico11")
            regiao_aval = st.text_input("📍 Região (opcional):", placeholder="ex: São Paulo, SP", key="ti_classico_105")

        detalhes_aval = st.text_area("📝 Detalhes adicionais:", height=100,
            placeholder="ex: Motor original, pintura refeita há 2 anos, interior original, rodas de liga não originais...", key="classico5_d2")

        if st.button("💰 GERAR ESTIMATIVA", key="classico12"):
            if veiculo_aval.strip():
                with st.spinner("Calculando estimativa..."):
                    prompt = (
                        f"Crie uma estimativa de valor para este veículo clássico.\n"
                        f"Veículo: {veiculo_aval}. Estado: {estado_aval}. Documentação: {documentacao_aval}.\n"
                        f"Região: {regiao_aval or 'não informada'}. Detalhes: {detalhes_aval or 'não informado'}.\n\n"
                        f"FORMATO:\n\n"
                        f"💰 ESTIMATIVA DE VALOR — {veiculo_aval.upper()}\n\n"
                        f"📊 FAIXA DE VALOR ESTIMADA: R$[X] a R$[X]\n"
                        f"[Baseado em padrões históricos do mercado de clássicos para esse modelo/estado]\n\n"
                        f"📈 FATORES QUE AUMENTAM O VALOR:\n[com base no estado e detalhes informados]\n\n"
                        f"📉 FATORES QUE REDUZEM O VALOR:\n[com base no estado e detalhes informados]\n\n"
                        f"🎯 ONDE ESSE VEÍCULO SE POSICIONA NO MERCADO:\n[comparação geral com a faixa de exemplares desse modelo]\n\n"
                        f"💡 COMO AUMENTAR O VALOR:\n[2-3 ações com melhor custo-benefício]\n\n"
                        f"🔍 ONDE CONFIRMAR ESSE VALOR:\n[Tabela FIPE Collection, anúncios reais, avaliadores especializados, clubes da marca]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Avaliacao", veiculo_aval, res)
                    st.session_state['aval_temp'] = res
            else:
                st.warning("Informe o veículo.")

        if st.session_state.get('aval_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['aval_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['aval_temp'], file_name="avaliacao.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_7"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_aval", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Avaliacao','tema':veiculo_aval if 'veiculo_aval' in dir() else '','conteudo':st.session_state['aval_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # PLANEJAMENTO DA RESTAURAÇÃO
        # ========================

    with _tab_Restauracao:
        st.header("🛠️ Planejamento da Restauração")

        col1, col2 = st.columns(2)
        with col1:
            veiculo_rest = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_rest")
            orcamento_rest = st.number_input("💰 Orçamento disponível (R$):", min_value=0.0, value=10000.0, step=1000.0, key="classico13")
        with col2:
            estado_atual_rest = st.selectbox("📊 Estado atual:", ["Rodando, precisa de retoques","Parado, mecânica ok","Parado há anos","Apenas a carroceria/chassi","Projeto desde zero"], key="classico14")
            prazo_rest = st.text_input("📅 Prazo desejado:", placeholder="ex: 6 meses, 1 ano, sem pressa...", key="ti_classico_106")

        descricao_rest = st.text_area("📝 Descreva o estado e o que precisa ser feito:", height=120,
            placeholder="ex: Motor funciona mas com barulho estranho, lataria com pontos de ferrugem, interior original mas gasto, pintura descascando...", key="classico4_d2")

        if st.button("🛠️ CRIAR PLANO DE RESTAURAÇÃO", key="classico15"):
            if veiculo_rest.strip():
                with st.spinner("Montando plano..."):
                    prompt = (
                        f"Crie um plano completo de restauração.\n"
                        f"Veículo: {veiculo_rest}. Orçamento: R${orcamento_rest}. Estado atual: {estado_atual_rest}.\n"
                        f"Prazo: {prazo_rest or 'flexível'}. Descrição: {descricao_rest or 'não detalhada'}.\n\n"
                        f"FORMATO:\n\n"
                        f"🛠️ PLANO DE RESTAURAÇÃO — {veiculo_rest.upper()}\n"
                        f"Orçamento: R${orcamento_rest} | Prazo: {prazo_rest or 'flexível'}\n\n"
                        f"📋 ORDEM IDEAL DOS SERVIÇOS:\n"
                        f"1. [serviço] — Complexidade: [X] — Tempo estimado: [X] — Custo aproximado: R$[X]\n"
                        f"[continue numerando todos os serviços necessários, na ordem lógica de execução]\n\n"
                        f"🎯 PRIORIDADES (o que fazer primeiro mesmo com orçamento limitado):\n[itens críticos de segurança/mecânica antes de estética]\n\n"
                        f"📅 CRONOGRAMA SUGERIDO:\n[divisão por fases/meses considerando o prazo informado]\n\n"
                        f"💰 DISTRIBUIÇÃO DO ORÇAMENTO:\n[como dividir os R${orcamento_rest} entre as categorias de serviço]\n\n"
                        f"⚠️ RISCOS DESSE TIPO DE RESTAURAÇÃO:\n[o que costuma sair do orçamento/prazo nesse tipo de projeto]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Restauracao", veiculo_rest, res)
                    st.session_state['rest_temp'] = res
            else:
                st.warning("Informe o veículo.")

        if st.session_state.get('rest_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['rest_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['rest_temp'], file_name="plano_restauracao.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_8"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_rest", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Restauracao','tema':veiculo_rest if 'veiculo_rest' in dir() else '','conteudo':st.session_state['rest_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # DIAGNÓSTICO MECÂNICO
        # ========================

    with _tab_Diagnostico:
        st.header("🔧 Diagnóstico Mecânico")

        veiculo_diag = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_diag")
        problema_diag = st.text_area("📝 Descreva o problema:", height=120,
            placeholder="ex: O motor está fazendo um ruído metálico quando acelero, principalmente em baixa rotação...", key="classico3_d2")

        if st.button("🔧 DIAGNOSTICAR", key="classico16"):
            if problema_diag.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Faça um diagnóstico mecânico preliminar.\n"
                        f"Veículo: {veiculo_diag}. Problema: {problema_diag}\n\n"
                        f"FORMATO:\n\n"
                        f"🔧 DIAGNÓSTICO — {veiculo_diag.upper()}\n\n"
                        f"🔍 POSSÍVEIS CAUSAS (da mais para a menos provável):\n[liste com base no sintoma descrito e no conhecimento sobre esse modelo]\n\n"
                        f"⚙️ COMPONENTES ENVOLVIDOS:\n[peças que tipicamente causam esse sintoma]\n\n"
                        f"🧪 TESTES RECOMENDADOS:\n[testes simples que ajudam a confirmar a causa]\n\n"
                        f"🚨 NÍVEL DE URGÊNCIA: [Baixo/Médio/Alto/Crítico]\n[justificativa — é seguro continuar rodando?]\n\n"
                        f"🔧 RECOMENDAÇÃO:\n[orientação final, sempre recomendando confirmação com mecânico especializado em clássicos]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Diagnostico", problema_diag[:60], res)
                    st.session_state['diag_temp'] = res
            else:
                st.warning("Descreva o problema.")

        if st.session_state.get('diag_temp'):
            st.markdown(f"<div class='card-red'>{st.session_state['diag_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['diag_temp'], file_name="diagnostico.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_9"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_diag", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'Diagnostico','tema':problema_diag[:60] if 'problema_diag' in dir() else '','conteudo':st.session_state['diag_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # GUIA DE PEÇAS
        # ========================

    with _tab_Pecas:
        st.header("📦 Guia de Peças")

        veiculo_pecas = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_pecas")
        peca_busca = st.text_input("🔧 Peça que você procura:", placeholder="ex: lanterna traseira, carburador, friso lateral...", key="ti_classico_107")

        if st.button("📦 BUSCAR INFORMAÇÕES DA PEÇA", key="classico17"):
            if peca_busca.strip() and veiculo_pecas.strip():
                with st.spinner("Buscando informações..."):
                    prompt = (
                        f"Forneça um guia completo sobre esta peça.\n"
                        f"Veículo: {veiculo_pecas}. Peça: {peca_busca}\n\n"
                        f"FORMATO:\n\n"
                        f"📦 {peca_busca.upper()} — {veiculo_pecas.upper()}\n\n"
                        f"🏭 PEÇA ORIGINAL:\n[características da peça original de fábrica]\n\n"
                        f"🔄 PEÇAS REPRODUZIDAS:\n[se existem reproduções no mercado e qualidade geral]\n\n"
                        f"✅ COMPATIBILIDADE:\n[outros modelos/anos que usam peça igual ou similar]\n\n"
                        f"🔍 DIFICULDADE PARA ENCONTRAR:\n[Fácil/Moderada/Difícil/Raríssima — e onde costuma-se procurar: clubes, feiras, importação]\n\n"
                        f"⚠️ CUIDADOS NA COMPRA:\n[como verificar se é original, problemas comuns em peças usadas desse tipo]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Pecas", f"{veiculo_pecas} — {peca_busca}", res)
                    st.session_state['pecas_temp'] = res
            else:
                st.warning("Informe o veículo e a peça.")

        if st.session_state.get('pecas_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['pecas_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['pecas_temp'], file_name="guia_pecas.txt", mime="text/plain",
        key="dl_classico_10"
    )

        # ========================
        # DOCUMENTAÇÃO
        # ========================

    with _tab_Documentacao:
        st.header("🧾 Documentação")

        tema_doc = st.selectbox("Tema:", [
            "Transferência de propriedade", "Placa preta — o que é e como solicitar",
            "Regularização de veículo sem documento", "Veículos modificados — documentação",
            "Importados — nacionalização e documentação", "Compra em leilão — cuidados documentais",
            "Licenciamento de veículo antigo", "Outro (perguntar)",
        ], key="classico2_d2")
        pergunta_doc = ""
        if tema_doc == "Outro (perguntar)":
            pergunta_doc = st.text_input("Sua dúvida sobre documentação:", key="ti_classico_108")

        if st.button("🧾 EXPLICAR", key="classico18"):
            topico = pergunta_doc if tema_doc == "Outro (perguntar)" and pergunta_doc.strip() else tema_doc
            if topico.strip():
                with st.spinner("Preparando explicação..."):
                    prompt = (
                        f"Explique de forma clara e prática: {topico}, no contexto de carros clássicos no Brasil.\n\n"
                        f"FORMATO:\n\n"
                        f"🧾 {topico.upper()}\n\n"
                        f"📖 O QUE É / COMO FUNCIONA:\n[explicação clara]\n\n"
                        f"📋 PASSO A PASSO GERAL:\n[processo típico — sempre observando que procedimentos variam por estado/DETRAN]\n\n"
                        f"📄 DOCUMENTOS GERALMENTE NECESSÁRIOS:\n[lista]\n\n"
                        f"⚠️ CUIDADOS E PEGADINHAS COMUNS:\n[erros frequentes nesse processo]\n\n"
                        f"💡 DICA:\n[1 dica prática]\n\n"
                        f"📍 IMPORTANTE: procedimentos de DETRAN variam por estado — confirme sempre no órgão local."
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Documentacao", topico, res)
                    st.session_state['doc_temp'] = res
            else:
                st.warning("Escolha ou descreva o tema.")

        if st.session_state.get('doc_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['doc_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['doc_temp'], file_name="documentacao.txt", mime="text/plain",
        key="dl_classico_11"
    )

        # ========================
        # SIMULADOR DE PLACA PRETA
        # ========================

    with _tab_PlacaPreta:
        st.header("🏅 Simulador de Placa Preta")

        st.markdown("""<div class="disclaimer-avaliacao">
        🏅 <strong>Importante:</strong> a certificação oficial de Placa Preta é feita por clubes de marca filiados à
        FBVA (Federação Brasileira de Veículos Antigos) com vistoria presencial. Esta é apenas uma PRÉ-AVALIAÇÃO
        educativa — não garante aprovação real.
        </div>""", unsafe_allow_html=True)

        veiculo_pp = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_pp")
        idade_pp = st.text_input("📅 Idade do veículo (anos):", placeholder="ex: 35 anos", key="ti_classico_109")
        descricao_pp = st.text_area("📝 Descreva o estado de originalidade e conservação:", height=150,
            placeholder="ex: Veículo com 35 anos, motor original, pintura original com pequenos retoques, interior original, documentação em dia...", key="classico1_d2")

        if st.button("🏅 FAZER PRÉ-AVALIAÇÃO", key="classico19"):
            if descricao_pp.strip() and veiculo_pp.strip():
                with st.spinner("Avaliando critérios..."):
                    prompt = (
                        f"Faça uma pré-avaliação educativa para certificação de Placa Preta.\n"
                        f"Veículo: {veiculo_pp}. Idade: {idade_pp or 'não informada'}.\n"
                        f"Descrição: {descricao_pp}\n\n"
                        f"FORMATO:\n\n"
                        f"🏅 PRÉ-AVALIAÇÃO — {veiculo_pp.upper()}\n\n"
                        f"📅 CRITÉRIO DE IDADE:\n[geralmente exige-se 30+ anos — avalie se atende com base na idade informada]\n\n"
                        f"✅ CRITÉRIOS QUE PARECEM ATENDIDOS:\n[com base na descrição]\n\n"
                        f"⚠️ CRITÉRIOS QUE MERECEM ATENÇÃO:\n[pontos que costumam ser exigidos e podem não estar claros na descrição]\n\n"
                        f"📊 ESTIMATIVA DE CHANCE DE APROVAÇÃO: [Baixa/Moderada/Alta]\n"
                        f"[IMPORTANTE: deixe claro que isso é uma estimativa educativa, não uma garantia]\n\n"
                        f"📋 PRÓXIMOS PASSOS REAIS:\n[como buscar a certificação oficial — clube de marca filiado à FBVA]"
                    )
                    res = classicos_ia(prompt, "Seja conservador nas estimativas de aprovação — sempre deixe claro que apenas a vistoria presencial oficial determina a certificação real.")
                    salvar_consulta("PlacaPreta", veiculo_pp, res)
                    st.session_state['pp_temp'] = res
            else:
                st.warning("Informe o veículo e a descrição.")

        if st.session_state.get('pp_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['pp_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['pp_temp'], file_name="placa_preta.txt", mime="text/plain",
        key="dl_classico_12"
    )

        # ========================
        # RADAR DO COLECIONADOR
        # ========================

    with _tab_Radar:
        st.header("💎 Radar do Colecionador")
        st.markdown(DISCLAIMER_AVALIACAO, unsafe_allow_html=True)

        tema_radar = st.selectbox("O que você quer explorar:", [
            "Os clássicos mais valorizados (tendência histórica)", "Potencial de valorização futura",
            "Melhores oportunidades (preço acessível + potencial)", "Joias esquecidas (pouco conhecidos)",
            "Índice de raridade de um modelo específico", "Índice de desejo (mais procurados)",
            "Mercado nacional vs internacional", "Modelos possivelmente supervalorizados",
            "Melhor momento para comprar/vender", "Próximos clássicos (modelos recentes com potencial)",
        ], key="select_tema_radar")
        categoria_radar = st.text_input("🎯 Categoria ou modelo específico (opcional):", placeholder="ex: nacionais dos anos 70, Opala, esportivos importados...", key="ti_classico_110")

        if st.button("💎 EXPLORAR TENDÊNCIAS", key="classico20"):
            with st.spinner("Analisando tendências..."):
                prompt = (
                    f"Explore o tema: {tema_radar}, no contexto do mercado de carros clássicos.\n"
                    f"Categoria/modelo de interesse: {categoria_radar or 'geral, sem foco específico'}.\n\n"
                    f"FORMATO:\n\n"
                    f"💎 {tema_radar.upper()}\n\n"
                    f"📊 ANÁLISE:\n[desenvolva o tema com base em padrões históricos conhecidos do mercado de clássicos]\n\n"
                    f"🚗 MODELOS/EXEMPLOS RELEVANTES:\n[liste exemplos concretos relacionados ao tema, com explicação breve de cada]\n\n"
                    f"💡 INSIGHT PARA O COLECIONADOR:\n[1-2 conclusões práticas]\n\n"
                    f"⚠️ LEMBRETE:\n[reforçar que são tendências históricas gerais, não previsões garantidas, e recomendar pesquisa em anúncios reais e tabelas especializadas]"
                )
                res = classicos_ia(prompt)
                salvar_consulta("Radar", tema_radar, res)
                st.session_state['radar_temp'] = res

        if st.session_state.get('radar_temp'):
            st.markdown(f"<div class='card-gold'>{st.session_state['radar_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['radar_temp'], file_name="radar_colecionador.txt", mime="text/plain",
        key="dl_classico_13"
    )

        # ========================
        # LINHA DO TEMPO
        # ========================

    with _tab_Timeline:
        st.header("🏁 Linha do Tempo")

        modelo_time = st.text_input("🚗 Modelo (sem ano específico):", value=st.session_state.veiculo_padrao.split(' ')[0] if st.session_state.veiculo_padrao else "", placeholder="ex: Fusca, Opala, Maverick...", key="ti_classico_111")

        if st.button("🏁 VER EVOLUÇÃO ANO A ANO", key="classico21"):
            if modelo_time.strip():
                with st.spinner("Montando linha do tempo..."):
                    prompt = (
                        f"Crie uma linha do tempo da evolução do modelo: {modelo_time}\n\n"
                        f"FORMATO:\n\n"
                        f"🏁 LINHA DO TEMPO — {modelo_time.upper()}\n\n"
                        f"[Para cada geração/período importante de mudança:]\n"
                        f"📅 [PERÍODO/ANOS]\n"
                        f"Principais mudanças: [motor, painel, lanternas, faróis, interior, suspensão, rodas, acabamentos — "
                        f"o que mudou especificamente nesse período]\n\n"
                        f"[Repita para todos os períodos relevantes da produção do modelo]\n\n"
                        f"🏆 GERAÇÃO MAIS DESEJADA PELOS COLECIONADORES:\n[qual período/ano é mais procurado e por quê]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Timeline", modelo_time, res)
                    st.session_state['timeline_temp'] = res
            else:
                st.warning("Informe o modelo.")

        if st.session_state.get('timeline_temp'):
            st.markdown(f"<div class='card'>{st.session_state['timeline_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['timeline_temp'], file_name="linha_do_tempo.txt", mime="text/plain",
        key="dl_classico_14"
    )

        # ========================
        # HISTÓRIA DO MODELO
        # ========================

    with _tab_Historia:
        st.header("🌎 História do Modelo")

        modelo_hist = st.text_input("🚗 Modelo:", value=st.session_state.veiculo_padrao.split(' ')[0] if st.session_state.veiculo_padrao else "", placeholder="ex: Fusca, Opala, Maverick...", key="ti_classico_112")

        if st.button("🌎 CONTAR A HISTÓRIA", key="classico22"):
            if modelo_hist.strip():
                with st.spinner("Reunindo a história..."):
                    prompt = (
                        f"Conte a história completa do modelo: {modelo_hist}\n\n"
                        f"FORMATO:\n\n"
                        f"🌎 A HISTÓRIA DO {modelo_hist.upper()}\n\n"
                        f"💡 ORIGEM DO PROJETO:\n[por que e como o veículo foi criado]\n\n"
                        f"🌍 CONTEXTO HISTÓRICO:\n[o que acontecia no mundo/país quando foi lançado]\n\n"
                        f"👨‍🔧 DESIGNERS E ENGENHEIROS:\n[pessoas-chave por trás do projeto, se conhecidas]\n\n"
                        f"🏁 SUCESSOS NAS PISTAS:\n[se aplicável, conquistas em corridas/rally]\n\n"
                        f"📺 PROPAGANDAS DA ÉPOCA:\n[como o veículo era anunciado, slogans marcantes]\n\n"
                        f"💡 CURIOSIDADES:\n[2-3 fatos pouco conhecidos]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Historia", modelo_hist, res)
                    st.session_state['hist_temp'] = res
            else:
                st.warning("Informe o modelo.")

        if st.session_state.get('hist_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['hist_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['hist_temp'], file_name="historia_modelo.txt", mime="text/plain",
        key="dl_classico_15"
    )

        # ========================
        # DIÁRIO DA RESTAURAÇÃO
        # ========================

    with _tab_Diario:
        st.header("🏕️ Diário da Restauração")
        st.markdown("Registre a evolução do seu projeto.")

        col1, col2 = st.columns(2)
        with col1:
            etapa_diario = st.text_input("🔧 Etapa/serviço realizado:", placeholder="ex: Troca do sistema de freios", key="ti_classico_113")
            gasto_diario = st.number_input("💰 Gasto nesta etapa (R$):", min_value=0.0, value=0.0, step=50.0, key="classico23")
        with col2:
            fornecedor_diario = st.text_input("🏪 Fornecedor/oficina (opcional):", placeholder="ex: Auto Peças Clássicas, Oficina do João...", key="ti_classico_114")
            horas_diario = st.number_input("⏱️ Horas trabalhadas:", min_value=0.0, value=0.0, step=0.5, key="classico24")

        notas_diario = st.text_area("📝 Notas sobre essa etapa:", height=100, placeholder="ex: Encontrei peças originais NOS, processo mais difícil do que esperado...", key="classico25")

        if st.button("📝 REGISTRAR NO DIÁRIO", key="classico26"):
            if etapa_diario.strip():
                st.session_state.diario_restauracao.append({
                    'data': datetime.now().strftime('%d/%m/%Y'),
                    'etapa': etapa_diario, 'gasto': gasto_diario, 'fornecedor': fornecedor_diario,
                    'horas': horas_diario, 'notas': notas_diario,
                })
                st.success("✅ Registrado no diário!")
                st.rerun()
            else:
                st.warning("Descreva a etapa.")

        if st.session_state.diario_restauracao:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            total_gasto = sum(e['gasto'] for e in st.session_state.diario_restauracao)
            total_horas = sum(e['horas'] for e in st.session_state.diario_restauracao)

            c1, c2, c3 = st.columns(3)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_restauracao)}</div><div>Etapas registradas</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>R${total_gasto:,.0f}</div><div>Gasto total</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_horas:.0f}h</div><div>Horas trabalhadas</div></div>", unsafe_allow_html=True)

            st.markdown("### 📖 Histórico de Etapas")
            for i, etapa in enumerate(reversed(st.session_state.diario_restauracao)):
                idx_real = len(st.session_state.diario_restauracao) - 1 - i
                with st.expander(f"🔧 {etapa['etapa']} — {etapa['data']} — R${etapa['gasto']:,.0f}"):
                    st.markdown(f"**Fornecedor:** {etapa.get('fornecedor','não informado')}")
                    st.markdown(f"**Horas trabalhadas:** {etapa.get('horas',0)}h")
                    if etapa.get('notas'):
                        st.markdown(f"**Notas:** {etapa['notas']}")
                    if st.button("🗑️ Remover", key=f"del_diario_{i}"):
                        st.session_state.diario_restauracao.pop(idx_real)
                        st.rerun()

            if st.button("🤖 GERAR RESUMO COMPLETO DO PROJETO", key="classico27"):
                with st.spinner("Gerando resumo..."):
                    etapas_txt = "\n".join([f"- {e['etapa']} ({e['data']}): R${e['gasto']:,.0f}, {e['horas']}h" for e in st.session_state.diario_restauracao])
                    prompt = (
                        f"Crie um resumo completo do projeto de restauração com base no histórico.\n"
                        f"Veículo: {st.session_state.veiculo_padrao}.\n"
                        f"Etapas registradas:\n{etapas_txt}\n"
                        f"Total gasto: R${total_gasto:,.2f}. Total horas: {total_horas}h.\n\n"
                        f"FORMATO:\n\n"
                        f"🏕️ RESUMO DO PROJETO DE RESTAURAÇÃO\n\n"
                        f"📊 VISÃO GERAL:\n[resumo do progresso até agora]\n\n"
                        f"💰 ANÁLISE DE CUSTOS:\n[comentário sobre o investimento até agora]\n\n"
                        f"📋 PRÓXIMAS ETAPAS SUGERIDAS:\n[com base no que já foi feito, o que tipicamente viria a seguir]\n\n"
                        f"🏆 VALOR AGREGADO ESTIMADO:\n[como esse investimento tende a impactar o valor do veículo — estimativa educativa]"
                    )
                    res = classicos_ia(prompt)
                    st.session_state['resumo_diario_temp'] = res

            if st.session_state.get('resumo_diario_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['resumo_diario_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar resumo (.txt)", data=st.session_state['resumo_diario_temp'], file_name="resumo_restauracao.txt", mime="text/plain",
        key="dl_classico_16"
    )

        # ========================
        # SOM ORIGINAL
        # ========================

    with _tab_Som:
        st.header("🔊 Som Original")

        veiculo_som = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_som")

        if st.button("🔊 DESCREVER SOM ORIGINAL", key="classico28"):
            if veiculo_som.strip():
                with st.spinner("Descrevendo..."):
                    prompt = (
                        f"Descreva como era o som/ronco original deste veículo: {veiculo_som}\n\n"
                        f"FORMATO:\n\n"
                        f"🔊 SOM ORIGINAL — {veiculo_som.upper()}\n\n"
                        f"🎵 CARACTERÍSTICA DO RONCO:\n[descrição sonora detalhada — grave, agudo, rítmico, etc]\n\n"
                        f"⚙️ CONFIGURAÇÃO DE FÁBRICA:\n[motor, escapamento original que geravam esse som]\n\n"
                        f"🔄 DIFERENÇAS ENTRE VERSÕES DE MOTOR:\n[se houver múltiplas opções de motor, como o som varia]\n\n"
                        f"🛠️ ESCAPAMENTOS ALTERNATIVOS DA ÉPOCA:\n[opções de escape esportivo que existiam para esse modelo]\n\n"
                        f"💡 CURIOSIDADE SONORA:\n[algo interessante sobre o som desse modelo específico]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("Som", veiculo_som, res)
                    st.session_state['som_temp'] = res
            else:
                st.warning("Informe o veículo.")

        if st.session_state.get('som_temp'):
            st.markdown(f"<div class='card'>{st.session_state['som_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['som_temp'], file_name="som_original.txt", mime="text/plain",
        key="dl_classico_17"
    )

        # ========================
        # QUIZ DO COLECIONADOR
        # ========================

    with _tab_Quiz:
        st.header("🧠 Quiz do Colecionador")
        st.markdown(f"Pontuação atual: **{st.session_state.quiz_pontuacao} pontos** | Nível: **{st.session_state.quiz_nivel_atual}**")

        nivel_quiz = st.selectbox("Escolha o nível:", ["Iniciante","Intermediário","Avançado","Especialista","Mestre do Antigomobilismo"], key="select_nivel_quiz")
        tema_quiz = st.text_input("Tema específico (opcional):", placeholder="ex: carros nacionais, motores, história geral...", key="ti_classico_115")

        if st.button("🧠 GERAR PERGUNTA", key="classico29"):
            with st.spinner("Preparando pergunta..."):
                prompt = (
                    f"Crie 1 pergunta de quiz sobre carros clássicos, nível {nivel_quiz}.\n"
                    f"Tema: {tema_quiz or 'geral'}.\n\n"
                    f"FORMATO:\n\n"
                    f"🧠 PERGUNTA ({nivel_quiz}):\n[a pergunta]\n\n"
                    f"A) [opção]\nB) [opção]\nC) [opção]\nD) [opção]\n\n"
                    f"✅ RESPOSTA CORRETA: [letra]\n"
                    f"📖 EXPLICAÇÃO: [por que essa é a resposta, com contexto interessante]"
                )
                res = classicos_ia(prompt)
                st.session_state['quiz_pergunta_temp'] = res
                st.session_state['quiz_respondido'] = False

        if st.session_state.get('quiz_pergunta_temp'):
            partes = st.session_state['quiz_pergunta_temp'].split('✅ RESPOSTA CORRETA')
            st.markdown(f"<div class='card'>{partes[0]}</div>", unsafe_allow_html=True)

            if not st.session_state.get('quiz_respondido'):
                if st.button("👁️ VER RESPOSTA", key="classico30"):
                    st.session_state['quiz_respondido'] = True
                    st.rerun()
            else:
                st.markdown(f"<div class='card-gold'>✅ RESPOSTA CORRETA{partes[1] if len(partes)>1 else ''}</div>", unsafe_allow_html=True)
                col_acertei, col_errei = st.columns(2)
                with col_acertei:
                    if st.button("✅ Acertei!", key="classico31"):
                        pontos = {"Iniciante":5,"Intermediário":10,"Avançado":15,"Especialista":20,"Mestre do Antigomobilismo":30}
                        st.session_state.quiz_pontuacao += pontos.get(nivel_quiz, 10)
                        st.session_state.quiz_nivel_atual = nivel_quiz
                        st.success(f"🎉 +{pontos.get(nivel_quiz,10)} pontos!")
                with col_errei:
                    if st.button("❌ Errei", key="classico32"):
                        st.info("Sem problema, vamos para a próxima!")

        # ========================
        # ENGENHARIA EXPLICADA
        # ========================

    with _tab_Engenharia:
        st.header("🔬 Engenharia Explicada")

        tema_eng = st.selectbox("Componente:", [
            "Carburador", "Distribuidor", "Suspensão", "Diferencial", "Câmbio (manual de época)",
            "Freios a tambor vs disco", "Direção mecânica/hidráulica", "Sistema elétrico de 6V vs 12V",
        ], key="select_tema_eng")

        if st.button("🔬 EXPLICAR", key="classico33"):
            with st.spinner("Preparando explicação..."):
                prompt = (
                    f"Explique de forma simples e visual: {tema_eng}, no contexto de carros clássicos.\n\n"
                    f"FORMATO:\n\n"
                    f"🔬 {tema_eng.upper()}\n\n"
                    f"📖 O QUE É E PARA QUE SERVE:\n[explicação simples]\n\n"
                    f"⚙️ COMO FUNCIONA:\n[explicação do mecanismo, passo a passo]\n\n"
                    f"🔧 PROBLEMAS COMUNS EM CLÁSSICOS:\n[o que tipicamente dá problema nesse componente em carros antigos]\n\n"
                    f"🛠️ MANUTENÇÃO BÁSICA:\n[cuidados que o proprietário pode ter]\n\n"
                    f"💡 CURIOSIDADE TÉCNICA:\n[1 fato interessante sobre a evolução desse componente]"
                )
                res = classicos_ia(prompt)
                salvar_consulta("Engenharia", tema_eng, res)
                st.session_state['eng_temp'] = res

        if st.session_state.get('eng_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['eng_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['eng_temp'], file_name="engenharia.txt", mime="text/plain",
        key="dl_classico_18"
    )

        # ========================
        # DNA DO AUTOMÓVEL
        # ========================

    with _tab_DNA:
        st.header("🧬 DNA do Automóvel")
        st.markdown("Uma viagem no tempo até a época em que seu clássico nasceu.")

        veiculo_dna = st.text_input("🚗 Modelo e ano:", value=st.session_state.veiculo_padrao, key="veiculo_dna")

        if st.button("🧬 VIAJAR NO TEMPO", key="classico34"):
            if veiculo_dna.strip():
                with st.spinner("Reconstruindo a época..."):
                    prompt = (
                        f"Reconstrua a época em que este veículo nasceu: {veiculo_dna}\n\n"
                        f"FORMATO:\n\n"
                        f"🧬 DNA — {veiculo_dna.upper()}\n\n"
                        f"📅 COMO ERA O BRASIL E O MUNDO NAQUELE ANO:\n[contexto histórico geral]\n\n"
                        f"💰 QUANTO CUSTAVA O CARRO NO LANÇAMENTO:\n[valor aproximado na época, em moeda da época]\n\n"
                        f"🏭 COMO FUNCIONAVA A FÁBRICA:\n[contexto da produção na época]\n\n"
                        f"📰 PRINCIPAIS ACONTECIMENTOS HISTÓRICOS DO ANO:\n[2-3 eventos marcantes]\n\n"
                        f"⛽ PREÇO DOS COMBUSTÍVEIS NA ÉPOCA:\n[contexto aproximado]\n\n"
                        f"🎵 MÚSICAS MAIS FAMOSAS DA ÉPOCA:\n[2-3 exemplos]\n\n"
                        f"🛣️ COMO ERAM AS ESTRADAS:\n[contexto da infraestrutura da época]\n\n"
                        f"🏁 PRINCIPAIS CONCORRENTES:\n[outros modelos que disputavam o mesmo mercado]\n\n"
                        f"📈 SALÁRIO MÍNIMO E PODER DE COMPRA:\n[contexto aproximado — quantos salários mínimos custava o carro]\n\n"
                        f"👨‍👩‍👧 PERFIL TÍPICO DO COMPRADOR:\n[quem comprava esse carro na época]"
                    )
                    res = classicos_ia(prompt)
                    salvar_consulta("DNA", veiculo_dna, res)
                    st.session_state['dna_temp'] = res
            else:
                st.warning("Informe o veículo.")

        if st.session_state.get('dna_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['dna_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['dna_temp'], file_name="dna_automovel.txt", mime="text/plain", use_container_width=True,
        key="dl_classico_19"
    )
            with col_sv:
                if st.button("❤️ Salvar", key="sv_dna", use_container_width=True):
                    st.session_state.consultas_salvas.append({'modulo':'DNA','tema':veiculo_dna if 'veiculo_dna' in dir() else '','conteudo':st.session_state['dna_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # CONSULTOR 24 HORAS
        # ========================

    with _tab_Consultor:
        st.header("🤖 Consultor 24 Horas")
        st.markdown("Pergunte qualquer coisa sobre qualquer carro antigo.")

        if 'chat_consultor' not in st.session_state:
            st.session_state.chat_consultor = []
        if 'consultor_key' not in st.session_state:
            st.session_state.consultor_key = 0

        if st.session_state.chat_consultor:
            for msg in st.session_state.chat_consultor:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FEF3E2;border:1px solid #B45309;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>🚗 Consultor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#FEF3E2;border:1px dashed #B45309;border-radius:12px;padding:16px;text-align:center;">
            🤖 <strong>Pergunte qualquer coisa!</strong> Ex: "Qual a diferença entre o Maverick GT e o Maverick comum?",
            "Vale a pena trocar o carburador original por injeção eletrônica?"
            </div>""", unsafe_allow_html=True)

        pergunta_consultor = st.text_input("Sua pergunta:", key=f"consultor_input_{st.session_state.consultor_key}", placeholder="Pergunte qualquer coisa sobre carros clássicos...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR", key="classico35"):
                if pergunta_consultor.strip():
                    with st.spinner("Consultando..."):
                        historico_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_consultor[-10:]]
                        resp = classicos_ia(pergunta_consultor, "Responda como um restaurador experiente, historiador e avaliador de mercado ao mesmo tempo. Seja didático e apaixonado.")
                    st.session_state.chat_consultor.append({"role": "user", "content": pergunta_consultor})
                    st.session_state.chat_consultor.append({"role": "assistant", "content": resp})
                    st.session_state.consultor_key += 1
                    salvar_consulta("Consultor", pergunta_consultor[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua pergunta.")
        with col_limpar:
            if st.button("🗑️ Limpar", key="classico36"):
                st.session_state.chat_consultor = []
                st.rerun()

        # ========================
        # BIBLIOTECA
        # ========================

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Clássicos IA — Especialista em Carros Antigos com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
