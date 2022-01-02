<template>
  <v-col cols="6" class="recipe">
    <v-row>
      <v-col>
        <h2>{{ recipe.name }}</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" class="d-flex flex-column">
        <p>{{ recipe.preparation }}</p>
        <v-img max-height="100" max-width="500" contain :src="image(recipe)" />
        <br />
        <v-spacer></v-spacer>
        <v-btn color="primary" elevation="7" large @click="prepare(recipe)"
          >Prepare cocktail</v-btn
        >
      </v-col>
      <v-col>
        <v-card class="mx-auto" width="300" min-height="400">
          <v-list subheader>
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-glass-cocktail</v-icon>
              </v-list-item-icon>

              <v-list-item-title>{{ recipe.glass }}</v-list-item-title>
            </v-list-item>

            <v-list-item v-if="recipe.garnish">
              <v-list-item-icon>
                <v-icon>mdi-fruit-citrus</v-icon>
              </v-list-item-icon>

              <v-list-item-title>{{ recipe.garnish }}</v-list-item-title>
            </v-list-item>

            <v-subheader inset>Ingredients</v-subheader>
            <v-list-item
              v-bind:key="ingredient.ingredient"
              v-for="ingredient of recipe.ingredients"
            >
              <v-badge
                v-if="ingredient.ingredient"
                color="green"
                :content="amount(ingredient)"
              >
                {{ ingredient.ingredient }}
              </v-badge>
              <span v-else color="red" :content="amount(ingredient)">
                {{ ingredient.special }}
              </span>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
export default {
  name: "Ingredient",
  props: {
    recipe: Object
  },
  methods: {
    image(recipe) {
      return `/images/${recipe.name}.png`;
    },
    amount(ingredient) {
      return `${ingredient.amount}${ingredient.unit}`;
    },
    async prepare(recipe) {
      await window.axios.post(`/recipes/`, recipe);
    }
  }
};
</script>

<style scoped>
.recipe {
  text-align: left;
  margin-bottom: 50px;
}
</style>
