<script setup>
import { ref } from "vue";
import axios from "axios";

const searchQuery = ref("");
const operadoras = ref([]);

const searchOperadoras = async () => {
  if (searchQuery.value.trim() === "") return;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/search`, {
      params: { query: searchQuery.value },
    });
    operadoras.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar operadoras:", error);
  }
};
</script>

<template>
  <div class="container">
    <h1>Buscar Operadoras</h1>
    <input v-model="searchQuery" @keyup.enter="searchOperadoras" placeholder="Nome da operadora..." />
    <button @click="searchOperadoras">Buscar</button>

    <ul v-if="operadoras.length">
      <li v-for="operadora in operadoras" :key="operadora.Razao_Social">
        <strong>{{ operadora.Razao_Social }}</strong> - {{ operadora.Nome_Fantasia }}
      </li>
    </ul>
    <p v-else>Nenhuma operadora encontrada.</p>
  </div>
</template>

<style>
.container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
input {
  padding: 8px;
  margin: 10px;
}
button {
  padding: 8px 15px;
  cursor: pointer;
}
</style>

<!-- Depois de instalada as bibliotecas (npm install), rodar npm run dev -->