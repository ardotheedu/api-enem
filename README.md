# API ENEM

🎯 **API REST para acessar questões do ENEM com filtros avançados**

Esta API permite consultar questões do ENEM (Exame Nacional do Ensino Médio) com diversos filtros, paginação e busca aleatória. Construída com NestJS e SQLite.

## ✨ Funcionalidades

- 📚 **Buscar questões** com filtros por ano, disciplina e idioma
- 🎲 **Questões aleatórias** com filtros opcionais
- 📄 **Paginação** para grandes volumes de dados
- 🗂️ **Listar metadados** disponíveis (anos, disciplinas, idiomas)
- 🔍 **Buscar questão específica** por ID
- 🌐 **CORS habilitado** para uso em frontend
- ✅ **Validação de dados** com class-validator

## 🚀 Instalação e Execução

### Pré-requisitos

- Node.js (versão 18 ou superior)
- npm ou yarn

### Instalação

```bash
# Clonar repositório
git clone <url-do-repositorio>
cd api-enem

# Instalar dependências
npm install

# Verificar se o banco de dados existe
# O arquivo enem_questions.db deve estar na raiz do projeto
```

### Execução

```bash
# Modo desenvolvimento
npm run start:dev

# Modo produção
npm run build
npm run start:prod
```

A API estará disponível em `http://localhost:3000`

## 📋 Endpoints Disponíveis

### Listar Questões
```http
GET /enem/questions
```

**Parâmetros de Query:**
- `year` (number): Filtrar por ano
- `discipline` (string): Filtrar por disciplina
- `language` (string): Filtrar por idioma
- `page` (number): Página (padrão: 1)
- `limit` (number): Itens por página (padrão: 10, max: 100)

**Exemplos:**
```bash
# Questões de 2023
curl "http://localhost:3000/enem/questions?year=2023"

# Questões de matemática
curl "http://localhost:3000/enem/questions?discipline=matematica"

# Questões de inglês com paginação
curl "http://localhost:3000/enem/questions?language=en&page=2&limit=5"
```

### Buscar Questão por ID
```http
GET /enem/questions/:id
```

**Exemplo:**
```bash
curl "http://localhost:3000/enem/questions/2575"
```

### Questão Aleatória
```http
GET /enem/questions/random
```

**Parâmetros de Query:**
- `year` (number): Filtrar por ano
- `discipline` (string): Filtrar por disciplina
- `language` (string): Filtrar por idioma

**Exemplos:**
```bash
# Questão aleatória
curl "http://localhost:3000/enem/questions/random"

# Questão aleatória de matemática de 2023
curl "http://localhost:3000/enem/questions/random?year=2023&discipline=matematica"
```

### Metadados
```http
GET /enem/years          # Lista anos disponíveis
GET /enem/disciplines    # Lista disciplinas disponíveis
GET /enem/languages      # Lista idiomas disponíveis
```

## 📖 Exemplo de Resposta

```json
{
  "data": [
    {
      "id": 2575,
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
          "letter": "D",
          "text": "Alternativa D",
          "filePath": null,
          "isCorrect": true
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

## 🛠️ Tecnologias Utilizadas

- **NestJS** - Framework Node.js
- **SQLite** - Banco de dados
- **TypeScript** - Linguagem de programação
- **class-validator** - Validação de dados
- **class-transformer** - Transformação de dados

## 📁 Estrutura do Projeto

```
src/
├── enem/
│   ├── dto/
│   │   ├── filter.dto.ts      # DTO para filtros
│   │   └── question.dto.ts    # DTO para questões
│   ├── enem.controller.ts     # Controlador REST
│   ├── enem.service.ts        # Lógica de negócio
│   └── enem.module.ts         # Módulo NestJS
├── app.module.ts              # Módulo principal
└── main.ts                    # Arquivo de inicialização
```

## 🧪 Testando a API

Execute o arquivo de exemplos incluído:

```bash
node api-examples.js
```

## 📝 Documentação Completa

Consulte o arquivo `API_DOCUMENTATION.md` para documentação detalhada de todos os endpoints.

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

---

**Desenvolvido com ❤️ para facilitar o acesso às questões do ENEM**
  <!--[![Backers on Open Collective](https://opencollective.com/nest/backers/badge.svg)](https://opencollective.com/nest#backer)
  [![Sponsors on Open Collective](https://opencollective.com/nest/sponsors/badge.svg)](https://opencollective.com/nest#sponsor)-->

## Description

[Nest](https://github.com/nestjs/nest) framework TypeScript starter repository.

## Project setup

```bash
$ pnpm install
```

## Compile and run the project

```bash
# development
$ pnpm run start

# watch mode
$ pnpm run start:dev

# production mode
$ pnpm run start:prod
```

## Run tests

```bash
# unit tests
$ pnpm run test

# e2e tests
$ pnpm run test:e2e

# test coverage
$ pnpm run test:cov
```

## Deployment

When you're ready to deploy your NestJS application to production, there are some key steps you can take to ensure it runs as efficiently as possible. Check out the [deployment documentation](https://docs.nestjs.com/deployment) for more information.

If you are looking for a cloud-based platform to deploy your NestJS application, check out [Mau](https://mau.nestjs.com), our official platform for deploying NestJS applications on AWS. Mau makes deployment straightforward and fast, requiring just a few simple steps:

```bash
$ pnpm install -g @nestjs/mau
$ mau deploy
```

With Mau, you can deploy your application in just a few clicks, allowing you to focus on building features rather than managing infrastructure.

## Resources

Check out a few resources that may come in handy when working with NestJS:

- Visit the [NestJS Documentation](https://docs.nestjs.com) to learn more about the framework.
- For questions and support, please visit our [Discord channel](https://discord.gg/G7Qnnhy).
- To dive deeper and get more hands-on experience, check out our official video [courses](https://courses.nestjs.com/).
- Deploy your application to AWS with the help of [NestJS Mau](https://mau.nestjs.com) in just a few clicks.
- Visualize your application graph and interact with the NestJS application in real-time using [NestJS Devtools](https://devtools.nestjs.com).
- Need help with your project (part-time to full-time)? Check out our official [enterprise support](https://enterprise.nestjs.com).
- To stay in the loop and get updates, follow us on [X](https://x.com/nestframework) and [LinkedIn](https://linkedin.com/company/nestjs).
- Looking for a job, or have a job to offer? Check out our official [Jobs board](https://jobs.nestjs.com).

## Support

Nest is an MIT-licensed open source project. It can grow thanks to the sponsors and support by the amazing backers. If you'd like to join them, please [read more here](https://docs.nestjs.com/support).

## Stay in touch

- Author - [Kamil Myśliwiec](https://twitter.com/kammysliwiec)
- Website - [https://nestjs.com](https://nestjs.com/)
- Twitter - [@nestframework](https://twitter.com/nestframework)

## License

Nest is [MIT licensed](https://github.com/nestjs/nest/blob/master/LICENSE).
