<template>
  <v-row class="ingredients">
    <v-col style="padding:0px" cols="3" v-bind:key="item" v-for="item in ingredients">
      <v-checkbox
        v-model="checkedIngredients"
        hide-details
        dense
        v-on:change="$emit('select', checkedIngredients)"
        :value="item"
        :label="item"
      ></v-checkbox>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "Ingredients",
  data: function() {
    return { checkedIngredients: [], itemsPerRow: 9, ingredients: [] };
  },
  async mounted() {
    this.ingredients = await window.axios.get(`/alcohols`);
  }
};
</script>

<style scoped>
.ingredients {
  text-align: left;
  margin-bottom: 40px;
  margin-top: 40px;
}
</style>
