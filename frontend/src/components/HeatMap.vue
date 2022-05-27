<template>
  <div id="heatmap_wrapper">
    <calendar-heatmap
      :values="state.list"
      :max="state.max"
      :end-date="new Date()"
      :range-color="['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']"
      tooltip-unit="분 운동"
    />
  </div>
  <span id="idid">
    {{ state.space }}
  </span>
</template>

<script>
import { computed, onMounted } from "vue";
import { reactive, ref } from "@vue/reactivity";
import { CalendarHeatmap } from "vue3-calendar-heatmap";
import * as report from "@/api/report.js";
import { useStore } from "vuex";
export default {
  components: {
    CalendarHeatmap,
  },
  setup() {
    const store = useStore();
    const value = ref([]);

    const state = reactive({
      isLogin: computed(() => {
        return store.getters["userStore/getIsLogin"];
      }),
      space: "",
      list: [],
      max: 720,
    });

    const getTimeReportList = async () => {
      await report.getTimeReportList(
        ({ data }) => {
          setTimeout(() => {
            state.max++;
          }, 1);
          for (let dat of data) {
            state.list.push({
              date: dat.timereport_day,
              count: dat.timereport_time,
            });
            // value.value.push({
            //   date: dat.timereport_day,
            //   count: dat.timereport_time,
            // });
          }
        },
        (error) => {
          console.log(error);
        }
      );
      // console.log(value.value);
    };
    // { date: "2022-03-28", count: 4 },
    onMounted(() => {
      if (!state.isLogin) {
        return;
      }
      getTimeReportList();
    });

    return { state, getTimeReportList, value };
  },
};
</script>

<style scoped>
#heatmap_wrapper {
  width: 85%;
  font-size: 1vmin;
  margin: auto;
  z-index: 3;
}
#idid {
  font-size: 50px;
}
</style>
