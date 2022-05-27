<template>
  <div>
    <div>
      <b-row>
        <b-col sm="3">
          <label for="email">이메일</label>
        </b-col>
        <b-col sm="5">
          <b-form-input
            id="email"
            v-model="this.email"
          ></b-form-input>
        </b-col>
        <b-col sm="4">
          <button
            id="findPaswwordButton"
            @click="sendPassword"
            >임시 비밀번호 전송</button>
        </b-col>
      </b-row>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from "@/config/index.js";

export default {
  name: "FindPassword",
  data: function () {
    return {
      email: null,
    }
  },
  methods: {
    sendPassword: function() {
      axios({
        method: 'post',
        url: API_BASE_URL + "accounts/temp_password/",
        data: {
          'email': this.email,
        }
      })
        .then(res => {
          if (res.status == 204) {
            alert('이메일을 확인해주세요')
          } else if (res.status == 203) {
            alert(`${res.data.message}로 가입한 계정입니다`)
          } else {
            alert('임시 비밀번호가 발송되었습니다.')
          }
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>

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
}

#findPaswwordButton {
  border-radius: 4px;
}
</style>