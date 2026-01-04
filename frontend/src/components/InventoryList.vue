<script setup lang="ts">
import { onMounted } from 'vue'
import { useInventoryStore } from '@/stores/inventory'

const inventoryStore = useInventoryStore()

onMounted(() => {
    inventoryStore.fetchInventory()
})

async function handleRemove(ingredientId: number) {
    if (confirm('Remove this ingredient from your inventory?')) {
        await inventoryStore.removeIngredient(ingredientId)
    }
}
</script>

<template>
    <div class="inventory-list">
        <h2>My Ingredients</h2>

        <div v-if="inventoryStore.loading" class="loading">
            Loading inventory...
        </div>

        <div v-else-if="inventoryStore.error" class="error">
            {{ inventoryStore.error }}
        </div>

        <div v-else-if="inventoryStore.items.length === 0" class="empty">
            No ingredients in your inventory. Add some to get recipe suggestions!
        </div>

        <ul v-else class="ingredient-items">
            <li v-for="item in inventoryStore.items" :key="item.id" class="ingredient-item">
                <div class="ingredient-info">
                    <span class="ingredient-name">{{ item.ingredient }}</span>
                    <span v-if="item.quantity" class="ingredient-quantity">
                        {{ item.quantity }} {{ item.unit }}
                    </span>
                </div>
                <button @click="handleRemove(item.ingredient_id)" class="btn-remove">
                    Remove
                </button>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.inventory-list {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgb(0, 0, 0, 0.1);
}
  
h2 {
    margin: 0 0 1rem 0;
    font-size: 1.5rem;
    color: #2c3e50;
}

.loading, .error, .empty {
    padding: 2rem;
    text-align: center;
    color: #666
}

.ingredient-items {
    list-style: none;
    padding: 0;
    margin: 0;
}

.ingredient-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    border-bottom: 1px solid #eee;
}

.ingredient-item:last-child {
    border-bottom: none;
}

.ingredient-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.ingredient-name {
    font-size: 0.875rem;
    color: #666;
}

.btn-remove {
    padding: 0.5rem 1rem;
    background: #e74c3c;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.875rem;
    transition: background 0.2s;
}

.btn-remove:hover {
    background: #c0392b;
}

</style>