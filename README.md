
# 🛡️ Escudo Digital | Digital Shield

> Sistema inteligente para ajudar idosos a identificar fake news, golpes digitais e conteúdos suspeitos.
>
> Intelligent system designed to help older adults identify fake news, online scams, and suspicious content.

---

# 🇧🇷 Português

## 📖 Sobre o Projeto

O Escudo Digital é uma solução desenvolvida para auxiliar idosos na identificação de fake news, golpes digitais e conteúdos suspeitos utilizando Inteligência Artificial.

A plataforma permite que o usuário envie mensagens, links e imagens para análise automática, recebendo uma classificação simples e visual que facilita a tomada de decisão e reduz os riscos de fraudes digitais.

O projeto busca promover inclusão digital, segurança da informação e autonomia para pessoas da terceira idade.

---

## 🎯 Objetivos

- Identificar possíveis fake news;
- Detectar golpes digitais;
- Analisar mensagens suspeitas;
- Verificar links potencialmente perigosos;
- Analisar imagens e capturas de tela;
- Auxiliar idosos na navegação segura pela internet.

---

## 🚦 Classificação de Risco

| Cor         | Classificação           |
| ----------- | ------------------------- |
| 🟢 Verde    | Conteúdo seguro          |
| 🟡 Amarelo  | Conteúdo suspeito        |
| 🔴 Vermelho | Possível golpe detectado |

---

## ✨ Funcionalidades

- 📩 Análise de mensagens de texto;
- 🔗 Verificação de links;
- 🖼️ Análise de imagens e prints;
- 🤖 Classificação utilizando Inteligência Artificial;
- 🚦 Feedback visual simplificado;
- 👨‍👩‍👧 Funcionalidade "Anjo da Guarda";
- 📱 Interface amigável para dispositivos móveis.

---

## 🏗️ Arquitetura

```text
Usuário
 │
 ▼
Interface Web
 │
 ▼
API Flask
 │
 ├── Análise de Texto
 ├── Análise de Links
 └── Análise de Imagens
          │
          ▼
      Motor de IA
          │
          ▼
 Classificação de Risco
          │
          ▼
      Resultado
```

---

## 🛠️ Tecnologias Utilizadas

### Linguagem

- Python

### Frameworks

- Flask
- Streamlit

### Inteligência Artificial

- Scikit-Learn
- Processamento de Linguagem Natural (PLN)
- Visão Computacional

### Ferramentas

- GitHub
- Trello
- ChatGPT
- Google Gemini

---

## 📂 Estrutura do Projeto

```text
bot_fake_news/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
│
├── static/
├── templates/
├── tests/
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalação

### Clonar o repositório

```bash
git clone https://github.com/matheus-monteiro97/bot_fake_news.git
```

### Acessar o diretório

```bash
cd bot_fake_news
```

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente virtual

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar aplicação

```bash
python app.py
```

---

## 📋 Requisitos Funcionais

- Receber mensagens suspeitas;
- Receber links para análise;
- Receber imagens e capturas de tela;
- Classificar riscos;
- Exibir feedback visual;
- Notificar contatos de confiança.

---

## 🔒 Requisitos Não Funcionais

- Interface acessível;
- Fácil utilização;
- Compatibilidade com smartphones;
- Resposta rápida;
- Confiabilidade das análises.

---

## 🚀 Melhorias Futuras

- Integração com WhatsApp;
- Detecção de deepfakes;
- Histórico de análises;
- Dashboard para familiares;
- Aprimoramento contínuo dos modelos de IA.

---

## 👥 Equipe

- Charles Patriarca
- Claybson Pereira
- Daniel Tavares
- Gustavo José
- João Gabriel de Santana
- Matheus Monteiro
- Sabrina Ferreira

---

# 🇺🇸 English

## 📖 About the Project

Digital Shield is a solution created to help older adults identify fake news, online scams, and suspicious digital content using Artificial Intelligence.

The platform allows users to submit messages, links, and images for automatic analysis. The system provides a simple visual classification to help users make safer decisions and avoid digital fraud.

The project promotes digital inclusion, cybersecurity awareness, and greater independence for elderly users.

---

## 🎯 Goals

- Identify fake news;
- Detect online scams;
- Analyze suspicious messages;
- Verify dangerous links;
- Analyze images and screenshots;
- Help older adults browse the internet safely.

---

## 🚦 Risk Classification

| Color     | Classification         |
| --------- | ---------------------- |
| 🟢 Green  | Safe content           |
| 🟡 Yellow | Suspicious content     |
| 🔴 Red    | Possible scam detected |

---

## ✨ Features

- 📩 Text message analysis;
- 🔗 Link verification;
- 🖼️ Image and screenshot analysis;
- 🤖 AI-powered classification;
- 🚦 Simple visual feedback;
- 👨‍👩‍👧 "Guardian Angel" trusted contact feature;
- 📱 Mobile-friendly interface.

---

## 🏗️ Architecture

```text
User
 │
 ▼
Web Interface
 │
 ▼
Flask API
 │
 ├── Text Analysis
 ├── Link Analysis
 └── Image Analysis
          │
          ▼
      AI Engine
          │
          ▼
   Risk Classification
          │
          ▼
      Final Result
```

---

## 🛠️ Technologies

### Language

- Python

### Frameworks

- Flask
- Streamlit

### Artificial Intelligence

- Scikit-Learn
- Natural Language Processing (NLP)
- Computer Vision

### Tools

- GitHub
- Trello
- ChatGPT
- Google Gemini

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/matheus-monteiro97/bot_fake_news.git
```

### Enter the project folder

```bash
cd bot_fake_news
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

---

## 📋 Functional Requirements

- Receive suspicious messages;
- Receive links for analysis;
- Receive images and screenshots;
- Classify risk levels;
- Display visual feedback;
- Notify trusted contacts.

---

## 🔒 Non-Functional Requirements

- Accessible interface;
- Easy to use;
- Smartphone compatibility;
- Fast response time;
- Reliable analysis.

---

## 🚀 Future Improvements

- WhatsApp integration;
- Deepfake detection;
- Analysis history;
- Family dashboard;
- Continuous AI model improvement.

---

## 👥 Team

- Charles Patriarca
- Claybson Pereira
- Daniel Tavares
- Gustavo José
- João Gabriel de Santana
- Matheus Monteiro
- Sabrina Ferreira

---

## 🎓 Academic Project

Escudo Digital / Digital Shield was developed as an academic project focused on cybersecurity, digital inclusion, and Artificial Intelligence solutions for older adults.

The project aims to reduce financial and emotional risks caused by online scams and misinformation.
