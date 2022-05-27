<template>
  <div style="margin-top: 1%">
    <b-modal id="modal" size="lg" title="프로필사진 수정">
      <ProfileImageForm @selectedProfileImage="profileImageSelect" />
    </b-modal>
    <div id="profile_wrapper" class="border">
      <b-row>
        <b-col sm="3">
          <img :src="imagePath" size="15vmin" id="avatar" />
          <img
            src="@/assets/plus.png"
            v-b-modal.modal
            id="plusButton"
            v-if="isEdit"
          />
        </b-col>
        <b-col sm="6" v-if="isEdit == false">
          <div id="profile">
            <p>이름 {{ this.userInfo.user_name }}</p>
            <p>번호 {{ this.userInfo.user_phone }}</p>
          </div>
        </b-col>
        <b-col sm="3" v-if="isEdit == false">
          <button @click="editMyInfo">프로필 수정</button>
          <button
            @click="changePassword"
            v-if="this.userInfo.user_type == 'default'"
          >
            비밀번호 수정
          </button>
        </b-col>

        <b-col sm="6" v-else>
          <div id="profile">
            <div style="margin-bottom: 10px">
              <label for="name">이름</label>
              <input
                id="name"
                type="text"
                v-model="this.userInfo.user_name"
                class="userInfoInput"
              />
            </div>
            <div>
              <label for="phone">번호</label>
              <input
                id="phone"
                type="text"
                v-model="userInfo.user_phone"
                class="userInfoInput"
              />
            </div>
          </div>
        </b-col>
        <b-col sm="3" v-if="isEdit == true">
          <button @click="editMyInfo">완료</button>
          <button @click="cancelMyInfo">취소</button>
        </b-col>
      </b-row>
    </div>

    <div id="middle">
      <div id="calendar_wrapper" class="border">
        <Calendar />
      </div>
      <div id="ranking_wrapper" class="border">
        <Ranking :vmin="state.vmin" />
      </div>
    </div>
    <div id="heat_map" class="border">
      <HeatMap />
    </div>
    <!-- 
      분 단위
      운동 기록 테이블 -> 

      유저가 min max 를 지정 할 수 있게?

      최소 0분 최대 240분 default

     -->
  </div>
</template>

<script>
import Calendar from "@/components/Calendar.vue";
import HeatMap from "@/components/HeatMap.vue";
import Ranking from "@/components/Ranking.vue";
import ProfileImageForm from "../components/ProfileImageForm.vue";
import { reactive } from "@vue/reactivity";
import { API_BASE_URL } from "@/config/index.js";
import router from "@/router";
import axios from "axios";
// import * as report from "@/api/report.js";

export default {
  setup() {
    const state = reactive({
      vmin:
        window.innerHeight > window.innerWidth
          ? window.innerHeight / 100
          : window.innerWidth / 100,
    });
    return { state };
  },
  components: { Calendar, HeatMap, ProfileImageForm, Ranking },
  data: function () {
    return {
      userInfo: {
        user_name: "",
        user_profile_image: "",
        user_notice: "",
        user_phone: "",
        user_type: "",
      },
      isEdit: false,
      isChangeProfileImage: false,
      imagePath: "",
      // values: [],
    };
  },
  created() {
    this.userInfo.user_name = this.$store.state.userStore.userName;
    this.userInfo.user_profile_image =
      this.$store.state.userStore.userProfileImage;
    this.userInfo.user_notice = this.$store.state.userStore.userNotice;
    this.userInfo.user_phone = this.$store.state.userStore.userPhone;
    this.userInfo.user_type = this.$store.state.userStore.userType;
    this.imagePath = require("@/assets/images/profileImage" +
      this.userInfo.user_profile_image +
      ".png");
    // async () => {
    //   await report.getTimeReportList(
    //     ({ data }) => {
    //       for (let dat of data) {
    //         this.values.push({
    //           date: dat.timereport_day,
    //           count: dat.timereport_time,
    //         });
    //       }
    //       console.log(this.values);
    //     },
    //     (error) => {
    //       console.log(error);
    //     }
    //   );
    // };
  },
  methods: {
    editMyInfo: function () {
      if (this.isEdit) {
        axios({
          url: API_BASE_URL + "accounts/profile/",
          method: "put",
          data: this.userInfo,
          headers: {
            Authorization: localStorage.getItem("jwt"),
          },
        })
          .then((res) => {
            console.log(res);
            this.$store.commit(
              "userStore/setUserName",
              this.userInfo.user_name
            );
            this.$store.commit(
              "userStore/setUserPhone",
              this.userInfo.user_phone
            );
            this.$store.commit(
              "userStore/setUserProfileImage",
              this.userInfo.user_profile_image
            );
            this.isEdit = !this.isEdit;
          })
          .catch((err) => {
            console.log(err);
            alert("정보를 입력해주세요!");
          });
      } else {
        this.isEdit = !this.isEdit;
      }
    },
    cancelMyInfo: function () {
      this.isEdit = !this.isEdit;
    },
    changeMyProfileImage: function () {
      this.isChangeProfileImage = !this.isChangeProfileImage;
      console.log(this.isChangeProfileImage);
    },
    profileImageSelect: function (selectedImage) {
      this.userInfo.user_profile_image = selectedImage;
      this.imagePath = require("@/assets/images/profileImage" +
        this.userInfo.user_profile_image +
        ".png");
      this.isChangeProfileImage = !this.isChangeProfileImage;
    },
    changePassword: function () {
      router.push("changepassword");
    },
  },
};
</script>

<style scoped>
#profile_wrapper {
  width: 70%;
  height: 50%;
  padding-top: 3%;
  padding-bottom: 3%;
  position: relative;
  left: 50%;
  transform: translate(-50%, 0%);
}
#avatar {
  left: 10%;
  top: 50%;
  transform: translate(-10%, -50%);
  position: absolute;
  width: 10%;
}
#calendar_wrapper {
  /* position: relative; */
  width: 60%;
  /* padding-bottom: 10%; */
  height: 96%;
  /* left: 25%;
  transform: translate(-25%); */
}
#profile {
  position: relative;
  text-align: left;
  /* left: 50%; */
  /* top: 50%;
  transform: translate(-50%, -25%); */
  font-size: 2vmin;
  /* display: inline-block; */
}
#ranking_wrapper {
  position: relative;
  width: 38%;
  /* height: 10%; */
  /* padding-bottom: 15%; */
  margin-left: 2%;
}
#middle {
  display: flex;
  width: 70%;
  /* padding-bottom: 5%; */
  left: 50%;
  transform: translate(-50%, 0%);
  position: relative;
  margin-top: 2%;
  z-index: 50;
}
.border {
  box-shadow: 5px 5px 5px 1px rgba(192, 192, 192, 0.74);
  border-radius: 5px;
}
#heat_map {
  margin-top: 2%;
  margin-bottom: 10%;
  width: 80%;
  padding-top: 2%;
  padding-bottom: 1%;
  display: flex;
  left: 50%;
  width: 70%;
  transform: translate(-50%, 0%);
  position: relative;
  z-index: 3;
  margin-bottom: 1%;
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
  margin-bottom: 10px;
}

.userInfoInput {
  height: 40px;
  margin-left: 20px;
  border-top: none;
  border-left: none;
  border-right: none;
}

#plusButton {
  position: absolute;
  left: 16%;
  top: 65%;
  width: 2.5%;
  cursor: pointer;
}
</style>
