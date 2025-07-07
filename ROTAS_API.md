# API ENEM - Guia Completo de Rotas

Este documento descreve todas as rotas disponíveis na API de questões do ENEM, com exemplos práticos de uso.

## Base URL
```
http://localhost:3000
```

---

## 📋 1. Listar Questões

### Endpoint
```
GET /enem/questions
```

### Parâmetros de Query (todos opcionais)
| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `year` | number | Filtrar por ano específico | `2023` |
| `discipline` | string | Filtrar por disciplina | `matematica` |
| `language` | string | Filtrar por idioma | `ingles` |
| `page` | number | Página (padrão: 1) | `2` |
| `limit` | number | Itens por página (padrão: 10, máx: 100) | `20` |

### Exemplos de Requisições

#### 1. Buscar todas as questões (primeira página)
```bash
curl "http://localhost:3000/enem/questions"
```

#### 2. Buscar questões de 2023
```bash
curl "http://localhost:3000/enem/questions?year=2023"
```

#### 3. Buscar questões de matemática
```bash
curl "http://localhost:3000/enem/questions?discipline=matematica"
```

#### 4. Buscar questões de inglês
```bash
curl "http://localhost:3000/enem/questions?language=ingles"
```

#### 5. Buscar questões com paginação
```bash
curl "http://localhost:3000/enem/questions?page=2&limit=20"
```

#### 6. Buscar questões de matemática de 2023
```bash
curl "http://localhost:3000/enem/questions?year=2023&discipline=matematica"
```

### Resposta de Exemplo
```json
{
  "data": [
    {
      "id": 1,
      "title": "Questão 1 - ENEM 2023",
      "index": 1,
      "year": 2023,
      "context": "Como é bom reencontrar os leitores da _Revista da Cultura_...",
      "alternativesIntroduction": "O uso não padrão dos colchetes para nomear a revista...",
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
          "text": "Perfil de público-alvo, constituído por leitores exigentes...",
          "filePath": null,
          "isCorrect": false
        },
        {
          "letter": "B",
          "text": "Propósito do editor, chamando a atenção para o rigor normativo...",
          "filePath": null,
          "isCorrect": false
        },
        {
          "letter": "C",
          "text": "Exclusividade na seleção temática, direcionada para a área...",
          "filePath": null,
          "isCorrect": false
        },
        {
          "letter": "D",
          "text": "Identidade da revista, voltada para a recepção e a promoção...",
          "filePath": null,
          "isCorrect": true
        },
        {
          "letter": "E",
          "text": "Padrão editorial dos artigos, organizados em torno de uma proposta...",
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

---

## 🔍 2. Buscar Questão por ID

### Endpoint
```
GET /enem/questions/:id
```

### Parâmetros de URL
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | number | ID da questão |

### Exemplos de Requisições

#### Buscar questão com ID 1
```bash
curl "http://localhost:3000/enem/questions/1"
```

#### Buscar questão com ID 100
```bash
curl "http://localhost:3000/enem/questions/100"
```

### Resposta de Exemplo
```json
{
  "id": 1,
  "title": "Questão 1 - ENEM 2023",
  "index": 1,
  "year": 2023,
  "context": "Como é bom reencontrar os leitores da _Revista da Cultura_...",
  "alternativesIntroduction": "O uso não padrão dos colchetes para nomear a revista...",
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
      "text": "Perfil de público-alvo, constituído por leitores exigentes...",
      "filePath": null,
      "isCorrect": false
    },
    {
      "letter": "D",
      "text": "Identidade da revista, voltada para a recepção e a promoção...",
      "filePath": null,
      "isCorrect": true
    }
  ],
  "files": []
}
```

### Possíveis Erros
- `404 Not Found`: Questão não encontrada
```json
{
  "statusCode": 404,
  "message": "Question with ID 999 not found"
}
```

---

## 🎲 3. Questão Aleatória

### Endpoint
```
GET /enem/questions/random
```

### Parâmetros de Query (todos opcionais)
| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| `year` | number | Filtrar por ano específico | `2023` |
| `discipline` | string | Filtrar por disciplina | `matematica` |
| `language` | string | Filtrar por idioma | `ingles` |

### Exemplos de Requisições

#### 1. Questão aleatória (qualquer)
```bash
curl "http://localhost:3000/enem/questions/random"
```

#### 2. Questão aleatória de 2023
```bash
curl "http://localhost:3000/enem/questions/random?year=2023"
```

#### 3. Questão aleatória de matemática
```bash
curl "http://localhost:3000/enem/questions/random?discipline=matematica"
```

#### 4. Questão aleatória de inglês
```bash
curl "http://localhost:3000/enem/questions/random?language=ingles"
```

#### 5. Questão aleatória de matemática de 2023
```bash
curl "http://localhost:3000/enem/questions/random?year=2023&discipline=matematica"
```

### Resposta de Exemplo
```json
{
  "id": 150,
  "title": "Questão 150 - ENEM 2023",
  "index": 150,
  "year": 2023,
  "context": "Uma empresa de transporte...",
  "alternativesIntroduction": "Qual é o valor da função?",
  "correctAlternative": "C",
  "discipline": {
    "label": "Matemática e suas Tecnologias",
    "value": "matematica-tecnologias"
  },
  "language": null,
  "alternatives": [
    {
      "letter": "A",
      "text": "10",
      "filePath": null,
      "isCorrect": false
    },
    {
      "letter": "C",
      "text": "25",
      "filePath": null,
      "isCorrect": true
    }
  ],
  "files": []
}
```

---

## 📅 4. Listar Anos Disponíveis

### Endpoint
```
GET /enem/years
```

### Parâmetros
Nenhum parâmetro necessário.

### Exemplo de Requisição
```bash
curl "http://localhost:3000/enem/years"
```

### Resposta de Exemplo
```json
[2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009]
```

---

## 📚 5. Listar Disciplinas Disponíveis

### Endpoint
```
GET /enem/disciplines
```

### Parâmetros
Nenhum parâmetro necessário.

### Exemplo de Requisição
```bash
curl "http://localhost:3000/enem/disciplines"
```

### Resposta de Exemplo
```json
[
  {
    "label": "Ciências Humanas e suas Tecnologias",
    "value": "ciencias-humanas"
  },
  {
    "label": "Ciências da Natureza e suas Tecnologias",
    "value": "ciencias-natureza"
  },
  {
    "label": "Linguagens, Códigos e suas Tecnologias",
    "value": "linguagens-codigos"
  },
  {
    "label": "Matemática e suas Tecnologias",
    "value": "matematica"
  }
]
```

---

## 🌐 6. Listar Idiomas Disponíveis

### Endpoint
```
GET /enem/languages
```

### Parâmetros
Nenhum parâmetro necessário.

### Exemplo de Requisição
```bash
curl "http://localhost:3000/enem/languages"
```

### Resposta de Exemplo
```json
[
  {
    "label": "Espanhol",
    "value": "espanhol"
  },
  {
    "label": "Inglês",
    "value": "ingles"
  }
]
```

---

## 🔧 Exemplos com JavaScript/Fetch

### 1. Buscar questões de matemática
```javascript
async function buscarQuestoesMat() {
  try {
    const response = await fetch('http://localhost:3000/enem/questions?discipline=matematica-tecnologias&limit=5');
    const data = await response.json();
    console.log('Questões de matemática:', data);
  } catch (error) {
    console.error('Erro:', error);
  }
}
```

### 2. Buscar questão aleatória
```javascript
async function questaoAleatoria() {
  try {
    const response = await fetch('http://localhost:3000/enem/questions/random');
    const questao = await response.json();
    console.log('Questão aleatória:', questao);
  } catch (error) {
    console.error('Erro:', error);
  }
}
```

### 3. Buscar questão por ID
```javascript
async function buscarQuestaoPorId(id) {
  try {
    const response = await fetch(`http://localhost:3000/enem/questions/${id}`);
    if (!response.ok) {
      throw new Error(`Questão ${id} não encontrada`);
    }
    const questao = await response.json();
    console.log('Questão encontrada:', questao);
  } catch (error) {
    console.error('Erro:', error);
  }
}
```

---

## 🐍 Exemplos com Python

### 1. Buscar questões de 2023
```python
import requests

