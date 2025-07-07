# Exemplos Práticos de Uso da API ENEM

Este documento contém exemplos práticos de como usar a API em diferentes cenários reais.

## 🎯 Cenários de Uso

### 1. Criar um Quiz Interativo

```javascript
class QuizEnem {
  constructor() {
    this.baseURL = 'http://localhost:3000';
    this.questaoAtual = null;
    this.pontuacao = 0;
  }

  // Buscar questão aleatória de uma disciplina específica
  async buscarQuestaoAleatoria(disciplina = null, ano = null) {
    try {
      let url = `${this.baseURL}/enem/questions/random`;
      const params = new URLSearchParams();
      
      if (disciplina) params.append('discipline', disciplina);
      if (ano) params.append('year', ano);
      
      if (params.toString()) {
        url += `?${params.toString()}`;
      }

      const response = await fetch(url);
      const questao = await response.json();
      
      this.questaoAtual = questao;
      return questao;
    } catch (error) {
      console.error('Erro ao buscar questão:', error);
      return null;
    }
  }

  // Verificar resposta do usuário
  verificarResposta(letraEscolhida) {
    if (!this.questaoAtual) return false;
    
    const correto = this.questaoAtual.correctAlternative === letraEscolhida;
    if (correto) {
      this.pontuacao++;
    }
    
    return correto;
  }

  // Exemplo de uso
  async iniciarQuiz() {
    console.log('🎯 Iniciando Quiz ENEM - Matemática');
    
    for (let i = 0; i < 5; i++) {
      const questao = await this.buscarQuestaoAleatoria('matematica-tecnologias');
      
      if (questao) {
        console.log(`\n📝 Questão ${i + 1}: ${questao.title}`);
        console.log(`📖 ${questao.context || questao.alternativesIntroduction}`);
        
        questao.alternatives.forEach(alt => {
          console.log(`${alt.letter}) ${alt.text}`);
        });
        
        // Simular resposta (normalmente seria input do usuário)
        const respostasSimuladas = ['A', 'B', 'C', 'D', 'E'];
        const respostaUsuario = respostasSimuladas[Math.floor(Math.random() * 5)];
        
        const correto = this.verificarResposta(respostaUsuario);
        console.log(`\n✅ Resposta: ${respostaUsuario} | Correto: ${correto ? 'SIM' : 'NÃO'}`);
        console.log(`🎯 Resposta correta: ${questao.correctAlternative}`);
      }
    }
    
    console.log(`\n🏆 Quiz finalizado! Pontuação: ${this.pontuacao}/5`);
  }
}

// Usar o quiz
const quiz = new QuizEnem();
quiz.iniciarQuiz();
```

### 2. Sistema de Estudo por Disciplina

```javascript
class SistemaEstudo {
  constructor() {
    this.baseURL = 'http://localhost:3000';
    this.estatisticas = {
      questoesRespondidas: 0,
      acertos: 0,
      erros: 0,
      disciplinas: {}
    };
  }

  // Buscar questões de uma disciplina específica
  async buscarQuestoesDisciplina(disciplina, ano = null, quantidade = 10) {
    try {
      const params = new URLSearchParams({
        discipline: disciplina,
        limit: quantidade.toString()
      });
      
      if (ano) params.append('year', ano);
      
      const response = await fetch(`${this.baseURL}/enem/questions?${params}`);
      const data = await response.json();
      
      return data.data;
    } catch (error) {
      console.error('Erro ao buscar questões:', error);
      return [];
    }
  }

  // Listar todas as disciplinas disponíveis
  async listarDisciplinas() {
    try {
      const response = await fetch(`${this.baseURL}/enem/disciplines`);
      const disciplinas = await response.json();
      
      console.log('📚 Disciplinas disponíveis:');
      disciplinas.forEach((disc, index) => {
        console.log(`${index + 1}. ${disc.label} (${disc.value})`);
      });
      
      return disciplinas;
    } catch (error) {
      console.error('Erro ao listar disciplinas:', error);
      return [];
    }
  }

  // Estudar uma disciplina específica
  async estudarDisciplina(valorDisciplina) {
    const questoes = await this.buscarQuestoesDisciplina(valorDisciplina);
    
    if (questoes.length === 0) {
      console.log('❌ Nenhuma questão encontrada para esta disciplina');
      return;
    }

    console.log(`\n📖 Iniciando estudo - ${questoes[0].discipline.label}`);
    console.log(`📊 ${questoes.length} questões encontradas\n`);

    for (let i = 0; i < questoes.length; i++) {
      const questao = questoes[i];
      
      console.log(`${'='.repeat(60)}`);
      console.log(`📝 Questão ${i + 1}/${questoes.length}: ${questao.title}`);
      console.log(`📅 Ano: ${questao.year}`);
      
      if (questao.context) {
        console.log(`\n📖 Contexto:`);
        console.log(questao.context.substring(0, 200) + '...');
      }
      
      if (questao.alternativesIntroduction) {
        console.log(`\n❓ ${questao.alternativesIntroduction}`);
      }
      
      console.log(`\n📋 Alternativas:`);
      questao.alternatives.forEach(alt => {
        const marker = alt.isCorrect ? '✅' : '  ';
        console.log(`${marker} ${alt.letter}) ${alt.text.substring(0, 100)}...`);
      });
      
      console.log(`\n🎯 Resposta correta: ${questao.correctAlternative}`);
      console.log(`${'='.repeat(60)}\n`);
    }
  }
}

// Usar o sistema
const sistema = new SistemaEstudo();
sistema.listarDisciplinas().then(() => {
  sistema.estudarDisciplina('matematica-tecnologias');
});
```

