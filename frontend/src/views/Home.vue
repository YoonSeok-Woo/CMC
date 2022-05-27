<template>
  <div class="home" style="background-color: #ffefd6">
    <LandingPageVideo />
    <ProgramIntro />
  </div>
</template>

<script>
// @ is an alias to /src
import LandingPageVideo from "@/components/LandingPageVideo.vue";
import ProgramIntro from "@/components/ProgramIntro.vue";
export default {
  name: "Home",
  components: {
    ProgramIntro,
    LandingPageVideo,
  },
  created: function () {
    console.log(this.$store.state.userStore);
  }
};
</script>

<style>
.home {
  /* background-color: grey; */
  /* margin: 0 100px; */
  /* padding: 0; */
}
</style>
