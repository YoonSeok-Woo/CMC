<template>
  <div style="text-align: center;">
    <div>
      <img src="@/assets/images/profileImageSquare1.png" alt="1" @click="selectImage">
      <img src="@/assets/images/profileImageSquare2.png" alt="2" @click="selectImage">
      <img src="@/assets/images/profileImageSquare3.png" alt="3" @click="selectImage">
      <img src="@/assets/images/profileImageSquare4.png" alt="4" @click="selectImage">
    </div>
    <div>
      <img src="@/assets/images/profileImageSquare5.png" alt="5" @click="selectImage">
      <img src="@/assets/images/profileImageSquare6.png" alt="6" @click="selectImage">
      <img src="@/assets/images/profileImageSquare7.png" alt="7" @click="selectImage">
      <img src="@/assets/images/profileImageSquare8.png" alt="8" @click="selectImage">
    </div>
    <div>
      <img src="@/assets/images/profileImageSquare9.png" alt="9" @click="selectImage">
      <img src="@/assets/images/profileImageSquare10.png" alt="10" @click="selectImage">
      <img src="@/assets/images/profileImageSquare11.png" alt="11" @click="selectImage">
      <img src="@/assets/images/profileImageSquare12.png" alt="12" @click="selectImage">
    </div>

  </div>
</template>

<script>
export default {
  name: "ProfileImageForm",
  methods: {
    selectImage: function (e) {
      const selectedImage = e.target.alt
      console.log("image changed by " + selectedImage)

      this.$emit("selectedProfileImage", selectedImage)
    }
  }
}
</script>

<style>

img {
  width: 180px;
}
</style>
