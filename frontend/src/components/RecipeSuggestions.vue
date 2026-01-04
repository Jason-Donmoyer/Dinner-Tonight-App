<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRecipeStore } from '@/stores/recipes'

const recipeStore = useRecipeStore()

onMounted(() => {
    recipeStore.fetchSuggestions()
})

watch(() => recipeStore.maxMissing, () => {
    recipeStore.fetchSuggestions()
})

function getMatchColor(percent: number): string {
    if (percent >= 80) return '#27ae60'
    if (percent >= 50) return '#f39c12'
    return '#e74c3c'
}
</script>

<template>
    <div class="recipe-suggestions">
        <div class="header">
            <h2>Recipe Suggestions</h2>

            <div class="filters">
                <label>
                    Missing ingredients allowed:
                    <select v-model="recipeStore.maxMissing">
                        <option :value="0">Exact match only</option>
                        <option :value="1">Up to 1 missing</option>
                        <option :value="2">Up tp 2 missing</option>
                        <option :value="3">Up to 3 missing</option>
                    </select>
                </label>
            </div>
        </div>

        <div v-if="recipeStore.loading" class="loading">
            Finding recipes...
        </div>

        <div v-else-if="recipeStore.error" class="error">
            {{ recipeStore.error }}
        </div>

        <div v-else-if="recipeStore.suggestions.length === 0" class="empty">
            No recipes match your current ingredients. Try adding more to your inventory!
        </div>

        <div v-else class="recipe-list">
            <div v-for="recipe in recipeStore.suggestions" :key="recipe.id" class="recipe-card">
                <div class="recipe-header">
                    <h3>{{ recipe.name }}</h3>
                    <span 
                        class="match-badge"
                        :style="{ backgroundColor: getMatchColor(recipe.match_pecent) }"
                        >
                        {{ recipe.match_percent }}% match
                    </span>
                </div>

                <p v-if="recipe.description" class="description">
                    {{ recipe.description }}
                </p>

                <div class="recipe-meta">
                    <span v-if="recipe.cooking_time" class="meta-item">
                        ⏱️ {{ recipe.cooking_time }} min
                    </span>
                    <span class="meta-item">
                        🥘 {{ recipe.total_ingredients }} ingredients
                    </span>
                    <span class="meta-item">
                        ✅ {{ recipe.matched_ingredients }} in stock
                    </span>
                </div>

                <div v-if="recipe.missing_ingredients.length > 0" class="missing">
                    <strong>Missing:</strong>
                    <span class="missing-items">
                        {{ recipe.missing_ingredients.join(', ') }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.recipe-suggestions {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 1rem;
}

h2 {
    margin: 0;
    font-size: 1.5rem;
    color: #2c3e50;
}

.filters select {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.875rem;
}

.loading, .error, .empty {
    padding: 2rem;
    text-align: center;
    color: #666;
}

.error {
    color: #e74c3c;
}

.recipe-list {
    display: grid;
    gap: 1rem;
}

.recipe-card {
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 1.25rem;
    transition: box-shadow 0.2s;
}

.recipe-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.recipe-header {
    display: flex;
    justify-content: space-between;
    align-items: start;
    gap: 1rem;
    margin-bottom: 0.75rem
}

.recipe-header h3 {
    margin: 0;
    font-size: 1.25rem;
    color: #2c3e50;
    flex: 1;
}

.match-badge {
    padding: 0.375rem 0.75rem;
    border-radius: 20px;
    color: white;
    font-size: 0.875rem;
    font-weight: 600;
    white-space: nowrap;
}

.description {
    color: #666;
    margin: 0 0 1rem 0;
    line-height: 1.5;
}

.recipe-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 0.75rem;
}

.meta-item {
    font-size: 0.875rem;
    color: #666;
}

.missing {
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 4px;
    padding: 0.75rem;
    font-size: 0.875rem;
}

.missing strong {
    color: #856404;
}

.missing-items {
    margin-left: 0.5rem;
    color: #666;
    text-transform: capitalize;
}

</style>