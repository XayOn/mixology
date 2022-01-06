<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn text @click="showSettings=false; recipes=[]">Mixologist</v-btn>
      <v-spacer></v-spacer>
      <v-btn icon @click="showSettings=!showSettings; recipes=[]">
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main class="pt-2 pt-sm-2 pt-xs-2 pt-md-0 pt-lg-0 pt-xl-0">
      <v-container  v-if="showSettings">
        <Settings v-on:saved="showSettings=false" />
      </v-container>
      <div v-if="!showSettings">
      <v-container>
        <Ingredients @select='updateRecipes'/>
      </v-container>
      <v-container fluid style="margin-left:5px" v-if="recipes.length != 0">
        <v-row class="recipes">
          <Recipe v-for="recipe in recipes" v-bind:key="recipe.name" :recipe=recipe />
        </v-row>
      </v-container>
      <v-container>
        <v-alert v-if="recipes.length == 0" border="left" 
                 elevation="2" icon="mdi-glass-cocktail" prominent text type="info">
          Select some ingredients to get the list of available cocktails
        </v-alert>
      </v-container>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import Recipe from './components/Recipe.vue'
import Ingredients from './components/Ingredients.vue'
import Settings from './components/Settings.vue'

export default {
  name: 'App',
  data: function(){
    return {recipes: [], showSettings: false}
  },
  methods: {
    async updateRecipes(ingredients) {
        let vals = ""; for (const v of ingredients) { vals += `current=${v}&`}
        this.recipes = await window.axios.get(`recipes/?${vals}`)
    }
  },
  components: {
    Recipe,
    Ingredients,
    Settings
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