### 3. Análise de Questões por Ano

```python
import requests
import matplotlib.pyplot as plt
from collections import Counter

class AnalisadorEnem:
    def __init__(self):
        self.base_url = "http://localhost:3000"
    
    def buscar_questoes_por_ano(self, ano, limite=200):
        """Busca questões de um ano específico"""
        url = f"{self.base_url}/enem/questions"
        params = {"year": ano, "limit": limite}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar questões: {e}")
            return None
    
    def analisar_distribuicao_disciplinas(self, ano):
        """Analisa a distribuição de questões por disciplina"""
        data = self.buscar_questoes_por_ano(ano)
        
        if not data:
            return
        
        disciplinas = []
        for questao in data['data']:
            if questao['discipline']:
                disciplinas.append(questao['discipline']['label'])
        
        contador = Counter(disciplinas)
        
        print(f"\n📊 Distribuição de questões por disciplina - ENEM {ano}")
        print("=" * 60)
        
        for disciplina, count in contador.most_common():
            print(f"{disciplina}: {count} questões")
        
        return contador
    
    def comparar_anos(self, anos):
        """Compara questões entre diferentes anos"""
        print(f"\n📈 Comparação entre os anos: {', '.join(map(str, anos))}")
        print("=" * 60)
        
        for ano in anos:
            data = self.buscar_questoes_por_ano(ano)
            if data:
                total = data['total']
                print(f"ENEM {ano}: {total} questões")
                
                # Analisar disciplinas
                disciplinas = []
                for questao in data['data']:
                    if questao['discipline']:
                        disciplinas.append(questao['discipline']['label'])
                
                contador = Counter(disciplinas)
                print(f"  Disciplinas mais frequentes:")
                for disc, count in contador.most_common(3):
                    print(f"    - {disc}: {count}")
                print()

# Usar o analisador
analisador = AnalisadorEnem()
analisador.analisar_distribuicao_disciplinas(2023)
analisador.comparar_anos([2021, 2022, 2023])
```

### 4. Gerador de Simulados

```javascript
class GeradorSimulados {
  constructor() {
    this.baseURL = 'http://localhost:3000';
  }

  // Gerar simulado balanceado
  async gerarSimulado(configuracao = {}) {
    const {
      questoesPorDisciplina = 10,
      ano = null,
      incluirIdiomas = true
    } = configuracao;

    try {
      // Buscar disciplinas disponíveis
      const disciplinas = await this.buscarDisciplinas();
      const simulado = [];

      for (const disciplina of disciplinas) {
        console.log(`📚 Buscando questões de ${disciplina.label}...`);
        
        const questoes = await this.buscarQuestoesDisciplina(
          disciplina.value, 
          questoesPorDisciplina,
          ano
        );

        simulado.push({
          disciplina: disciplina.label,
          questoes: questoes
        });
      }

      // Incluir questões de idiomas se solicitado
      if (incluirIdiomas) {
        const idiomas = await this.buscarIdiomas();
        for (const idioma of idiomas) {
          if (idioma.value !== 'pt') { // Pular português
            const questoes = await this.buscarQuestoesIdioma(
              idioma.value, 
              5, // Menos questões de idiomas
              ano
            );
            
            if (questoes.length > 0) {
              simulado.push({
                disciplina: `${idioma.label} (Idioma)`,
                questoes: questoes
              });
            }
          }
        }
      }

      return simulado;
    } catch (error) {
      console.error('Erro ao gerar simulado:', error);
      return [];
    }
  }

  async buscarDisciplinas() {
    const response = await fetch(`${this.baseURL}/enem/disciplines`);
    return await response.json();
  }

  async buscarIdiomas() {
    const response = await fetch(`${this.baseURL}/enem/languages`);
    return await response.json();
  }

  async buscarQuestoesDisciplina(disciplina, limite, ano) {
    const params = new URLSearchParams({
      discipline: disciplina,
      limit: limite.toString()
    });
    
    if (ano) params.append('year', ano);
    
    const response = await fetch(`${this.baseURL}/enem/questions?${params}`);
    const data = await response.json();
    return data.data;
  }

  async buscarQuestoesIdioma(idioma, limite, ano) {
    const params = new URLSearchParams({
      language: idioma,
      limit: limite.toString()
    });
    
    if (ano) params.append('year', ano);
    
    const response = await fetch(`${this.baseURL}/enem/questions?${params}`);
    const data = await response.json();
    return data.data;
  }

  // Exportar simulado como JSON
  exportarSimulado(simulado, nomeArquivo = 'simulado_enem.json') {
    const blob = new Blob([JSON.stringify(simulado, null, 2)], {
      type: 'application/json'
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = nomeArquivo;
    a.click();
    
    URL.revokeObjectURL(url);
  }

  // Imprimir relatório do simulado
  imprimirRelatorio(simulado) {
    console.log('\n📋 RELATÓRIO DO SIMULADO GERADO');
    console.log('=' * 50);
    
    let totalQuestoes = 0;
    
    simulado.forEach(secao => {
      console.log(`\n📚 ${secao.disciplina}: ${secao.questoes.length} questões`);
      totalQuestoes += secao.questoes.length;
      
      // Mostrar anos das questões
      const anos = secao.questoes.map(q => q.year);
      const anosUnicos = [...new Set(anos)].sort();
      console.log(`   Anos: ${anosUnicos.join(', ')}`);
    });
    
    console.log(`\n🎯 Total de questões: ${totalQuestoes}`);
    console.log(`⏱️  Tempo estimado: ${Math.ceil(totalQuestoes * 3)} minutos`);
  }
}

// Usar o gerador
const gerador = new GeradorSimulados();

// Gerar simulado completo
gerador.gerarSimulado({
  questoesPorDisciplina: 15,
  ano: 2023,
  incluirIdiomas: true
}).then(simulado => {
  gerador.imprimirRelatorio(simulado);
  // gerador.exportarSimulado(simulado, 'simulado_enem_2023.json');
});
```

