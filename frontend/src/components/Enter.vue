<template>
  <div style="margin-top: 3%; margin-bottom: 8%">
    <b-container fluid id="area_wrapper">
      <b-row align="center">
        <b-col>
          <Login />
        </b-col>
        <b-col>
          <Register />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";
export default {
  name: "Enter",
  components: {
    Login,
    Register,
  },
};
</script>

<style scoped>
#aera_wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 100vmin;
}
</style>
