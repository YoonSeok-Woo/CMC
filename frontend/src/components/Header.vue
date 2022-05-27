<template>
  <div id="header">
    <div id="nav_group">
      <b-row>
        <b-col cols="4">
          <img id="logo" src="@/assets/images/logo.png" @click="goMain()" />
        </b-col>
        <b-col cols="5"></b-col>
        <b-col cols="3" id="menu_group">
          <img
            src="@/assets/exercise.png"
            id="exercise"
            @click="goExercise()"
            v-if="state.isLogin"
          />
          &nbsp;
          <img
            src="@/assets/mypage.png"
            id="mypage"
            @click="goMypage()"
            v-if="state.isLogin"
          />
          &nbsp;
          <img
            src="@/assets/login.png"
            id="login"
            @click="login()"
            v-if="!state.isLogin"
          />
          &nbsp;
          <img
            src="@/assets/logout.png"
            id="logout"
            @click="logout()"
            v-if="state.isLogin"
          />
        </b-col>
      </b-row>
    </div>
  </div>
  <!-- TODO: 네비바 디자인 변경 요망 -->
</template>

<script>
import router from "@/router";
import { computed, onMounted, reactive } from "@vue/runtime-core";
import { notify } from "@kyvg/vue3-notification";
import { useStore } from "vuex";

export default {
  name: "Header",
  setup() {
    const store = useStore();
    const state = reactive({
      isLogin: computed(() => {
        return store.getters["userStore/getIsLogin"];
      }),
    });
    const goMypage = () => {
      router.push("mypage");
    };
    const goMain = () => {
      router.push("/");
    };
    const login = () => {
      router.push("login");
    };
    const logout = () => {
      document.cookie = "cmc_token=; max-age=0; SameSite=Lax;";
      localStorage.removeItem("jwt");
      store.commit("userStore/setIsLogin", false);
      notify({
        title: "정상적으로 로그아웃 되었습니다.",
        speed: 300,
        duration: 1000,
        type: "success",
      });
      window.location.href = "/";
    };
    const goExercise = () => {
      router.push("exercise");
    };
    onMounted(() => {});
    const getCookie = (cookie_name) => {
      // 출처 : https://webisfree.com/2015-02-04/[%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8]-%EC%BF%A0%ED%82%A4(cookie)-%EC%A0%80%EC%9E%A5-%EB%B0%8F-%EC%82%AD%EC%A0%9C-%EC%98%88%EC%A0%9C%EB%B3%B4%EA%B8%B0
      var x, y;
      var val = document.cookie.split(";");

      for (var i = 0; i < val.length; i++) {
        x = val[i].substr(0, val[i].indexOf("="));
        y = val[i].substr(val[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, ""); // 앞과 뒤의 공백 제거하기
        if (x == cookie_name) {
          return unescape(y); // unescape로 디코딩 후 값 리턴
        }
      }
      return undefined;
    };
    return {
      state,
      goMypage,
      goMain,
      login,
      logout,
      getCookie,
      goExercise,
    };
  },
};
</script>

<style scoped>
#header {
  /* margin-bottom: 1%; */
  border-bottom: 1px solid rgba(128, 128, 128, 0.384);
  /* box-shadow: 1px 0 0 1px rgba(128, 128, 128, 0.384); */
}
#nav_group {
  padding: 0.5vmin;
}
#login {
  width: 4vmin;
}
#logout {
  width: 4vmin;
}
#mypage {
  width: 4vmin;
}
#exercise {
  width: 5vmin;
}
#go_main {
  cursor: pointer;
}
img {
  cursor: pointer;
}
#logo {
  width: 27.5vmin;
}
.opacity {
  opacity: 65%;
}
#menu_group {
  margin: auto;
}
</style>
