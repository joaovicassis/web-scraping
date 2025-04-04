<template>
  <div class="search-form">
    <!-- Formulário de busca -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <input 
              v-model="searchQuery" 
              @input="debounceSearch"
              type="text" 
              class="form-control" 
              placeholder="Digite sua busca..."
            >
          </div>
          <div class="col-md-3">
            <select v-model="selectedUF" class="form-select">
              <option value="">Todos os estados</option>
              <option v-for="uf in ufs" :key="uf" :value="uf">{{ uf }}</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="selectedModalidade" class="form-select">
              <option value="">Todas as modalidades</option>
              <option v-for="mod in modalidades" :key="mod" :value="mod">{{ mod }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <button @click="search" class="btn btn-primary w-100">Buscar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Carregando...</span>
      </div>
    </div>

    <!-- Erro -->
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <!-- Sem resultados -->
    <div v-else-if="results.length === 0" class="alert alert-info">
      Nenhum resultado encontrado.
    </div>

    <!-- Tabela de resultados -->
    <div v-else class="table-responsive">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Registro ANS</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
            <th>Modalidade</th>
            <th>Cidade/UF</th>
            <th>Bairro</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="result in results" :key="result.registro_ans">
            <td>{{ result.registro_ans }}</td>
            <td>{{ result.razao_social }}</td>
            <td>{{ result.nome_fantasia }}</td>
            <td>{{ result.modalidade }}</td>
            <td>{{ result.cidade }}/{{ result.uf }}</td>
            <td>{{ result.bairro }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginação -->
    <div v-if="results.length > 0" class="d-flex justify-content-between align-items-center mt-4">
      <div>
        Mostrando {{ results.length }} resultados
      </div>
      <div>
        <button 
          @click="previousPage" 
          :disabled="currentPage === 1"
          class="btn btn-outline-primary me-2"
        >
          Anterior
        </button>
        <button 
          @click="nextPage" 
          :disabled="results.length < limit"
          class="btn btn-outline-primary"
        >
          Próxima
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// Estado
const searchQuery = ref('')
const selectedUF = ref('')
const selectedModalidade = ref('')
const results = ref([])
const loading = ref(false)
const error = ref(null)
const currentPage = ref(1)
const limit = ref(10)
const ufs = ref([])
const modalidades = ref([])
const searchTimeout = ref(null)

// Métodos
const search = async () => {
  loading.value = true
  error.value = null
  
  try {
    const params = new URLSearchParams({
      query: searchQuery.value,
      limit: limit.value,
      offset: (currentPage.value - 1) * limit.value
    })
    
    if (selectedUF.value) {
      params.append('uf', selectedUF.value)
    }
    
    if (selectedModalidade.value) {
      params.append('modalidade', selectedModalidade.value)
    }
    
    const response = await axios.get(`/api/search?${params}`)
    results.value = response.data
  } catch (err) {
    error.value = 'Erro ao realizar a busca. Por favor, tente novamente.'
    console.error('Erro:', err)
  } finally {
    loading.value = false
  }
}

const debounceSearch = () => {
  clearTimeout(searchTimeout.value)
  searchTimeout.value = setTimeout(() => {
    currentPage.value = 1
    search()
  }, 500)
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    search()
  }
}

const nextPage = () => {
  currentPage.value++
  search()
}

const loadFilters = async () => {
  try {
    // Carrega UFs únicas
    const ufResponse = await axios.get('/api/search?query=&limit=1')
    if (ufResponse.data.length > 0) {
      ufs.value = [...new Set(ufResponse.data.map(item => item.uf))].sort()
    }
    
    // Carrega modalidades únicas
    const modResponse = await axios.get('/api/search?query=&limit=1')
    if (modResponse.data.length > 0) {
      modalidades.value = [...new Set(modResponse.data.map(item => item.modalidade))].sort()
    }
  } catch (err) {
    console.error('Erro ao carregar filtros:', err)
  }
}

// Lifecycle hooks
onMounted(() => {
  loadFilters()
})
</script>

<style scoped>
.search-form {
  max-width: 1200px;
  margin: 0 auto;
}
</style> 