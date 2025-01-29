# RPA Consulta CNPJ 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  
Solução de automação para consulta em massa de CNPJs via API BrasilAPI. Processa planilhas Excel e retorna dados cadastrais atualizados.

![Interface Moderna](https://via.placeholder.com/800x400.png?text=Interface+Moderno+RPA+Consulta+CNPJ)

---

## 📦 Instalação Rápida

```bash
git clone https://github.com/seu-usuario/rpa-consulta-cnpj.git
cd rpa-consulta-cnpj
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

---

🚀 Como Executar

python app.py

Acesse: http://localhost:5000

---

🛠 Fluxo de Trabalho

sequenceDiagram
    Usuário->>+Aplicação: Envia planilha .xlsx
    Aplicação->>+API: Consulta CNPJ 1
    API-->>-Aplicação: Retorna dados
    Aplicação->>+API: Consulta CNPJ 2
    API-->>-Aplicação: Retorna dados
    Aplicação->>Usuário: Disponibiliza download

---

📂 Estrutura do Código

rpa-consulta-cnpj/
├── app.py                 # Core da aplicação
├── config/
│   ├── constants.py       # Configurações globais
│   └── api_endpoints.py   # URLs de APIs
├── services/
│   ├── excel_handler.py   # Manipulação de Excel
│   └── api_service.py     # Comunicação com APIs
├── static/
│   ├── css/               # Estilos customizados
│   └── js/                # Scripts opcionais
└── templates/
    ├── index.html         # Interface principal
    └── processing.html    # Tela de processamento

---

⚙️ Especificações Técnicas

Componente	Detalhes
Taxa de Consultas	~3 consultas/segundo
Limite de Arquivo	16MB (configurável)
Timeout	20 segundos por consulta
Retentativas	3 tentativas automáticas
Logs	Registro em console e arquivo

---

📄 Modelo de Planilha

Coluna	Exemplo	Obrigatório
RAZÃO SOCIAL	Empresa XYZ LTDA	Sim
CNPJ	00123456000195	Sim
SITUAÇÃO CADASTRAL	ATIVA	Não
CNAE	6202-3/00	Não
PORTE	MEI	

---

🛑 Limitações Conhecidas

Dependência total da disponibilidade da BrasilAPI

Não suporta CNPJs mal formatados (ex: com caracteres especiais)

Limite de 1000 linhas por execução (configurável no código)

---

📌 Melhorias Futuras

Sistema de filas com Redis

Dashboard de progresso em tempo real

Suporte a múltiplos formatos (CSV, JSON)

Integração com outras APIs (Receita WS, Sintegra)

---

# Testes Automatizados
pytest tests/

# Exemplo de Consulta Unitária
from services.api_service import consultar_cnpj
cnpj = "00123456000195"
dados = consultar_cnpj(cnpj)
print(dados['porte'])  # Retorna: MEI

---

Licença MIT - Consulte LICENSE para detalhes completos.
Versão: 1.0.0 - Atualizado em 15/03/2024

---

Este arquivo README.md completo contém:  
✅ Instruções de instalação  
✅ Diagramas técnicos  
✅ Modelo de dados  
✅ Roadmap de melhorias  
✅ Exemplos de código  

Salve como `README.md` na raiz do projeto! 😊