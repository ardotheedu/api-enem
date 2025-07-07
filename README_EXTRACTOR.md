# Extrator de Questões do ENEM

Scripts Python para extrair questões do ENEM da pasta `quiz-items` e armazená-las em um banco de dados SQLite.

## Arquivos

- `extract_questions.py` - Script principal para extrair questões e criar o banco de dados
- `view_questions.py` - Script para consultar e visualizar dados do banco
- `requirements_extractor.txt` - Informações sobre dependências (não há dependências externas)

## Como usar

### 1. Extraindo questões

Execute o script principal para extrair todas as questões da pasta `quiz-items`:

```bash
python extract_questions.py
```

O script irá:
- Criar um banco de dados SQLite chamado `enem_questions.db`
- Extrair todas as questões de todos os anos disponíveis
- Organizar os dados em tabelas relacionais
- Exibir estatísticas ao final

### 2. Consultando questões

Use o script de visualização para consultar os dados:

```bash
python view_questions.py
```

## Estrutura do Banco de Dados

O banco de dados possui as seguintes tabelas:

### `exams`
- `id` - ID único do exame
- `title` - Título do exame (ex: "ENEM 2023")
- `year` - Ano do exame
- `created_at` - Data de criação

### `disciplines`
- `id` - ID único da disciplina
- `label` - Nome da disciplina (ex: "Matemática e suas Tecnologias")
- `value` - Valor da disciplina (ex: "matematica")
- `created_at` - Data de criação

### `languages`
- `id` - ID único do idioma
- `label` - Nome do idioma (ex: "Inglês")
- `value` - Valor do idioma (ex: "ingles")
- `created_at` - Data de criação

### `questions`
- `id` - ID único da questão
- `title` - Título da questão
- `index_number` - Número da questão no exame
- `year` - Ano do exame
- `discipline_id` - ID da disciplina (chave estrangeira)
- `language_id` - ID do idioma (chave estrangeira, nullable)
- `context` - Contexto/texto da questão
- `alternatives_introduction` - Introdução das alternativas
- `correct_alternative` - Letra da alternativa correta
- `created_at` - Data de criação

### `alternatives`
- `id` - ID único da alternativa
- `question_id` - ID da questão (chave estrangeira)
- `letter` - Letra da alternativa (A, B, C, D, E)
- `text` - Texto da alternativa
- `file_path` - Caminho do arquivo associado (nullable)
- `is_correct` - Se é a alternativa correta
- `created_at` - Data de criação

### `question_files`
- `id` - ID único do arquivo
- `question_id` - ID da questão (chave estrangeira)
- `file_path` - Caminho do arquivo
- `created_at` - Data de criação

## Exemplos de Uso do Visualizador

### Buscar questões por ano
```python
from view_questions import EnemQuestionViewer

viewer = EnemQuestionViewer()
questions = viewer.search_questions(year=2023, limit=5)
```

### Buscar questões por disciplina
```python
math_questions = viewer.search_questions(discipline="matematica", limit=10)
```

### Obter questão aleatória
```python
random_question = viewer.get_random_question()
viewer.print_question(random_question)
```

### Exportar questões para JSON
```python
viewer.export_questions_to_json("enem_2023.json", year=2023)
```

## Funcionalidades

✅ **Extração completa**: Extrai todas as questões de todos os anos disponíveis
✅ **Banco relacional**: Organiza dados em tabelas relacionais normalizadas
✅ **Busca avançada**: Permite buscar por ano, disciplina, idioma
✅ **Questões aleatórias**: Gera questões aleatórias para estudo
✅ **Exportação**: Exporta questões para JSON
✅ **Estatísticas**: Exibe estatísticas dos dados extraídos
✅ **Visualização**: Formata questões para visualização
✅ **Integridade**: Evita duplicatas e mantém integridade referencial

## Estrutura dos Dados Extraídos

Cada questão contém:
- Informações básicas (título, ano, índice)
- Disciplina e idioma (quando aplicável)
- Contexto da questão
- Alternativas com textos e arquivos
- Resposta correta
- Arquivos associados

## Requisitos

- Python 3.6 ou superior
- Bibliotecas padrão do Python (sqlite3, json, pathlib)
- Pasta `quiz-items` no diretório raiz

## Logs e Feedback

Os scripts fornecem feedback em tempo real:
- ✅ Operações bem-sucedidas
- ⚠️ Avisos sobre dados não encontrados
- ❌ Erros durante o processamento
- 📊 Estatísticas finais
