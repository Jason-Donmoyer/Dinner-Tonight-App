import { defineStore } from 'pinia'
import { ref } from 'vue'
import { inventoryApi, type InventoryItem } from '@/api/client'

export const useInventoryStore = defineStore('inventory', () => {
    const items = ref<InventoryItem[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchInventory() {
        loading.value = true
        error.value = null
        try {
            const response = await inventoryApi.getAll()
            items.value = response.data
        } catch (e: any) {
            error.value = e.message || 'Failed to fetch inventory'
            console.error('Error fetching inventory:', e)
        } finally {
            loading.value = false
        }
    }

    async function addIngredient(ingredientId: number, quantity?: number, unit?: string) {
        try {
            await inventoryApi.add(ingredientId, quantity, unit)
            await fetchInventory() // Refresh the list
            return true
        } catch (e: any) {
            error.value = e.response?.data?.detail || 'Failed to add ingrediet'
            console.error('Error adding ingredient:', e)
            return false
        }
    }

    async function removeIngredient(ingredientId: number) {
        try {
            await inventoryApi.remove(ingredientId)
            await fetchInventory() // Refresh the list
            return true 
        } catch (e: any) {
            error.value = e.response?.data?.detail || 'Failed to remove ingredient'
            console.error('Error removing ingredient:', e)
            return false
        }
    }

    return {
        items,
        loading,
        error,
        fetchInventory,
        addIngredient,
        removeIngredient
    }
})