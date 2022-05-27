<template>
  <div id="footer">
    <div>
      <ul id="menu_group" style="height: 100px">
        <ul class="menu" style="display: flex">
          <img id="teamLogo" src="@/assets/gitlab.png" />
          <div style="margin-left: 60px">
            <p class="infoList">☎️ 02) 123-1234</p>
            <p class="infoList" @click="kakaoChannel()" style="cursor: pointer">
              ✉️ 카카오톡 채널 링크
            </p>
            <p class="infoList">📧 cmc.ssafy@gmail.com</p>
            <p class="infoList">🏢 서울특별시 강남구 역삼동 테헤란로 212</p>
          </div>
        </ul>
        <ul class="menu"></ul>
        <ul></ul>
        <li></li>
        <ul class="menu">
          <p>Gitlab</p>
          <li>
            <img
              id="gitlabLogo"
              src="@/assets/gitlab.png"
              @click="openGitlab()"
            />
          </li>
        </ul>
      </ul>
    </div>
    <div>Copyright © A502 ALL Rights Reserved 2022<br /></div>
  </div>
</template>

<script>
import { onMounted } from "@vue/runtime-core";
export default {
  name: "app-footer",
  setup() {
    const openGitlab = () => {
      window.open("https://lab.ssafy.com/s06-ai-image-sub2/S06P22A502");
    };
    const kakaoChannel = () => {
      window.open("http://pf.kakao.com/_xdxbrNb");
    };
    const unDraggable = onMounted(() => {
      // window.document.onselectstart = new Function("return false");
    });
    return {
      openGitlab,
      kakaoChannel,
      unDraggable,
    };
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}

#gitlabLogo {
  width: 5vmin;
  height: 5vmin;
  cursor: pointer;
  /* border-radius: 50%;
  border: 1px solid white; */
}
li {
  list-style: none;
}
#footer {
  background-color: black;
  color: white;
}
#menu_group {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  height: 40px;
  margin-bottom: 50px;
}
.menu {
  margin-top: 25px;
}

#teamLogo {
  margin-top: 10px;
  width: 10vmin;
  height: 10vmin;
}

.infoList {
  margin-top: 5px;
  margin-bottom: 0px;
  font-size: 1.6vmin;
  text-align: left;
}
</style>
