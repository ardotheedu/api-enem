#!/usr/bin/env node

/**
 * Script de teste para verificar todas as rotas da API ENEM
 * Execute: node test_api.js
 */

const https = require('http');

const BASE_URL = 'http://localhost:3000';

// Função para fazer requisições HTTP
function fazerRequisicao(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const jsonData = JSON.parse(data);
          resolve({ status: res.statusCode, data: jsonData });
        } catch (error) {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });
    
    req.on('error', (error) => {
      reject(error);
    });
    
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
  });
}

// Função para testar uma rota
async function testarRota(nome, url, esperado = 200) {
  try {
    console.log(`🔍 Testando: ${nome}`);
    console.log(`   URL: ${url}`);
    
    const resultado = await fazerRequisicao(url);
    
    if (resultado.status === esperado) {
      console.log(`   ✅ Sucesso (${resultado.status})`);
      
      if (typeof resultado.data === 'object') {
        if (Array.isArray(resultado.data)) {
          console.log(`   📊 Retornou ${resultado.data.length} itens`);
        } else if (resultado.data.data && Array.isArray(resultado.data.data)) {
          console.log(`   📊 Retornou ${resultado.data.data.length} questões (total: ${resultado.data.total})`);
        } else if (resultado.data.id) {
          console.log(`   📝 Questão ID: ${resultado.data.id} - ${resultado.data.title}`);
        }
      }
    } else {
      console.log(`   ❌ Falha (${resultado.status})`);
    }
    
    console.log('');
    return resultado.status === esperado;
  } catch (error) {
    console.log(`   ❌ Erro: ${error.message}`);
    console.log('');
    return false;
  }
}

// Função principal de teste
async function executarTestes() {
  console.log('🚀 INICIANDO TESTES DA API ENEM');
  console.log('=' * 50);
  console.log('');
  
  let totalTestes = 0;
  let testesPassaram = 0;
  
  // Lista de testes
  const testes = [
    // Testes básicos
    ['Listar questões (primeira página)', `${BASE_URL}/enem/questions`],
    ['Listar questões com limite', `${BASE_URL}/enem/questions?limit=5`],
    ['Questões de 2023', `${BASE_URL}/enem/questions?year=2023`],
    ['Questões de matemática', `${BASE_URL}/enem/questions?discipline=matematica-tecnologias`],
    ['Questões de inglês', `${BASE_URL}/enem/questions?language=en`],
    ['Questões paginadas', `${BASE_URL}/enem/questions?page=2&limit=3`],
    
    // Questão específica
    ['Questão por ID (1)', `${BASE_URL}/enem/questions/1`],
    ['Questão por ID (100)', `${BASE_URL}/enem/questions/100`],
    
    // Questão aleatória
    ['Questão aleatória', `${BASE_URL}/enem/questions/random`],
    ['Questão aleatória de 2023', `${BASE_URL}/enem/questions/random?year=2023`],
    ['Questão aleatória de matemática', `${BASE_URL}/enem/questions/random?discipline=matematica-tecnologias`],
    
    // Listas de metadados
    ['Listar anos disponíveis', `${BASE_URL}/enem/years`],
    ['Listar disciplinas disponíveis', `${BASE_URL}/enem/disciplines`],
    ['Listar idiomas disponíveis', `${BASE_URL}/enem/languages`],
    
    // Testes de filtros combinados
    ['Filtros combinados: ano + disciplina', `${BASE_URL}/enem/questions?year=2023&discipline=matematica-tecnologias`],
    ['Filtros combinados: disciplina + idioma', `${BASE_URL}/enem/questions?discipline=linguagens-codigos-tecnologias&language=en`],
  ];
  
  // Executar todos os testes
  for (const [nome, url] of testes) {
    totalTestes++;
    const sucesso = await testarRota(nome, url);
    if (sucesso) testesPassaram++;
    
    // Pequena pausa entre testes
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Testes de erro (devem retornar 404)
  console.log('🔍 TESTANDO CASOS DE ERRO');
  console.log('-' * 30);
  console.log('');
  
  const testesErro = [
    ['Questão inexistente', `${BASE_URL}/enem/questions/99999`, 404],
    ['Parâmetros inválidos', `${BASE_URL}/enem/questions?year=abc`, 400],
  ];
  
  for (const [nome, url, statusEsperado] of testesErro) {
    totalTestes++;
    const sucesso = await testarRota(nome, url, statusEsperado);
    if (sucesso) testesPassaram++;
    
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Relatório final
  console.log('📊 RELATÓRIO FINAL');
  console.log('=' * 50);
  console.log(`Total de testes: ${totalTestes}`);
  console.log(`Testes aprovados: ${testesPassaram}`);
  console.log(`Testes falharam: ${totalTestes - testesPassaram}`);
  console.log(`Taxa de sucesso: ${((testesPassaram / totalTestes) * 100).toFixed(1)}%`);
  
  if (testesPassaram === totalTestes) {
    console.log('');
    console.log('🎉 TODOS OS TESTES PASSARAM!');
    console.log('✅ API está funcionando corretamente');
  } else {
    console.log('');
    console.log('⚠️  ALGUNS TESTES FALHARAM');
    console.log('❌ Verifique se a API está executando em http://localhost:3000');
  }
}

// Verificar se a API está rodando
async function verificarAPI() {
  try {
    console.log('🔍 Verificando se a API está rodando...');
    await fazerRequisicao(`${BASE_URL}/enem/years`);
    console.log('✅ API está respondendo!');
    console.log('');
    return true;
  } catch (error) {
    console.log('❌ API não está respondendo');
    console.log('💡 Certifique-se de que a API está rodando em http://localhost:3000');
    console.log('💡 Execute: npm run start:dev');
    console.log('');
    return false;
  }
}

// Executar script
(async () => {
  const apiRodando = await verificarAPI();
  
  if (apiRodando) {
    await executarTestes();
  } else {
    console.log('❌ Não foi possível executar os testes');
  }
})();
