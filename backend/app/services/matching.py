from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

class RecipeMatchingService:
    """
    Service for matching recipes to user's ingredient inventory.
    """

    def __init__(self, db: Session):
        self.db = db

    def find_matching_recipes(
        self,
        user_id: int = 1,
        max_missing: int = 2,
        limit: int = 10
    ) -> List[dict]:
        """
        Find recipes ranked by ingredient match percentage.

        Args:
            user_id: User ID to check inventory for
            max_missing: Maximum number of missing ingredients allowed
            limit: Maximum number of recipes to return

        Returns:
            List of recipe matches with metadata
        """

        query = text("""
            WITH recipe_match AS (
                SELECT
                    r.id,
                    r.name,
                    r.description,
                    r.cooking_time,
                    COUNT(ri.ingredient_id) as total_ingredients,
                    COUNT(ui.ingredient_id) as matched_ingredients,
                    ARRAY_AGG(i.name) FILTER (WHERE ui.ingredient_id IS NULL) as missing
                FROM recipes r
                JOIN recipe_ingredients ri ON r.id = ri.recipe_id
                JOIN ingredients i ON ri.ingredient_id = i.id
                LEFT JOIN user_inventory ui ON ri.ingredient_id = ui.ingredient_id
                    AND ui.user_id = :user_id
                GROUP BY r.id, r.name, r.description, r.cooking_time
            )
            SELECT
                id,
                name,
                description,
                cooking_time,
                total_ingredients,
                matched_ingredients,
                total_ingredients - matched_ingredients as missing_count,
                ROUND(matched_ingredients::numeric / total_ingredients * 100) as match_percent,
                COALESCE(missing, ARRAY[]::text[]) as missing_ingredients
            FROM recipe_match
            WHERE total_ingredients - matched_ingredients <= :max_missing
            ORDER BY match_percent DESC, missing_count ASC
            LIMIT :limit
            """)
        
        result = self.db.execute(query, {
            "user_id": user_id,
            "max_missing": max_missing,
            "limit": limit
        })

        return [dict(row._mapping) for row in result]
            
