<template>
    <v-card dark tile flat color="" class="card-height">
        <v-toolbar-title>Ragamuffings Chat</v-toolbar-title>
        
        <v-progress-circular
            :size="70"
            :width="7"
            indeterminate
            v-if="chat_loading"
            class="chat-loading"
        ></v-progress-circular>
        <div v-else>
            <v-card-text id="messages">
                <div 
                    class="chat-message" 
                    v-for="(message, index) in messages" 
                    :key="index"
                    :class=" (message.author == email) ? 'right': '' "
                >
                    <v-list-tile-avatar class="circle">
                        <img src="https://picsum.photos/250/300?image=783">
                    </v-list-tile-avatar>
                    {{message.body}}
                </div>
            </v-card-text>
            <v-container fluid grid-list-md text-xs-center class="input-form">
                <v-layout row wrap>
                    <v-flex xs12 md12>
                    <v-textarea
                        v-model="message"
                        box
                        label="message"
                        rows="1"
                        width="50px"
                    ></v-textarea>
                    </v-flex>
                    <button type="submit" style="margin-left: -30px; z-index: 3;">
                        <i class="material-icons" @click="sendMessage(message)">send</i>
                    </button>
                </v-layout>
            </v-container>
        </div>
    </v-card>
</template>

<script>
export default {
    name: "ChatRoom",
    props: {
        email: String,
        messages: Array,
        chat_loading: Boolean,
    },
    data() {
        return {
            message: "",
        }
    },
    methods: {
      sendMessage(message) {
        this.message = ""
        this.$emit('new-message', message)
      }
    },
    created() {}
}
</script>

<style>
  #messages {
      
  }
    .chat-message {
    position: relative;
    float: left;
    clear: both;
    margin: 2px 50px 20px;
    padding: 8px;
    border-radius: 8px;
    line-height: 22px;
    background-color: #ddd;
    color: black;
  }
  .circle {
    position: absolute;
    top: -2px;
    left: -50px;
    height: 42px;
    width: 42px;
  }
  .right {
    background-color: #448AFF;
    color: #fff;
    float: right !important;
  }
  .chat-message .circle {
    position: absolute;
    top: -2px;
    left: -50px;
    height: 42px;
    width: 42px;
  }
  .chat-message.right {
      background-color: #448AFF;
      color: #fff;
  }
  .chat-message.right .circle {
      left: auto;
      right: -65px;
  }
  .input-form {
    clear: both;
  }
  .chat-loading {
    margin-top: auto; 
    margin-top: 13%;
  }
</style>
