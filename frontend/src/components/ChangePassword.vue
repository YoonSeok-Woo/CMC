<template>
  <div>
    <b-container fluid style="margin-top: 30px; margin-bottom: 400px">
      <b-row align="center">
        <b-col sm="2"></b-col>
        <b-col sm="8">
          <b-row>
            <b-col sm="3">
              <label for="originalPassword">이전 비밀번호</label>
            </b-col>
            <b-col sm="9">
              <b-form-input
                id="originalPassword"
                type="password"
                v-model="this.originalPassword"></b-form-input>
            </b-col>
          </b-row>
          <br />

          <b-row>
            <b-col sm="3">
              <label for="newPassword">새 비밀번호</label>
            </b-col>
            <b-col sm="9">
              <b-form-input
                id="newPassword"
                type="password"
                v-model="this.newPassword"></b-form-input>
            </b-col>
          </b-row>
          <br />

          <b-row>
            <b-col sm="3">          
              <label for="newPasswordConfirmation">새 비밀번호 확인</label>
            </b-col>
            <b-col sm="9">  
              <b-form-input
                id="newPasswordConfirmation" 
                type="password"
                v-model="this.newPasswordConfirmation"></b-form-input>    
            </b-col>
          </b-row>
          <br />

          <button
            class="mx-1" variant="dark" id="changePasswordButton"
            @click="changePassword"
            style="margin-top: 20px; border-radius: 4px;"
            >비밀번호 변경</button>
        </b-col>
        <b-col sm="2"></b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios"
import { API_BASE_URL } from "@/config/index.js";

export default {
  name: "ChangePassword",
  data: function () {
    return {
      originalPassword: null,
      newPassword: null,
      newPasswordConfirmation: null,
    }
  },
  methods: {
    changePassword: function() {
      if (this.newPassword != this.newPasswordConfirmation) {
        alert("비밀번호를 확인해주세요")
      } else {
        axios({
          method: 'post',
          url: API_BASE_URL + "accounts/password/",
          headers: { Authorization: localStorage.getItem('jwt')},
          data: {
            'newPassword': this.newPassword,
          }
        })
          .then(res => {
            console.log(res)
            alert('비밀번호가 수정되었습니다')
          })
          .catch(err => {
            console.log(err)
          })
      }
    }
  }
}
</script>

<style>

</style>