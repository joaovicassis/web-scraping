<template>
  <div class="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand" to="/">Busca de Operadoras</router-link>
      </div>
    </nav>

    <main class="container mt-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<style>
.app {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.navbar {
  margin-bottom: 2rem;
}
</style> 