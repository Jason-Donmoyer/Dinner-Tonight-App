<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { ingredientsApi, type Ingredient } from '@/api/client'
import { useInventoryStore } from '@/stores/inventory'
import { useRecipeStore } from '@/stores/recipes'

const inventoryStore = useInventoryStore()
const recipeStore = useRecipeStore()

const searchQuery = ref('')
const searchResults = ref<Ingredient[]>([])
const searching = ref(false)
const selectedIngredient = ref<Ingredient | null>(null)
const errorMessage = ref('')

// Filter out ingredients already in the inventory
const filteredResults = computed(() => {
    const inventoryIds = inventoryStore.items.map(item => item.ingredient_id)
    return searchResults.value.filter(ing => !inventoryIds.includes(ing.id))
})

// Debounce search
let searchTimeout: number
watch(searchQuery, (newQuery) => {
    if (searchTimeout) clearTimeout(searchTimeout)

    if (newQuery.length < 2) {
        searchResults.value = []
        return
    }

    searchTimeout = setTimeout(async () => {
        searching.value = true
        try {
            const response = await ingredientsApi.search(newQuery)
            searchResults.value = response.data
        } catch (e) {
            console.error('Search failed:', e)
        } finally {
            searching.value = false
        }
    }, 300) as unknown as number
})

async function selectIngredient(ingredient: Ingredient) {
    selectedIngredient.value = ingredient
    const success = await inventoryStore.addIngredient(ingredient.id)

    if (success) {
        searchQuery.value = ''
        searchResults.value = []
        selectedIngredient.value = null
        // Refresh recipe suggestions after adding ingredient
        recipeStore.fetchSuggestions()
    }
}
</script>

<template>
    <div class="add-ingredient">
        <h3>Add Ingredients</h3>

        <div class="search-box">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Search for ingredients..."
                class="search-input"
            />

            <div v-if="searching" class="search-results">
                <div class="result-item">Searching...</div>
            </div>

            <div v-else-if="filteredResults.length > 0" class="search-results">
                <button
                    v-for="ingredient in filteredResults"
                    :key="ingredient.id"
                    @click="selectIngredient(ingredient)"
                    class="result-item"
                >
                    <span class="result-name">{{ ingredient.name }}</span>
                    <span v-if="ingredient.category" class="result-category">
                        {{ ingredient.category }}
                    </span>
                </button>
            </div>

            <div v-else-if="searchQuery.length >= 2 && searchResults.length > 0" class="search-results">
                <div class="result-item">No ingredients found</div>
            </div>
        </div>

        <p v-if="inventoryStore.error" class="error-message">
            {{ errorMessage }}
        </p>
    </div>
</template>

<style scoped>
.add-ingredient {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h3 {
    margin: 0 0 1rem 0;
    font-size: 1.25rem;
    color: #2c3e50;
}

.search-box {
    position: relative;
}

.search-input {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.2s;
}

.search-input:focus {
    outline: none;
    border-color: #3498db;
}

.search-results {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 4px 4px;
    max-height: 300px;
    overflow-y: auto;
    box-shadow: 0 4px 12px rgbs(0, 0,l 0, 0.1);
    z-index: 10;
}

.result-item {
    width: 100%;
    padding: 0.75rem;
    border: none;
    background: none;
    text-align: left;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f0f0f0;
    transition: background 0.2s;
}

.result-item:last-child {
    border-bottom: none;
}

.result-item:hover {
    background: #f8f9fa;
}

.result-name {
    font-weight: 500;
    text-transform: capitalize;
    color: #2c3e50;
}

.result-category {
    font-size: 0.875rem;
    color: #666;
    text-transform: capitalize;
    padding: 0.25rem 0.5rem;
    background: #ecf0f1;
    border-radius: 12px;
}

.error-message {
    margin-top: 0.75rem;
    padding: 0.75rem;
    background: #fee;
    border: 1px solid #e74c3c;
    border-radius: 4px;
    color: #c0392b;
    font-size: 0.875rem;
}

</style>