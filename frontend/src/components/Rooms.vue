<template>
    <v-card class="card-margin-bottom">
        <v-toolbar color="orange lighten-1" dark>
            <v-toolbar-title>Team</v-toolbar-title>
        </v-toolbar>
        <v-list two-line>
            <template v-for="(room, index) in rooms">
                <v-list-tile :key="index" avatar ripple @click="showRoom(room.name)">
                    <v-list-tile-avatar>
                        <img :src="room.avatar">
                    </v-list-tile-avatar>
                    <v-list-tile-content>
                        <v-list-tile-title>{{room.name}}</v-list-tile-title>
                        <v-list-tile-sub-title>{{room.name}}</v-list-tile-sub-title>
                    </v-list-tile-content>
                </v-list-tile>
            </template>
        </v-list>
    </v-card>
</template>

<script>
import { EventBus } from '../../Event'
import axios from 'axios'

export default {
  name: "Rooms",
  data() {
    return {
        rooms: [
            {
                id: 1, name: 'The Winners', avatar: 'https://picsum.photos/250/300?image=783',
            },
            {
                id: 2, name: 'Remote Control', avatar: 'https://picsum.photos/250/300?image=783',
            },
            {
                id: 3, name: 'Team Fabulous', avatar: 'https://picsum.photos/250/300?image=783',
            },
            {
                id: 4, name: 'Slow Down', avatar: 'https://picsum.photos/250/300?image=783',
            }
        ],
        roomCount: 4,
        loading: false,
    }
  },
  created() {
    EventBus.$on('new_room', (data) => {
        this.roomCount++;
        this.rooms.push({id: this.roomCount, name: data});
    });
  },
  methods: {
    showRoom(room) {
        console.log(room)
        EventBus.$emit('show_room', room);
    }
  }

}
</script>

<style scoped>
  .card-margin-bottom {
      margin-bottom: 10px;
  }
</style>

