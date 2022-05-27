<template>
  <div class="callbackPage">
    <h1>로그인 중...</h1>
  </div>
</template>

<script>
import axios from "axios";
import { BASE_SERVER_URL } from "@/config/index.js";
import { useStore } from "vuex";

export default {
  name: "GoogleCallback",
  data() {
    return {
      BASE_URL: "https://j6a502.p.ssafy.io/",
      access_token: null,
      code: null,
      store: useStore(),
    };
  },
  methods: {
    googleLogin() {
      const GOOGLE_CALLBACK_URI = this.BASE_URL + "googlecallback";
      const url = new URL(window.location.href);
      const urlParams = url.searchParams;
      const code = urlParams.get("code");
      this.code = code;

      axios({
        method: "post",
        url: "https://oauth2.googleapis.com/token",
        data: {
          redirect_uri: GOOGLE_CALLBACK_URI,
          client_id: process.env.VUE_APP_GOOGLE_OAUTH_CLIENT_ID,
          client_secret: process.env.VUE_APP_GOOGLE_OAUTH_SECRET_KEY,
          code: code,
          grant_type: "authorization_code",
        },
      })
        .then((res) => {
          this.access_token = res.data.access_token;
          axios({
            method: "get",
            url: `https://www.googleapis.com/oauth2/v2/userinfo?access_token=${this.access_token}`,
          })
            .then((res) => {
              axios({
                method: "post",
                url: BASE_SERVER_URL + "api/v1/accounts/googlelogin/",
                data: {
                  id: res.data.id,
                  email: res.data.email,
                  access_token: this.access_token,
                  code: this.code,
                },
              })
                .then((res) => {

                  if(res.data.valid) {
                    axios({
                      method: "post",
                      url: BASE_SERVER_URL + "api/v1/accounts/google/login/finish/",
                      data: {
                        access_token: this.access_token,
                        code: this.code,
                      },
                    })
                    .then((res) => {
                      // access_token 저장
                      console.log(res);
                      localStorage.setItem("jwt", "Bearer " + res.data.access_token);

                      // 사용자 정보 요청
                      axios({
                        method: 'get',
                        url: BASE_SERVER_URL + "api/v1/accounts/profile/",
                        headers: {
                          Authorization: localStorage.getItem('jwt'),
                        }
                      })
                        .then((res) => {
                          console.log(res)
                          this.store.commit("userStore/setUserName", res.data.user_name);
                          this.store.commit("userStore/setUserProfileImage", res.data.user_profile_image);
                          this.store.commit("userStore/setUserPhone", res.data.user_phone);
                          this.store.commit("userStore/setUserNotice", res.data.user_notice);
                        })

                      document.cookie = "cmc_token=kakao; max-age=7200; SameSite=Lax";
                      this.store.commit("userStore/setIsLogin", true);
                      window.location.href = "/";
                    })
                    .catch((err) => {
                      console.log(err)
                      alert("이미 존재하는 계정입니다.");
                    })                
                  }else {
                    console.log("valid false")
                    alert("이미 존재하는 계정입니다.");
                  }
                })
                .catch((err) => {
                  console.log(err);
                });
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  created: function () {
    this.googleLogin();
  },
};
</script>

<style></style>
