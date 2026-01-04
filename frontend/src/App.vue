<script setup lang="ts">
import { onMounted } from 'vue'
import RecipeSuggestions from './components/RecipeSuggestions.vue'
import InventoryList from './components/InventoryList.vue'
import AddIngredient from './components/AddIngredient.vue'
import { useInventoryStore } from './stores/inventory'

const inventoryStore = useInventoryStore()

onMounted(() => {
  inventoryStore.fetchInventory()
})
</script>

<template>
  <div id="app">
    <header class="app-header">
      <h1>Dinner Tonight!</h1>
      <p>Find recipes based on what you have</p>
    </header>

    <main class="app-main">
      <div class="sidebar">
        <AddIngredient />
        <InventoryList />
      </div>

      <div class="content">
        <RecipeSuggestions />
      </div>
    </main>
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 2.5rem;
  color: #2c3e50;
}

.app-header p {
  margin: 0.5rem 0 0 0;
  color: #666;
  font-size: 1.125rem;
}

.app-main {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 2rem;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

</style>