def buscar_questoes_2023():
    url = "http://localhost:3000/enem/questions"
    params = {"year": 2023, "limit": 10}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Encontradas {data['total']} questões de 2023")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro: {e}")
        return None
```

### 2. Questão aleatória de inglês
```python
import requests

def questao_aleatoria_ingles():
    url = "http://localhost:3000/enem/questions/random"
    params = {"language": "en"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        questao = response.json()
        print(f"Questão aleatória de inglês: {questao['title']}")
        return questao
    except requests.exceptions.RequestException as e:
        print(f"Erro: {e}")
        return None
```

---

## 📊 Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Parâmetros inválidos |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

---

## 🚀 Como Iniciar a API

```bash
# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run start:dev

# Executar em modo produção
npm run start:prod
```

A API estará disponível em `http://localhost:3000`

---

## 📝 Notas Importantes

1. **Paginação**: Por padrão, a API retorna 10 questões por página. Use `limit` e `page` para controlar a paginação.

2. **Filtros**: Todos os filtros podem ser combinados para buscar questões específicas.

3. **Disciplinas**: Use os valores exatos retornados pela rota `/enem/disciplines` para filtrar por disciplina.

4. **Idiomas**: Use os valores exatos retornados pela rota `/enem/languages` para filtrar por idioma.

5. **CORS**: A API está configurada para aceitar requisições de qualquer origem durante o desenvolvimento.

6. **Validação**: Todos os parâmetros são validados automaticamente. Parâmetros inválidos retornarão erro 400.

---

## 🔍 Estrutura de Dados

### Questão Completa
```typescript
interface Question {
  id: number;
  title: string;
  index: number;
  year: number;
  context?: string;
  alternativesIntroduction?: string;
  correctAlternative?: string;
  discipline?: {
    label: string;
    value: string;
  };
  language?: {
    label: string;
    value: string;
  };
  alternatives: Alternative[];
  files: string[];
}

interface Alternative {
  letter: string;
  text: string;
  filePath?: string;
  isCorrect: boolean;
}
```
