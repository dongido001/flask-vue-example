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
                <Rooms />
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

                <v-card dark tile flat color="" class="card-height">
                    <v-toolbar-title>Ragamuffings Chat</v-toolbar-title>
                    <v-card-text>
                      <div class="chat-message">
                        <v-list-tile-avatar class="circle">
                          <img src="https://picsum.photos/250/300?image=783">
                        </v-list-tile-avatar>
                        Lo-fi you probably haven't heard of them etsy leggings raclette kickstarter four dollar toast. 
                        Raw denim fingerstache food truck chia health goth synth. Forage man bun intelligentsia freegan 
                        PBR&B banh mi asymmetrical chambray.
                      </div>

                      <div class="chat-message right">
                        <v-list-tile-avatar class="circle">
                          <img src="https://picsum.photos/250/300?image=783">
                        </v-list-tile-avatar>
                        Lo-fi you probably haven't heard of them.
                      </div>

                      <div class="chat-message">
                        <v-list-tile-avatar class="circle">
                          <img src="https://picsum.photos/250/300?image=783">
                        </v-list-tile-avatar>
                        Raw denim fingerstache food truck chia health goth synth.
                      </div>
                    </v-card-text>

                    <v-container fluid grid-list-md text-xs-center class="input-form">
                      <v-layout row wrap>
                          <v-flex xs12 md12>
                            <v-textarea
                              v-model="chat"
                              box
                              label="message"
                              rows="1"
                              width="50px"
                            ></v-textarea>
                          </v-flex>
                            <button type="submit" style="margin-left: -30px; z-index: 3;">
                              <i class="material-icons">send</i>
                            </button>
                      </v-layout>
                    </v-container>
                </v-card>
            </v-flex>

            <v-flex xs6>
                <v-card dark tile flat color="red darken-4" class="card-height">
                    <v-toolbar-title>Master Video Feed</v-toolbar-title>
                    <v-card-text>
                        <v-progress-circular
                          :size="70"
                          :width="7"
                          indeterminate
                          v-if="video_room_loading"
                          class="video-loading"
                        ></v-progress-circular>
                        <div id="master-video" v-else></div>
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
import { EventBus } from '../../Event'
import Video from 'twilio-video'
const Chat = require('twilio-chat')
import axios from 'axios'
import Rooms from './Rooms'
import Footer from './Footer'

export default {
  name: 'App',
  components: {
    Rooms,
    Footer
  },
    props: {
        email: String
    },
  data () {
    return {
      chat: null,
      authenticated: true,
      video_room_loading: false,
      active_room: null,
      video_client: null,
      chat_client: null,
      room_name: null
    }
  },
  props: ['email'],
  created() {
    EventBus.$on('show_room', (room) => {
        this.createChat(room);
    })

    // this.createChat('master');

    // When we are about to transition away from this page, disconnect
    // from the room, if joined.
    window.addEventListener('beforeunload', this.leaveRoomIfJoined);

  },
  methods: {
    setAuthenticated(access_token) {
      localStorage.auth = access_token
      this.authenticated = true
    },
    async getAccessToken() {
      return await axios
                    .post("/api/generate_video_token", {
                      identity: this.email,
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
         
        let VueThis = this

        this.getAccessToken().then( (data) => {

            if (data.status != 200) {
               return 
            } 

            this.video_room_loading = true
            VueThis.room_name = null

            const token = data.data.token

            let connectOptions = {
                name: room_name,
                // logLevel: 'debug',
                audio: true, 
                video: { width: 120, height: 120 }
            };

            this.leaveRoomIfJoined();
            
            // remove any remote track when joining a new room
            // document.getElementById('remoteTrack').innerHTML = ""; 

            Chat.Client.create( token )
                .then( (client) => {
                    client.getPublicChannelDescriptors()
                        .then( channels => { /*this.channels = channels.state.items } */ });
                    this.chat_client = client;
                });

            Video.connect(token , connectOptions).then( room => {

                this.dispatchLog('Successfully joined a Room: '+ room_name);

                // set active toom
                this.active_room = room;
                this.room_name = room_name;
                this.video_room_loading = false

                // Attach the Tracks of the Room's Participants.
                room.participants.forEach(function(participant) {
                    console.log(participant)
                    let previewContainer = document.getElementById('team-video');
                    this.attachParticipantTracks(participant, previewContainer);
                });

                // When a Participant joins the Room, log the event.
                room.on('participantConnected', function(participant) {
                    this.dispatchLog("Joining: '" + participant.identity + "'");
                });

                // When a Participant adds a Track, attach it to the DOM.
                room.on('trackSubscribed', function(track, participant) {
                    this.dispatchLog(participant.identity + " added track: " + track.kind);
                    let previewContainer = document.getElementById('team-video');
                    this.attachTracks([track], previewContainer);
                });
                
                // When a Participant removes a Track, detach it from the DOM.
                room.on('trackUnsubscribed', function(track, participant) {
                    this.dispatchLog(participant.identity + " removed track: " + track.kind);
                    this.detachTracks([track]);
                });

                // When a Participant leaves the Room, detach its Tracks.
                room.on('participantDisconnected', function(participant) {
                    this.dispatchLog("Participant '" + participant.identity + "' left the room");
                    this.detachParticipantTracks(participant);
                });

                if(!this.localTrack) {
                    Video.createLocalVideoTrack().then(track => {
                      console.group(track)
                      let localMediaContainer = document.getElementById('master-video');
                      localMediaContainer.appendChild(track.attach());

                      this.localTrack = true;
                    });
                }
            }, function(error) {
                console.error('Unable to connect to Room: ' +  error.message);
            });

          });
     },
     dispatchLog(message) {
        EventBus.$emit('new_log', message);
     }
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
  .video-loading {
    margin-top: auto; 
    margin-top: 13%;
  }
</style>