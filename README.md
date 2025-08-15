# Disparador de Mensagens PontoMais – TopFama

Sistema automatizado para envio de alertas de ponto via WhatsApp para gestores, processando relatórios do sistema PontoMais com inteligência e precisão.

---

## 📌 Índice

- [🎯 Visão Geral](#-visão-geral)
- [⚡ Principais Funcionalidades](#-principais-funcionalidades)
- [🛠️ Tecnologias](#️-tecnologias)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🚀 Como Executar](#-como-executar)
- [📊 Tipos de Relatório](#-tipos-de-relatório)
- [🔧 Configuração](#-configuração)
- [📱 Interface do Sistema](#-interface-do-sistema)
- [🧠 Lógica de Processamento](#-lógica-de-processamento)
- [📨 Sistema de Mensagens](#-sistema-de-mensagens)
- [🔍 Recursos Avançados](#-recursos-avançados)
- [🚨 Tratamento de Erros](#-tratamento-de-erros)
- [👥 Contribuição](#-contribuição)

---

## 🎯 Visão Geral

O **Disparador de Mensagens PontoMais** é uma solução completa que automatiza a comunicação de ocorrências de ponto entre RH e gestores. O sistema processa relatórios CSV do PontoMais, aplica regras de negócio inteligentes e envia mensagens personalizadas via WhatsApp para cada gestor responsável.

### 🌟 Diferenciais
- **Processamento Inteligente**: Reconhece e trata diferentes formatos de relatório
- **Mapeamento Automático**: Converte nomes de equipes inconsistentes em códigos padronizados
- **Filtragem Avançada**: Remove registros desnecessários (ex: sábados, faltas justificadas)
- **Interface Moderna**: Design responsivo com feedback visual em tempo real
- **Integração WhatsApp**: Conexão direta via Evolution API com QR Code

---

## ⚡ Principais Funcionalidades

### 🔄 Processamento de Dados
- Upload e validação de arquivos CSV
- Limpeza automática de dados (remoção de cabeçalhos/rodapés)
- Normalização de datas e formatação de campos
- Agrupamento inteligente por colaborador e data

### 📱 Conectividade WhatsApp
- Autenticação via QR Code em tempo real
- Monitoramento contínuo do status de conexão
- Envio de mensagens com delays configuráveis
- Sistema de logout integrado

### 🎛️ Interface Interativa
- Seleção de tipo de relatório (Auditoria/Ocorrências)
- Filtros configuráveis (ignorar sábados, modo debug)
- Seleção múltipla de equipes com busca
- Logs detalhados e estatísticas em tempo real

### 📊 Análise e Monitoramento
- Dashboard com métricas de envio
- Sistema de logs categorizados
- Modo debug para análise de dados processados
- Relatórios de sucesso/erro por equipe

---

## 🛠️ Tecnologias

### Backend
- **Python 3.10+** - Linguagem principal
- **Flask** - Framework web com Blueprint architecture
- **Pandas** - Processamento e análise de dados CSV
- **Requests** - Integração com APIs externas
- **Logging** - Sistema de logs estruturado

### Frontend
- **HTML5 Semântico** - Estrutura moderna e acessível
- **CSS3 Modular** - Estilos organizados por componente
- **JavaScript ES6+** - Módulos modernos e programação assíncrona
- **Fetch API** - Comunicação assíncrona com backend

### Integração
- **Evolution API** - Gateway para WhatsApp Business
- **Google Sheets API** - Carregamento de números de telefone
- **SMTP** - Envio de logs por email em caso de erro

---

## 📁 Estrutura do Projeto

```
topfama-pontomais/
│
├── 📁 app/                          # Código principal da aplicação
│   ├── __init__.py
│   ├── controller.py                # Lógica principal de processamento
│   ├── routes.py                    # Rotas da API Flask
│   │
│   ├── 📁 processamento/            # Módulos de processamento de dados
│   │   ├── csv_reader.py            # Leitura e validação de CSV
│   │   ├── csv_reader_ocorrencias.py # Leitor específico para ocorrências
│   │   ├── log.py                   # Sistema de logging
│   │   ├── mapear_gerencia.py       # Mapeamento inteligente de equipes
│   │   ├── motivos_ocorrencias.py   # Validação de motivos de ocorrência
│   │   └── ocorrencias_processor.py # Processador de relatório de ocorrências
│   │
│   ├── 📁 services/                 # Serviços externos
│   │   └── email_sender.py          # Envio de logs por email
│   │
│   └── 📁 whatsapp/                 # Integração WhatsApp
│       ├── enviar_mensagem.py       # Cliente da Evolution API
│       ├── mensagem.py              # Geração de mensagens personalizadas
│       └── numeros_equipes.py       # Carregamento de contatos
│
├── 📁 static/                       # Arquivos estáticos
│   ├── config.json                  # Configuração da Evolution API
│   │
│   ├── 📁 css/                      # Estilos modulares
│   │   ├── base.css                 # Estilos base e animações
│   │   ├── header.css               # Cabeçalho e branding
│   │   ├── whatsapp-status.css      # Card de status do WhatsApp
│   │   ├── qr-code.css              # Seção de QR Code
│   │   ├── connection-message.css   # Mensagens de conexão
│   │   ├── main-content.css         # Layout principal
│   │   ├── forms.css                # Formulários e inputs
│   │   ├── dropdown.css             # Componentes dropdown
│   │   ├── logs.css                 # Sistema de logs
│   │   ├── stats.css                # Estatísticas e métricas
│   │   └── responsive.css           # Responsividade mobile
│   │
│   └── 📁 js/                       # Scripts modulares
│       ├── main.js                  # Inicialização da aplicação
│       ├── config.js                # Carregamento de configurações
│       ├── api.js                   # Comunicação com backend
│       ├── whatsapp.js              # Integração WhatsApp
│       ├── eventos.js               # Gerenciamento de eventos
│       ├── dropdown.js              # Lógica dos dropdowns
│       ├── dragdrop.js              # Funcionalidade drag & drop
│       ├── ui.js                    # Atualizações da interface
│       ├── helpers.js               # Funções auxiliares
│       └── tipo-dropdown.js         # Dropdown de tipo de relatório
│
├── 📁 templates/                    # Templates HTML
│   └── index.html                   # Interface principal
│
├── 📁 log/                          # Diretório de logs (criado automaticamente)
├── 📁 uploads/                      # Uploads temporários (criado automaticamente)
│
├── main.py                          # Ponto de entrada da aplicação
├── .env                             # Variáveis de ambiente
├── requirements.txt                 # Dependências Python
└── README.md                        # Este arquivo
```

---

## 🚀 Como Executar

### 1️⃣ Pré-requisitos
```bash
# Python 3.10 ou superior
python --version

# Git (para clonar o repositório)
git --version
```

### 2️⃣ Instalação
```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd topfama-pontomais

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3️⃣ Configuração

Criar arquivo `.env` na raiz do projeto:
```env
# Evolution API (WhatsApp Gateway)
EVOLUTION_URL=http://192.168.99.41:8080
EVOLUTION_INSTANCE=Teste
EVOLUTION_TOKEN=T0pF4m4D3vs

# Google Sheets (Números das equipes)
PLANILHA_EQUIPES_URL=https://docs.google.com/spreadsheets/d/.../export?format=csv

# Email (Logs de erro)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seuemail@topfama.com
EMAIL_PASS=suasenha
EMAIL_TO=dev@topfama.com
```

Configurar `static/config.json`:
```json
{
  "EVOLUTION_URL": "http://192.168.99.41:8080",
  "EVOLUTION_INSTANCE": "Teste",
  "EVOLUTION_TOKEN": "T0pF4m4D3vs"
}
```

### 4️⃣ Execução
```bash
python main.py
```

Acesse: `http://localhost:5000`

---

## 📊 Tipos de Relatório

### 🔍 Relatório de Auditoria
**Arquivo**: Exportação padrão de ocorrências do PontoMais
**Estrutura**: 
- Ignora 3 primeiras linhas (cabeçalho)
- Ignora 12 últimas linhas (rodapé)
- Colunas: `Nome`, `Equipe`, `Data`, `Ocorrência`, `Valor`

**Ocorrências Tratadas**:
- ✅ **Falta**: Faltas não justificadas
- ✅ **Horas Faltantes**: Devem ser > 1 hora
- ✅ **Horas Extras**: Devem ser > 2 horas
- ✅ **Mais de 6 dias consecutivos**: Alerta para folgas
- ✅ **Interjornada insuficiente**: < 11h entre expedientes
- ✅ **Intrajornada insuficiente**: Pausa de almoço < 1h

**Filtros Especiais**:
- Remove faltas "abonadas" ou "justificadas"
- Opção de ignorar registros de sábado
- Combina "falta" + "horas faltantes" em mensagem única

### ⚠️ Relatório de Ocorrências
**Arquivo**: Relatório específico de ocorrências pendentes
**Estrutura**:
- Ignora 4 primeiras linhas
- Ignora 5 últimas linhas
- Colunas: `Nome`, `Equipe`, `Data`, `Motivo`, `Ação pendente`

**Motivos Válidos**:
- "Número de pontos menor que o previsto"
- "Possui pontos durante exceção"
- "Número errado de pontos"

**Ações Válidas**:
- "Colaborador solicitar ajuste"
- "Gestor aprovar solicitação de ajuste"
- "Gestor corrigir lançamento de exceção"

---

## 🔧 Configuração

### 🗺️ Mapeamento de Equipes
O sistema converte automaticamente nomes inconsistentes em códigos padronizados:

```python
# Exemplos de mapeamento
"Departamento Pessoal" → "DP"
"CD10", "CD 10", "cd-10" → "CD10"
"Loja 75", "Loja l 75", "Filial Nova 75" → "75"
"Gente e Gestão" → "RH"
"Logística" → "Produtos"
```

### 📞 Números das Equipes
Carregados automaticamente via Google Sheets:
- Coluna 1: Nome da equipe
- Coluna 2: Número do WhatsApp (formato brasileiro)
- Limpeza automática: remove prefixos internacionais
- Validação: números devem ter 10-12 dígitos

### 🎨 Templates de Mensagens
Personalizados por tipo de ocorrência:
```python
TEMPLATES = {
    "Falta": "*{nome}* _faltou_. Por favor *justificar*.",
    "Horas Faltantes": "*{nome}* ficou devendo *{horas}*. Por favor *justificar*.",
    "Horas extras": "*{nome}* fez mais de 2 horas extras. _Total_: *{valor}*. Por favor *ajustar*."
}
```

---

## 📱 Interface do Sistema

### 🔐 Conexão WhatsApp
1. **Status em Tempo Real**: Monitora conexão Evolution API
2. **QR Code Dinâmico**: Atualizado automaticamente
3. **Informações do Perfil**: Nome, número e foto do WhatsApp conectado
4. **Logout Integrado**: Desconexão segura com um clique

### 📤 Upload de Arquivos
- **Drag & Drop**: Arrastar arquivo diretamente na interface
- **Validação**: Aceita apenas arquivos .CSV
- **Preview**: Mostra nome do arquivo selecionado
- **Análise Prévia**: Carrega equipes disponíveis automaticamente

### ⚙️ Configurações
- **Tipo de Relatório**: Dropdown inteligente (Auditoria/Ocorrências)
- **Ignorar Sábados**: Checkbox para filtrar registros de fim de semana
- **Modo Debug**: Exibe dados processados para análise
- **Seleção de Equipes**: Dropdown multiselect com busca

### 📊 Monitoramento
- **Logs em Tempo Real**: Coloridos por tipo (sucesso/erro/warning/info)
- **Barra de Progresso**: Indica status do processamento
- **Estatísticas**: Contadores de mensagens, equipes, sucessos e erros
- **Panel Debug**: Dados JSON processados (modo desenvolvedor)

---

## 🧠 Lógica de Processamento

### 1️⃣ Carregamento e Validação
```python
def carregar_dados(caminho_csv, ignorar_sabados, tipo_relatorio):
    # Carrega CSV removendo linhas de cabeçalho/rodapé
    # Aplica filtros específicos por tipo de relatório
    # Normaliza colunas e formatos de data
    # Remove registros inválidos
```

### 2️⃣ Limpeza e Transformação
```python
# Normalização de dados
df.columns = df.columns.str.strip()
df.rename(columns={"Funcionário": "Nome", "Data do ponto": "Data"})

# Filtros especiais para sábados
if ignorar_sabados:
    # Remove "Falta" em sábados
    # Remove "Horas Faltantes" = 04:00 em sábados
```

### 3️⃣ Mapeamento de Equipes
```python
def mapear_equipe(txt):
    # Corrige erros comuns: "Loja l 66" → "Loja 66"
    # Identifica padrões com regex
    # Aplica regras de negócio específicas
    # Retorna código padronizado
```

### 4️⃣ Geração de Mensagens
```python
def gerar_mensagem(grupo):
    # Agrupa por Nome + Data
    # Identifica combinações especiais (falta + horas faltantes)
    # Aplica templates personalizados
    # Remove duplicatas e mensagens desnecessárias
```

### 5️⃣ Envio e Controle
```python
def enviar_whatsapp(numero, mensagem, equipe):
    # Formata número brasileiro
    # Envia via Evolution API
    # Aplica delays entre mensagens
    # Registra logs detalhados
```

---

## 📨 Sistema de Mensagens

### 🎯 Mensagem Final Formatada
```
*LOJA 75*

*NO DIA 05/07/2025:*
• João Silva _faltou_. Por favor *justificar*.
• Maria Santos ficou devendo *2:30 horas*. Por favor *justificar*.

*NO DIA 06/07/2025:*
• Pedro Costa fez mais de 2 horas extras. _Total_: *3:15*. Por favor *ajustar*.
```

### ⚡ Regras Inteligentes
- **Combinação Falta + Horas Faltantes**: Unifica em mensagem única
- **Filtro de Tempo**: Horas faltantes < 1h são ignoradas
- **Faltas Justificadas**: Não geram alertas
- **Deduplicação**: Remove mensagens idênticas
- **Ordenação**: Mensagens ordenadas por data

### 📞 Controle de Envio
- **Rate Limiting**: Delay de 4-8 segundos entre mensagens
- **Retry Logic**: Reenvio automático em caso de falha
- **Validação de Número**: Números inválidos são rejeitados
- **Logs Detalhados**: Sucesso/erro por equipe

---

## 🔍 Recursos Avançados

### 🔄 Processamento Assíncrono
- Interface responsiva durante processamento
- Feedback visual em tempo real
- Cancelamento seguro de operações
- Manutenção de estado da aplicação

### 📊 Analytics Integrado
```python
stats = {
    "total": 15,           # Total de equipes processadas
    "equipes": 12,         # Equipes únicas
    "sucesso": 10,         # Envios bem-sucedidos  
    "erro": 2              # Falhas de envio
}
```

### 🎨 Interface Adaptativa
- **Design Responsivo**: Funciona em desktop/tablet/mobile
- **Tema Corporativo**: Cores e branding TopFama
- **Animações Suaves**: Transições e micro-interações
- **Acessibilidade**: Semântica HTML e contraste adequado

### 🔐 Segurança e Privacidade
- Upload temporário com limpeza automática
- Logs com dados sensíveis mascarados
- Conexão HTTPS obrigatória em produção
- Tokens de API em variáveis de ambiente

---

## 🚨 Tratamento de Erros

### 📧 Sistema de Alertas
Em caso de erro crítico, o sistema:
1. Captura stacktrace completo
2. Envia log por email para desenvolvedores
3. Remove arquivos temporários
4. Exibe mensagem amigável ao usuário

### 🔍 Logs Detalhados
```python
# Exemplo de log estruturado
logging.info(">>> Iniciando processamento CSV: arquivo.csv")
logging.info(">>> Parâmetros: ignorar_sabados=True, tipo=Auditoria")
logging.info("🧪 Colunas carregadas: ['Nome', 'Equipe', 'Data', 'Ocorrência', 'Valor']")
logging.error("❌ Falha ao enviar para LOJA 75: Timeout na API")
```

### 🛡️ Validações Robustas
- **Formato de Arquivo**: Apenas .CSV aceitos
- **Estrutura de Dados**: Validação de colunas obrigatórias
- **Conexão API**: Retry automático e timeout configurável
- **Números de Telefone**: Formatação e validação brasileira

---

## 👥 Contribuição

### 🔧 Desenvolvimento Local
```bash
# Ativar modo debug
export FLASK_ENV=development

# Executar com reload automático
python main.py
```

### 📝 Padrões de Código
- **Python**: PEP 8, type hints quando aplicável
- **JavaScript**: ES6+, módulos nativos, async/await
- **CSS**: BEM methodology, variáveis CSS customizadas
- **Commits**: Conventional commits (feat:, fix:, docs:)

### 🧪 Testing
```bash
# Modo debug habilitado
curl -X POST -F "debugMode=true" -F "csvFile=@test.csv" localhost:5000/enviar

# Logs detalhados em /log/
tail -f log/log_execucao_*.log
```

### 🚀 Deploy
1. Configurar variáveis de ambiente de produção
2. Usar servidor WSGI (Gunicorn, uWSGI)
3. Configurar reverse proxy (Nginx)
4. Monitorar logs em produção

---

## 📄 Licença

**Uso Exclusivo TopFama**  
Este projeto é propriedade da TopFama e destinado exclusivamente para uso interno.

---

## 🌟 Créditos

**Desenvolvido por**: Bruno di Luca  
**Equipe**: TopFama Technology & Operations  
**Contato**: bruno@grupotopfama.com.br  

---

*"Automatizando processos, humanizando relações."* 🚀