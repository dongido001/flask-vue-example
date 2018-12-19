<template> 
  <v-app id="inspire">
    <v-toolbar
      color="blue-grey"
      dark
      fixed
      app
    >
      <v-toolbar-side-icon ></v-toolbar-side-icon>
      <v-toolbar-title>Toolbar</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-side-icon ></v-toolbar-side-icon>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout row>
            <v-flex xs12 sm6 md2>
                <Rooms v-on:show_room="createChat"/>
                <Rooms />
            </v-flex>

            <v-flex xs6>
                <v-card dark tile flat color="" class="card-height">
                    <v-toolbar-title>Team Video Feed</v-toolbar-title>
                    <v-card-text>
                        <v-progress-circular
                          :size="70"
                          :width="7"
                          indeterminate
                          v-if="video_room_loading"
                          class="video-loading"
                        ></v-progress-circular>
                        <div id="team-video" v-else></div>
                    </v-card-text>
                </v-card>

                <ChatRoom 
                  :messages="chat_messages" 
                  v-on:new-message="addMessage" 
                  :chat_loading="chat_loading"
                  :email="logged_user_email"
                />
            </v-flex>

            <v-flex xs6>
                <v-card dark tile flat color="red darken-4" class="card-height">
                    <v-toolbar-title>Master Video Feed</v-toolbar-title>
                    <v-card-text>
                        <div id="master-video"></div>
                    </v-card-text>
                </v-card>

                <v-card dark tile flat color="red darken-4" class="card-height">
                    <v-toolbar-title>Game Play</v-toolbar-title>
                    <v-card-text>
                       <v-progress-circular
                          :size="70"
                          :width="7"
                          indeterminate
                          v-if="video_room_loading"
                          class="video-loading"
                        ></v-progress-circular>
                        <span v-else> %444 </span>
                    </v-card-text>
                </v-card>
            </v-flex>

        </v-layout>
      </v-container>
    </v-content>
    <v-navigation-drawer
      right
      temporary
      fixed
    ></v-navigation-drawer>
    <Footer />
  </v-app>
</template>

<script>
const Chat = require('twilio-chat')
import Video from 'twilio-video'
import axios from 'axios'
import { mapState } from 'vuex'

import { EventBus } from '../../Event'
import Rooms from './Rooms'
import Footer from './Footer'
import ChatRoom from './ChatRoom'

