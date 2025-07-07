# API ENEM - Documentação

API REST para acessar questões do ENEM com filtros avançados.

## Endpoints Disponíveis

### 1. Listar Questões
```
GET /enem/questions
```

**Parâmetros de Query:**
- `year` (number, opcional): Filtrar por ano específico
- `discipline` (string, opcional): Filtrar por disciplina
- `language` (string, opcional): Filtrar por idioma
- `page` (number, opcional): Página para paginação (padrão: 1)
- `limit` (number, opcional): Limite de questões por página (padrão: 10, máximo: 100)

**Exemplo de Resposta:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Questão 1 - ENEM 2023",
      "index": 1,
      "year": 2023,
      "context": "Texto da questão...",
      "alternativesIntroduction": "Introdução das alternativas...",
      "correctAlternative": "D",
      "discipline": {
        "label": "Linguagens, Códigos e suas Tecnologias",
        "value": "linguagens-codigos-tecnologias"
      },
      "language": {
        "label": "Português",
        "value": "pt"
      },
      "alternatives": [
        {
          "letter": "A",
          "text": "Alternativa A",
          "filePath": null,
          "isCorrect": false
        },
        {
          "letter": "B",
          "text": "Alternativa B",
          "filePath": null,
          "isCorrect": false
        },
        {
          "letter": "C",
          "text": "Alternativa C",
          "filePath": null,
          "isCorrect": false
        },
        {
          "letter": "D",
          "text": "Alternativa D",
          "filePath": null,
          "isCorrect": true
        },
        {
          "letter": "E",
          "text": "Alternativa E",
          "filePath": null,
          "isCorrect": false
        }
      ],
      "files": []
    }
  ],
  "total": 183,
  "page": 1,
  "limit": 10,
  "totalPages": 19
}
```

### 2. Buscar Questão por ID
```
GET /enem/questions/:id
```

**Parâmetros:**
- `id` (number): ID da questão

**Exemplo de Resposta:**
```json
{
  "id": 1,
  "title": "Questão 1 - ENEM 2023",
  "index": 1,
  "year": 2023,
  "context": "Texto da questão...",
  "alternativesIntroduction": "Introdução das alternativas...",
  "correctAlternative": "D",
  "discipline": {
    "label": "Linguagens, Códigos e suas Tecnologias",
    "value": "linguagens-codigos-tecnologias"
  },
  "language": {
    "label": "Português",
    "value": "pt"
  },
  "alternatives": [...],
  "files": []
}
```

### 3. Questão Aleatória
```
GET /enem/questions/random
```

**Parâmetros de Query:**
- `year` (number, opcional): Filtrar por ano específico
- `discipline` (string, opcional): Filtrar por disciplina
- `language` (string, opcional): Filtrar por idioma

**Exemplo de Resposta:** Mesma estrutura da busca por ID

### 4. Listar Anos Disponíveis
```
GET /enem/years
```

**Exemplo de Resposta:**
```json
[2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009]
```

### 5. Listar Disciplinas Disponíveis
```
GET /enem/disciplines
```

**Exemplo de Resposta:**
```json
[
  {
    "label": "Ciências da Natureza e suas Tecnologias",
    "value": "ciencias-natureza-tecnologias"
  },
  {
    "label": "Ciências Humanas e suas Tecnologias",
    "value": "ciencias-humanas-tecnologias"
  },
  {
    "label": "Linguagens, Códigos e suas Tecnologias",
    "value": "linguagens-codigos-tecnologias"
  },
  {
    "label": "Matemática e suas Tecnologias",
    "value": "matematica-tecnologias"
  }
]
```

### 6. Listar Idiomas Disponíveis
```
GET /enem/languages
```

**Exemplo de Resposta:**
```json
[
  {
    "label": "Espanhol",
    "value": "es"
  },
  {
    "label": "Inglês",
    "value": "en"
  },
  {
    "label": "Português",
    "value": "pt"
  }
]
```

## Exemplos de Uso

### Buscar questões de 2023
```
GET /enem/questions?year=2023
```

### Buscar questões de matemática
```
GET /enem/questions?discipline=matematica-tecnologias
```

### Buscar questões de inglês de 2023
```
GET /enem/questions?year=2023&language=en
```

### Buscar questões com paginação
```
GET /enem/questions?page=2&limit=20
```

### Questão aleatória de matemática
```
GET /enem/questions/random?discipline=matematica-tecnologias
```

## Códigos de Erro

- `400 Bad Request`: Parâmetros inválidos
- `404 Not Found`: Questão não encontrada
- `500 Internal Server Error`: Erro interno do servidor

## Executar a API

```bash
# Instalar dependências
npm install

# Executar em modo de desenvolvimento
npm run start:dev

# Executar em modo de produção
npm run start:prod
```

A API estará disponível em `http://localhost:3000`
