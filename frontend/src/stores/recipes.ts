import { defineStore } from 'pinia'
import { ref } from 'vue'
import { recipesApi, type RecipeMatch } from '@/api/client'

export const useRecipeStore = defineStore('recipes', () => {
    const suggestions = ref<RecipeMatch[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)
    const maxMissing = ref(2)

    async function fetchSuggestions() {
        loading.value = true
        error.value = null

        try {
            const response = await recipesApi.getSuggestions(maxMissing.value, 20)
            suggestions.value = response.data
        } catch (e: any) {
            error.value = e.message || 'Failed to fetch recipe suggestions'
            console.error('Error feyching suggestions:', e)
        } finally {
            loading.value = false
        }
    }

    return {
        suggestions,
        loading,
        error,
        maxMissing,
        fetchSuggestions
    }
})