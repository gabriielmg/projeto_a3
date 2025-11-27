# Documentação do Aplicativo Foodsy

## 1. Introdução

O Foodsy é um aplicativo desenvolvido para facilitar a busca por restaurantes próximos ao usuário, com base na localização atual e no tipo de comida desejada. A solução foi criada para tornar o processo de escolha mais rápido, prático e intuitivo, reduzindo a necessidade de navegar em vários aplicativos ou sites.

---

## 2. Objetivo do Aplicativo

O objetivo principal do Foodsy é oferecer uma experiência simples e eficiente para encontrar restaurantes próximos, com filtros úteis e informações essenciais, como:

* Avaliação média (rating)
* Número de avaliações
* Distância
* Imagens do local
* Endereço e nome

Além disso, o app integra diretamente com o Google Maps para navegação.

---

## 3. Funcionalidades

### **3.1 Busca por tipo de comida ou restaurante**

O usuário digita o nome de um prato ou estabelecimento (ex.: pizza, sushi, hamburgueria) e recebe resultados próximos.

### **3.2 Detecção automática de localização**

O app solicita a localização do usuário para calcular a distância real entre ele e os restaurantes.

### **3.3 Filtros inteligentes**

* Melhor avaliados
* Mais populares (maior número de reviews)

### **3.4 Exibição de resultados**

Os resultados são apresentados em cartões contendo:

* Foto
* Nome
* Endereço
* Avaliação
* Número de reviews
* Distância em km

### **3.5 Navegação integrada**

Ao clicar em um restaurante, o app pergunta se o usuário deseja abrir o caminho no Google Maps.

### **3.6 Interface moderna**

Design inspirado em apps atuais como iFood, priorizando simplicidade e responsividade.

---

## 4. Arquitetura do Sistema

O sistema é dividido em duas partes principais:

### **4.1 Frontend (interface)**

Construído com:

* HTML
* CSS
* JavaScript

Responsável pela exibição, interação e envio das solicitações ao backend.

### **4.2 Backend (servidor)**

Construído em **Python (Flask)**.
Responsável por:

* Receber consultas
* Processar dados
* Consultar a API do Google Places
* Retornar informações tratadas para o frontend

---

## 5. Tecnologias Utilizadas

* **Flask (Python)**
* **Google Places API**
* **HTML5/CSS3**
* **JavaScript**
* **Geolocalização do navegador**
* **API de Fotos do Google**

---

## 6. Fluxo de Funcionamento

1. Usuário abre o app.
2. Permite o acesso à localização.
3. Digita o tipo de comida.
4. O app envia a busca ao servidor.
5. O backend consulta o Google Places.
6. Os restaurantes são retornados e exibidos.
7. O usuário pode aplicar filtros.
8. Ao clicar, escolhe abrir rota no Google Maps.

---

## 7. Estrutura de Arquivos

```
/foodsy
│
├── static/
│   ├── app.js
│   ├── style.css
│   └── images/
│       └── logo.png
│
├── templates/
│   └── index.html
│
├── app.py
├── .env (API KEY)
└── README.md
```

---

## 8. Dependências

### No backend (Python):

* flask
* requests
* python-dotenv

### Arquivo **requirements.txt** sugerido:

```
Flask==2.2.5
python-dotenv==1.0.0
requests==2.31.0
```

---

## 9. Como Executar o Projeto

### **9.1 Criar ambiente virtual (opcional)**

```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### **9.2 Instalar dependências**

```
pip install -r requirements.txt
```

### **9.3 Configurar API Key**

Criar arquivo **.env**:

```
API_KEY=SUA_GOOGLE_PLACES_API_KEY
```

### **9.4 Executar o servidor**

```
python app.py
```

O app estará disponível em:
**[http://localhost:5000](http://localhost:5000)**

---

## 10. Possíveis Melhorias Futuras

* Sistema próprio de avaliações
* Sistema de contas e login
* Painel de estabelecimentos
* Mapa integrado direto no app
* Histórico de buscas
* Recomendações personalizadas

---

## 11. Conclusão

O Foodsy é uma solução simples, mas poderosa, para ajudar usuários a encontrarem restaurantes próximos de forma rápida e eficiente. Sua interface intuitiva, aliada à integração com a API do Google Maps, torna o processo de descoberta muito mais prático. A arquitetura utilizada permite futuras melhorias e expansão sem dificuldade.

---

Fim da documentação.
