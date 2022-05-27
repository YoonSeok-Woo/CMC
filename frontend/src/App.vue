<template>
  <div id="app">
    <div id="nav">
      <Header />
    </div>
    <router-view />
    <Footer id="footer" />
  </div>
  <notifications position="top cevnter" width="80%" />
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  components: {
    Header,
    Footer,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: auto;
  overflow-x: hidden;
}
#footer {
  /* position: absolute; */
  /* width: 100%; */
  bottom: 0px;
}
</style>
