<template>
  <div id="register_from">
    <b-col cols="10">
      <b-card>
        회원가입
        <hr />
        <b-row>
          <b-col sm="3">
            <label for="registerEmail">이메일</label>
          </b-col>
          <b-col sm="5">
            <b-form-input id="registerEmail" v-model="credentials.email" @keyup.enter="signup"></b-form-input>
          </b-col>
          <b-col sm="4">
            <button
            id="emailCheckButton"
            @click="emailCheck"
            style="display: inline-block;">이메일 인증</button>
          </b-col>
        </b-row>
        <br />
        <b-row>
          <b-col sm="3">
            <label for="code">인증번호</label>
          </b-col>
          <b-col sm="5">
            <b-form-input
            id="code"
            v-model="code"
            @keyup.enter="signup"
            ></b-form-input>
          </b-col>
          <b-col sm="4">
            <button
            class="mx-1" variant="dark" id="AuthCodeCheckButton"
            @click="authCodeCheck"
              >인증번호 확인</button>
          </b-col>
        </b-row>
        <br />
        <b-row>
          <b-col sm="3">
            <label for="userPwd">비밀번호</label>
          </b-col>
          <b-col sm="9">
            <b-form-input
            id="userPwd"
            type="password"
            v-model="credentials.password"
            @keyup.enter="signup"
            ></b-form-input>
          </b-col>
        </b-row>
        <br />
        <b-row>
          <b-col sm="3">
            <label for="userPwdConfirm">비밀번호 확인</label>
          </b-col>
          <b-col sm="9">
            <b-form-input
            id="userPwdConfirm"
            type="password"
            v-model="credentials.passwordConfirmation"
            @keyup.enter="signup"
            ></b-form-input>
          </b-col>
        </b-row>
        <br />
        <b-row>
          <b-col sm="3">
            <label for="userName">이름</label>
          </b-col>
          <b-col sm="9">
            <b-form-input
            id="userName"
            v-model="credentials.userName"
            @keyup.enter="signup"
            ></b-form-input>
          </b-col>
        </b-row>
        <br />
        <b-row>
          <b-col sm="3">
            <label for="userPhone">휴대폰번호</label>
          </b-col>
          <b-col sm="9">
            <b-form-input
            id="userPhone"
            v-model="credentials.userPhone"
            @keyup.enter="signup"
            ></b-form-input>
          </b-col>
        </b-row>
        <br />
        <button
        class="mx-1" variant="dark" id="registerButton"
        @click="signup"
        >회원가입</button>
      </b-card>
    </b-col>
  </div>
</template>

<script scoped>

import axios from 'axios'
import { API_BASE_URL } from "@/config/index.js";

export default {
  name: "Register",
  data: function () {
    return {
      credentials: {
        email: null,
        userName: null,
        userPhone: null,
        password: null,
        passwordConfirmation: null,
      },
      auth_result: false,
      code: null,
      auth_code: null,
    }
  },
  methods: {
    signup: function() {
      if (this.auth_result == false) {
        alert('이메일 인증을 완료해주세요')
        document.getElementById("registerEmail").value = null;
      } else if (this.credentials.password != this.credentials.passwordConfirmation) {
        alert('비밀번호가 일치하지 않습니다')
        document.getElementById("userPwd").value = null;
        document.getElementById("userPwdConfirm").value = null;
      } else {
        axios({
          method: 'post',
          url: API_BASE_URL + 'accounts/signup/',
          data: {
            email: this.credentials.email,
            user_name: this.credentials.userName,
            user_phone: this.credentials.userPhone,
            password: this.credentials.password,
          }
        })
          .then(() => {
            alert('회원가입이 완료되었습니다')
            document.getElementById("registerEmail").value = null;
            document.getElementById("code").value = null;
            document.getElementById("userName").value = null;
            document.getElementById("userPhone").value = null;
            document.getElementById("userPwd").value = null;
            document.getElementById("userPwdConfirm").value = null;
            this.credentials.email = null;
            this.credentials.userName = null;
            this.credentials.userPhone = null;
            this.credentials.password = null;
            this.credentials.passwordConfirmation = null;
            this.auth_code = null;
            this.auth_result = false;
          })
          .catch(err => {
            console.log(err);
          })
      }
    },
    emailCheck() {
      axios({
        method: 'post',
        url: API_BASE_URL + 'accounts/email_auth/',
        data: {
          email: this.credentials.email,
        }
      })
        .then(res => {
          if (res.data.status == 1) {
            alert('중복된 이메일 입니다.')
            document.getElementById("registerEmail").value = null;
          } else if (res.data.status == 2) {
            this.auth_code = res.data.code
            alert('인증번호를 발송했습니다')
          } else {
            alert('유효한 이메일인지 확인해주세요')
            document.getElementById("registerEmail").value = null;
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    authCodeCheck() {
      if (this.code != null && this.code == this.auth_code) {
        this.auth_result = true
        alert('인증완료 되었습니다.')
      } else {
        alert('인증번호를 다시 입력해주세요')
        document.getElementById('code').value = null;
      }
    }
  }
};
</script>

<style>
#registerButton {
  border-radius: 4px;
}

#emailCheckButton {
  border-radius: 4px;
}

#AuthCodeCheckButton {
  border-radius: 4px;
}
</style>
