<template>
  <v-app id="inspire">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>Login form</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field prepend-icon="person" v-model="email" label="email" type="text"></v-text-field>
                  <v-text-field id="password" prepend-icon="lock" v-model="password" label="Password" type="password"></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" v-on:click="login">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  import { mapActions } from 'vuex'

  export default {
    data: () => ({
      email: "",
      password: "",
      loading: false
    }),
    props: {
      source: String
    },
    methods: {
        login() {
            this.loading = true;
            this.$http
                .post("/api/login", {
                    email: this.email,
                    password: this.password
                })
                .then(response => {
                    if (response.data.status == "success") {
                        const access_token = response.data.access_token
                        const user_data = response.data.user_data

                        this.proccessing = false;

                        this.updateUserRole(user_data.role)
                        this.updateAccessToken(access_token)
                        this.updateLoggedUserEmail(this.email)

                        this.$router.push('/')
                    } else {
                        this.message = "Login Faild, try again";
                    }
                })
                .catch(error => {
                    this.message = "Login Faild, try again";
                    this.proccessing = false;
                });
        },
        ...mapActions({
          updateLoggedUserEmail: 'updateLoggedUserEmail',
          updateUserRole: 'updateUserRole',
          updateAccessToken: 'updateAccessToken', // map this.updateAccessToken(access_token) 
                                                  // to this.$store.commit('updateAccessToken', access_token)
        })
    },
    created() {
    }
  }
</script>