export default {
  name: 'App',
  components: {
    Rooms,
    Footer,
    ChatRoom
  },
  data () {
    return {
      chat: null,
      video_room_loading: false,
      chat_loading: false,
      active_room: null,
      video_client: null,
      room_name: null,
      chat_client: null,
      chat_channel: null,
      chat_messages: [],
      twilio_access_token: null,
    }
  },
  created() {
    // this.createChat('master');

    // When we are about to transition away from this page, disconnect
    // from the room, if joined.
    window.addEventListener('beforeunload', this.leaveRoomIfJoined);
  },
  computed: {
    ...mapState({
        logged_user_email: state => state.logged_user_email,
        token: state => state.token,
        role: state => state.role
    })
  },
  methods: {
    async getAccessToken() {

      if (this.twilio_access_token) {
        return new Promise( (resolve, reject) => {
            resolve({
                data: {token: this.twilio_access_token}
            })
        });
      }

      return await axios
                    .post("/api/generate_video_token", {
                      identity: this.logged_user_email,
                    })
    },
    // Attach the Tracks to the DOM.
    attachTracks(tracks, container) {
        tracks.forEach(function(track) {
            container.appendChild(track.attach());
        });
    },
    // Attach the Participant's Tracks to the DOM.
    attachParticipantTracks(participant, container) {
        let tracks = Array.from(participant.tracks.values());
        this.attachTracks(tracks, container);
    },
    // Detach the Tracks from the DOM.
    detachTracks(tracks) {
        tracks.forEach( (track) => {
            track.detach().forEach((detachedElement) => {
               detachedElement.remove();
            });
        });
    },
    // Detach the Participant's Tracks from the DOM.
    detachParticipantTracks(participant) {
        let tracks = Array.from(participant.tracks.values());
        this.detachTracks(tracks);
    },
    // Leave Room.
    leaveRoomIfJoined() {
        if (this.active_room) {
            this.active_room.disconnect();
        }
    },
    createChat(room_name) {
        this.loading = true;

        this.facilitatorRoom()

        this.getAccessToken().then( (data) => {

            if (data.status != 200) {
               return 
            } 

            this.video_room_loading = true
            this.chat_loading = true
            this.room_name = null

            const token = data.data.token
            this.twilio_access_token = token

            let connectOptions = {
                name: room_name,
                // logLevel: 'debug',
                audio: true, 
                video: { width: 120, height: 120 }
            };

            this.leaveRoomIfJoined();
            
            // remove any remote track when joining a new room
            document.getElementById('team-video').innerHTML = ""; 

            Chat.Client.create( token )
                .then( (client) => {
                    client.getPublicChannelDescriptors()
                        .then( channels => { /*this.channels = channels.state.items } */ });
                    this.chat_client = client;
                    this.addChannel(room_name)
                    this.chat_loading = false;
                });

            Video.connect(token , connectOptions).then( room => {
                // set active toom
                this.active_room = room;
                this.room_name = room_name;
                this.video_room_loading = false

                // Attach the Tracks of the Room's Participants.
                room.participants.forEach( (participant) => {
                    console.log(participant)
                    let previewContainer = document.getElementById('team-video');
                    this.attachParticipantTracks(participant, previewContainer);
                });

                // When a Participant adds a Track, attach it to the DOM.
                room.on('trackSubscribed', (track, participant) => {
                    let previewContainer = document.getElementById('team-video');
                    this.attachTracks([track], previewContainer);
                });
                
                // When a Participant removes a Track, detach it from the DOM.
                room.on('trackUnsubscribed', (track, participant) => {
                    this.detachTracks([track]);
                });

                // When a Participant leaves the Room, detach its Tracks.
                room.on('participantDisconnected', (participant) => {
                    this.detachParticipantTracks(participant);
                });
                
                // Add the user track
                // if(!this.localTrack) {
                //     Video.createLocalVideoTrack().then(track => {
                //       console.group(track)
                //       let localMediaContainer = document.getElementById('facilatator-video');
                //       localMediaContainer.appendChild(track.attach());

                //       this.localTrack = true;
                //     });
                // }
            }, function(error) {
                console.error('Unable to connect to Room: ' +  error.message);
            });

          });
     },
     facilitatorRoom() {
         this.getAccessToken().then( data => {
            let connectOptions = {
                name: 'facilltator-room',
                // logLevel: 'debug',
                audio: true, 
                video: { width: 120, height: 120 }
            };

            if(!this.localTrack && (this.role == 'facilitator') ) {
                Video.createLocalVideoTrack().then(track => {
                    let localMediaContainer = document.getElementById('master-video');
                    localMediaContainer.appendChild(track.attach());
                });

            }

            Video.connect(data.data.token , connectOptions).then( room => {
                // Attach the Tracks of the Facilitator.
                // First Check if the user is a facilitator
                room.participants.forEach(participant => {
                    this.$http.get(`/api/get_user_details?email=${this.logged_user_email}`)
                        .then( data => {
                            if ( data.data.role != 'facilitator') {
                                let previewContainer = document.getElementById('master-video');
                                this.attachParticipantTracks(participant, previewContainer)
                            }
                        })

                });
            }, function(error) {
                console.error('Unable to connect to Room: ' +  error.message);
            });
         })

        // this.createChat('facilator-room');
     },
     // FUNCTIONS FOR CHAT
     async setupChannel(channel) {
      this.chat_channel = channel;
      channel.decline() // Unsubscribe from events
          .then( (channel) => {
              // Then join the channel
              channel.join().then( (channel) => {
                  channel.getMessages().then( messages => {
                      this.chat_messages = messages.items;
                  });

                  // Listen for new messages sent to the channel
                  channel.on('messageAdded', (message) => {
                    this.chat_messages.push(message.state);
                  });
              }).catch( (err) => {
                  // Listen for new messages sent to the channel
                  channel.on('messageAdded', (message) => {
                    this.chat_messages.push(message.state);
                  });

                  // If there is error joining the room,
                  // get all messages on the channel
                  channel.getMessages().then( messages => {
                      this.chat_messages = messages.items;
                  });
              });
          });
    },
    addMessage(message) {
      if (this.chat_channel) {
        this.chat_channel.sendMessage(message);
      }
    },
    async addChannel(uniqueName) {
        this.chat_client.createChannel({ uniqueName: uniqueName})
              .then(channel => (this.setupChannel(channel)) ) 
              .catch(error => {
                this.chat_client.getChannelByUniqueName(uniqueName)
                  .then( channel => (this.setupChannel(channel)) )
                  .catch( err => (console.log(err.message)) )
              });
      }
    // END FUNCTIONS FOR CHAT
  }
}
</script>

<style scoped>
  .card-height {
    height: 360px;
    margin: 4px;
    text-align: center;
  }
  #master-video {
    position: relative;
    margin: 0;
    /* width: 300px; */
    height: 250px;
    border: 1px solid red;
    overflow: hidden;
    margin: 10px;
  }
  .video-loading {
    margin-top: auto; 
    margin-top: 13%;
  }
</style>