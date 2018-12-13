<template>
    <div class="col-md-3 rooms">
        <div class="room" v-for="room in rooms" v-bind:key="room.id" @click="showRoom(room.name)">
            {{room.name}}
        </div>
        <AddRoom />
    </div>
</template>

<script>
import { EventBus } from '../Event'
import axios from 'axios'
import AddRoom from '../components/AddRoom'

export default {
  name: "Rooms",
  data() {
    return {
        rooms: [
            {id: 1, name: 'PHP Room'},
            {id: 2, name: 'Python Room'},
            {id: 3, name: 'Daily standup'}
        ],
        roomCount: 3,
        loading: false,
    }
  },
  components: {
   AddRoom  
  },
  created() {
    EventBus.$on('new_room', (data) => {
        this.roomCount++;
        this.rooms.push({id: this.roomCount, name: data});
    });
  },
  methods: {
    showRoom(room) {
        EventBus.$emit('show_room', room);
    }
  }

}
</script>

<style scoped>
    .rooms > .room {
        border: 1px solid rgb(124, 129, 124);
        padding: 13px;
        margin: 3px 0px;
        color: ghostwhite;
    }

    .rooms {
      border: 1px solid rgb(64, 68, 64);
      cursor: pointer;
    }
</style>

