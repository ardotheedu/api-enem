// Exemplos de uso da API ENEM
// Execute este script com: node api-examples.js

const BASE_URL = 'http://localhost:3000/enem';

// Função helper para fazer requisições
async function makeRequest(endpoint, description) {
  try {
    console.log(`\n🔍 ${description}`);
    console.log(`URL: ${BASE_URL}${endpoint}`);
    
    const response = await fetch(`${BASE_URL}${endpoint}`);
    const data = await response.json();
    
    console.log(`Status: ${response.status}`);
    console.log('Resposta:', JSON.stringify(data, null, 2));
    
    return data;
  } catch (error) {
    console.error(`Erro: ${error.message}`);
  }
}

async function runExamples() {
  console.log('🚀 EXEMPLOS DE USO DA API ENEM');
  console.log('===============================');

  // 1. Listar anos disponíveis
  await makeRequest('/years', 'Listar anos disponíveis');

  // 2. Listar disciplinas disponíveis
  await makeRequest('/disciplines', 'Listar disciplinas disponíveis');

  // 3. Listar idiomas disponíveis
  await makeRequest('/languages', 'Listar idiomas disponíveis');

  // 4. Buscar questões de 2023 (primeira página)
  await makeRequest('/questions?year=2023&limit=3', 'Buscar 3 questões de 2023');

  // 5. Buscar questões de matemática
  await makeRequest('/questions?discipline=matematica&limit=2', 'Buscar 2 questões de matemática');

  // 6. Buscar questões de inglês
  await makeRequest('/questions?language=en&limit=2', 'Buscar 2 questões de inglês');

  // 7. Buscar questões com paginação
  await makeRequest('/questions?page=2&limit=5', 'Buscar página 2 com 5 questões');

  // 8. Buscar questão específica por ID
  await makeRequest('/questions/2575', 'Buscar questão específica (ID: 2575)');

  // 9. Questão aleatória
  await makeRequest('/questions/random', 'Buscar questão aleatória');

  // 10. Questão aleatória de matemática de 2023
  await makeRequest('/questions/random?year=2023&discipline=matematica', 'Questão aleatória de matemática de 2023');

  // 11. Filtro complexo: questões de ciências humanas de 2022
  await makeRequest('/questions?year=2022&discipline=ciencias-humanas&limit=2', 'Questões de ciências humanas de 2022');

  console.log('\n✅ Todos os exemplos foram executados!');
}

// Executar exemplos
runExamples().catch(console.error);
