import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import MyPage from "@/views/MyPage.vue";
import Enter from "@/components/Enter.vue";
import Exercise from "@/views/Exercise.vue";
import ChangePassword from "@/components/ChangePassword.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/googlecallback",
    name: "GoogleCallback",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/GoogleCallback.vue"),
  },
  {
    path: "/kakaocallback",
    name: "KakaoCallback",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/KakaoCallback.vue"),
  },
  {
    path: "/mypage",
    name: "MyPage",
    component: MyPage,
  },
  {
    path: "/login",
    name: "login",
    component: Enter,
  },
  {
    path: "/exercise",
    name: "Exercise",
    component: Exercise,
  },
  {
    path: "/changepassword",
    name: "ChangePassword",
    component: ChangePassword,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
