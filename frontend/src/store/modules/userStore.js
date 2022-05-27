export const userStore = {
  namespaced: true,
  state: {
    userEmail: "",
    userName: "",
    userType: "",
    userPhone: "",
    userGrade: null,
    userProfileImage: "1",
    userNotice: 0,
    userRecordTime: null,
    userRecordCount: null,
    isLogin: false,
  },
  getters: {
    getIsLogin(state) {
      return state.isLogin;
    },
    getUserType(state) {
      return state.userType;
    },
    getUserNotice(state) {
      return state.userNotice;
    },
    getUserEmail(state) {
      return state.userEmail;
    },
    getUserName(state) {
      return state.userName;
    },
    getUserProfileImage(state) {
      return state.userProfileImage;
    },
  },
  mutations: {
    setUserName(state, userName) {
      state.userName = userName;
    },
    setUserType(state, userType) {
      state.userType = userType;
    },
    setIsLogin(state, isLogin) {
      state.isLogin = isLogin;
    },
    setUserEmail(state, userEmail) {
      state.userEmail = userEmail;
    },
    setUserNotice(state, userNotice) {
      state.userNotice = userNotice;
    },
    setUserProfileImage(state, userProfileImage) {
      state.userProfileImage = userProfileImage;
    },
    setUserPhone(state, value) {
      state.userPhone = value;
    },
  },
  actions: {},
};
