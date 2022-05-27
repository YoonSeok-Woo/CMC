<template>
  <div id="login_form">
    <b-col cols="10">
      <b-card>
        로그인
        <hr />
        <b-row>
          <b-col sm="3">
            <label for="email">이메일</label>
          </b-col>
          <b-col sm="9">
            <b-form-input
              id="email"
              v-model="this.credentials.email"
              @keyup.enter="login"
            ></b-form-input>
          </b-col>
        </b-row>
        <br />
        <b-row>
          <b-col sm="3">
            <label for="password">비밀번호</label>
          </b-col>
          <b-col sm="9">
            <b-form-input
              id="password"
              type="password"
              v-model="this.credentials.password"
              @keyup.enter="login"
            ></b-form-input>
          </b-col>
        </b-row>
        <br />
        <div>
          <button class="mx-1" id="loginButton" @click="login">로그인</button>
          <button class="mx-1" id="passwordButton" @click="changePasswordFlag">
            비밀번호 찾기
          </button>
        </div>
        <div id="findPasswordDiv" style="display: none">
          <FindPassword />
        </div>
        <hr style="margin-top: 30px" />
        <div>
          <img
            id="googleImage"
            src="@/assets/google.png"
            alt="구글"
            @click="googleLogin()"
          />
          <img src="@/assets/kakao.png" alt="카카오" @click="kakaoLogin()" />
        </div>
      </b-card>
    </b-col>
  </div>
</template>

<script scoped>
import FindPassword from "@/components/FindPassword.vue";
import axios from "axios";
import { API_BASE_URL } from "@/config/index.js";
import { useStore } from "vuex";
export default {
  name: "Login",
  components: {
    FindPassword,
  },
  data: function () {
    return {
      credentials: {
        email: null,
        password: null,
      },
      googleOauthClientID: process.env.VUE_APP_GOOGLE_OAUTH_CLIENT_ID,
      googleOauthRedirectUri: "https://j6a502.p.ssafy.io/googlecallback",
      kakaoOauthClientID: process.env.VUE_APP_KAKAO_CLIENT_ID,
      kakaoOauthRedirectUri: "https://j6a502.p.ssafy.io/kakaocallback",
      store: useStore(),
    };
  },
  methods: {
    login: function () {
      axios({
        method: "post",
        url: API_BASE_URL + "accounts/login/",
        data: this.credentials,
      })
        .catch(() => {
          alert("아이디와 비밀번호를 확인해주세요!");
        })
        .then((res) => {
          localStorage.setItem("jwt", "JWT " + res.data.token);

          // 사용자 정보 요청
          axios({
            method: "get",
            url: API_BASE_URL + "accounts/profile/",
            headers: {
              Authorization: localStorage.getItem("jwt"),
            },
          })
            .then((res) => {
              console.log(res);
              this.store.commit("userStore/setUserEmail", res.data.email);
              this.store.commit("userStore/setUserName", res.data.user_name);
              this.store.commit("userStore/setUserType", res.data.user_type);
              this.store.commit(
                "userStore/setUserProfileImage",
                res.data.user_profile_image
              );
              this.store.commit("userStore/setUserPhone", res.data.user_phone);
              this.store.commit(
                "userStore/setUserNotice",
                res.data.user_notice
              );
            })
            .catch((err) => {
              console.log(err);
            });

          document.cookie = "cmc_token=normal; max-age=7200; SameSite=Lax";
          this.store.commit("userStore/setIsLogin", true);
          window.location.href = "/";
        })
        .catch((err) => {
          console.log(err);
        });
    },
    googleLogin() {
      const googleOAuthURL = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${this.googleOauthClientID}&response_type=code&redirect_uri=${this.googleOauthRedirectUri}&scope=https://www.googleapis.com/auth/userinfo.email`;
      window.location.assign(googleOAuthURL);
    },
    kakaoLogin() {
      const kakaoOAuthURL = `https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=${this.kakaoOauthClientID}&redirect_uri=${this.kakaoOauthRedirectUri}`;
      window.location.assign(kakaoOAuthURL);
    },
    changePasswordFlag() {
      document
        .getElementById("findPasswordDiv")
        .setAttribute("style", "display: ");
    },
  },
};
</script>

<style scoped>
img {
  cursor: pointer;
}

#loginButton {
  width: 20vmin;
  cursor: pointer;
}
#passwordFlag {
  color: grey;
  text-decoration: underline;
  cursor: pointer;
}

button {
  width: 20vmin;
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  color: white;
  background-color: #212529;
  font-family: inherit;
  font-size: 1rem;
  border: 1px solid transparent;
  font-weight: 400;
  line-height: 1.5;
  cursor: pointer;
}

#findPasswordDiv {
  margin-top: 20px;
}

#googleImage {
  width: 183px;
  height: 50px;
  margin-right: 10px;
}
</style>
