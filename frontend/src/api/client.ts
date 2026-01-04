import axios from 'axios'
import type { NamedTupleMember } from 'typescript'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json'
    }
})

// Type definitions
export interface RecipeMatch {
    id: number
    name: string
    description: string | null
    cooking_time: number | null
    total_ingredients: number
    matched_ingredients: number
    missing_count: number
    match_pecent: number
    missing_ingredients: string[]
}

export interface InventoryItem {
    id: number
    ingredient: string
    ingredient_id: number
    quantity: number | null
    unit: number | null
}

export interface Ingredient {
    id: number
    name: string
    category: string | null
}

export interface Recipe {
    id: number
    name: string
    description: string | null
    instructions: string | null
    cooking_time: number | null
    servings: number | null
}

// API methods
export const recipesApi = {
    getSuggestions: (maxMissing = 2, limit = 10) => 
        api.get<RecipeMatch[]>(`/recipes/suggestions?max-missing=${maxMissing}&limit=${limit}`),

    getAll: (skip = 0, limit = 20) =>
        api.get<Recipe[]>(`/recipes/?skip=${skip}&limit=${limit}`),

    getById: (id: number) =>
        api.get<Recipe>(`/recipes/${id}`)
}

export const inventoryApi = {
    getAll: () => 
        api.get<InventoryItem[]>('/inventory'),

    add: (ingredientId: number, quantity?: number, unit?: string) => {
        const params = new URLSearchParams({ ingredient_id: ingredientId.toString() })
        if (quantity !== undefined) params.append('quantity', quantity.toString())
            if (unit) params.append('unit', unit)
            return api.post('/inventory', null, { params })
    },

    remove: (ingredientId: number) =>
        api.delete(`/inventory/${ingredientId}`),

    update: (ingredientId: number, quantity: number, unit: string) => {
        const params = new URLSearchParams({
            quantity: quantity.toString(),
            unit: unit
        })
        return api.put(`/inventory/${ingredientId}`, null, { params })
    }
}

export const ingredientsApi = {
    search: (query: string, limit = 10) =>
        api.get<Ingredient[]>(`/ingredients/search?q=${encodeURIComponent(query)}&limit=${limit}`),

    getAll: (skip = 0, limit = 100) =>
        api.get<Ingredient[]>(`/ingredients/?skip=${skip}&limit=${limit}`)
}