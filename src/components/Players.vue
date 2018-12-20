<template>
    <v-card class="card-margin-bottom">
        <v-toolbar color="orange lighten-1" dark>
            <v-toolbar-title>Players</v-toolbar-title>
        </v-toolbar>
        <v-list two-line>
            <template v-for="(player, index) in players">
                <v-list-tile 
                    :key="index" 
                    avatar 
                    ripple 
                >
                    <v-list-tile-avatar>
                        <img src="https://picsum.photos/250/300?image=783'">
                    </v-list-tile-avatar>
                    <v-list-tile-content>
                        <v-list-tile-title>{{player.first_name}} {{player.last_name}}</v-list-tile-title>
                        <v-list-tile-sub-title>{{player.first_name}} {{player.last_name}}</v-list-tile-sub-title>
                    </v-list-tile-content>
                </v-list-tile>
            </template>
        </v-list>
    </v-card>
</template>

<script>
export default {
  name: "Players",
  props: {
    players: Array
  },
  data() {
    return {
        loading: false,
    }
  },
  methods: {}

}
</script>

<style scoped>
  .card-margin-bottom {
      margin-bottom: 10px;
  }
  .nav-active {
    background: rgb(201, 199, 199);  
  }
</style>