### 5. Busca Avançada com Filtros

```bash
#!/bin/bash

# Script para buscar questões usando curl

BASE_URL="http://localhost:3000"

echo "🔍 BUSCA AVANÇADA - QUESTÕES ENEM"
echo "================================="

# 1. Questões de matemática dos últimos 3 anos
echo -e "\n📊 Questões de Matemática (2021-2023):"
for year in 2021 2022 2023; do
    echo "  📅 Ano $year:"
    curl -s "$BASE_URL/enem/questions?discipline=matematica-tecnologias&year=$year&limit=3" | \
    jq -r '.data[] | "    - \(.title) (Questão \(.index))"'
done

# 2. Questões de idiomas
echo -e "\n🌐 Questões de Idiomas:"
for lang in en es; do
    lang_name=$([ "$lang" = "en" ] && echo "Inglês" || echo "Espanhol")
    echo "  🗣️ $lang_name:"
    curl -s "$BASE_URL/enem/questions?language=$lang&limit=2" | \
    jq -r '.data[] | "    - \(.title) (\(.year))"'
done

# 3. Questões mais recentes
echo -e "\n🆕 Questões Mais Recentes (2023):"
curl -s "$BASE_URL/enem/questions?year=2023&limit=5" | \
jq -r '.data[] | "  - \(.title) | \(.discipline.label)"'

# 4. Estatísticas gerais
echo -e "\n📈 Estatísticas Gerais:"
echo "  Anos disponíveis:"
curl -s "$BASE_URL/enem/years" | jq -r '.[] | "    - \(.)"'

echo -e "\n  Disciplinas disponíveis:"
curl -s "$BASE_URL/enem/disciplines" | jq -r '.[] | "    - \(.label)"'

echo -e "\n  Idiomas disponíveis:"
curl -s "$BASE_URL/enem/languages" | jq -r '.[] | "    - \(.label)"'

echo -e "\n✅ Busca concluída!"
```

## 💡 Dicas de Uso

### 1. **Otimização de Requisições**
- Use paginação para grandes volumes de dados
- Combine filtros para buscar questões específicas
- Cache os resultados das disciplinas e idiomas

### 2. **Tratamento de Erros**
```javascript
async function buscarQuestaoSegura(id) {
  try {
    const response = await fetch(`http://localhost:3000/enem/questions/${id}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        console.log(`Questão ${id} não encontrada`);
        return null;
      }
      throw new Error(`Erro HTTP: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Erro ao buscar questão:', error);
    return null;
  }
}
```

### 3. **Construção de URLs Dinâmicas**
```javascript
function construirURL(filtros) {
  const params = new URLSearchParams();
  
  Object.entries(filtros).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      params.append(key, value);
    }
  });
  
  return `http://localhost:3000/enem/questions?${params.toString()}`;
}

// Uso
const url = construirURL({
  year: 2023,
  discipline: 'matematica-tecnologias',
  limit: 20
});
```

### 4. **Processamento em Lote**
```javascript
async function processarQuestoes(filtros, processarFuncao) {
  let page = 1;
  let totalProcessadas = 0;
  
  while (true) {
    const response = await fetch(
      construirURL({...filtros, page, limit: 50})
    );
    
    const data = await response.json();
    
    if (data.data.length === 0) break;
    
    for (const questao of data.data) {
      await processarFuncao(questao);
      totalProcessadas++;
    }
    
    console.log(`Processadas ${totalProcessadas} questões...`);
    
    if (page >= data.totalPages) break;
    page++;
  }
  
  console.log(`✅ Total processadas: ${totalProcessadas} questões`);
}
```

Estes exemplos mostram como integrar a API em diferentes tipos de aplicações, desde sistemas de estudo até ferramentas de análise de dados educacionais.
