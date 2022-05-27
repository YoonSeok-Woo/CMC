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
  name: "KakaoCallback",
  data() {
    return {
      BASE_URL: "https://j6a502.p.ssafy.io/",
      access_token: null,
      code: null,
      store: useStore(),
    };
  },
  methods: {
    kakaoLogin() {
      const KAKAO_CALLBACK_URI = this.BASE_URL + "kakaocallback";
      const url = new URL(window.location.href);
      const urlParams = url.searchParams;
      const code = urlParams.get("code");
      this.code = code;

      const kakaoHeader = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
      };

      const bodyData = {
        grant_type: "authorization_code",
        client_id: process.env.VUE_APP_KAKAO_CLIENT_ID,
        redirect_uri: KAKAO_CALLBACK_URI,
        code: code,
      };
      const queryStringBody = Object.keys(bodyData)
        .map((k) => encodeURIComponent(k) + "=" + encodeURI(bodyData[k]))
        .join("&");

      console.log(queryStringBody);

      axios({
        method: "post",
        url: `https://kauth.kakao.com/oauth/token`,
        data: queryStringBody,
        headers: kakaoHeader,
      })
        .then((res) => {
          console.log("토큰 결과값");
          console.log(res);
          this.access_token = res.data.access_token;
          console.log(this.access_token);

          console.log("access token");
          console.log(this.access_token);
          // 로그인
          axios({
            method: "post",
            url: BASE_SERVER_URL + "api/v1/accounts/kakaologin/",
            data: {
              access_token: this.access_token,
              code: this.code,
            },
          })
            .then((res) => {

              if(res.data.valid) {
                axios({
                  method: "post",
                  url: BASE_SERVER_URL + "api/v1/accounts/kakao/login/finish/",
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
    },
  },
  created: function () {
    this.kakaoLogin();
  },
};
</script>

<style>
  .callbackPage {
    height: 74vh;
    padding-top: 30vh;
  }
</style>
