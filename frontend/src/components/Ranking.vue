<template>
  <BarChart
    :chartData="testData"
    :height="13 * state.vmin"
    :options="options"
  />
</template>

<script>
import { computed, defineComponent, reactive, onMounted, ref } from "vue";
import { BarChart } from "vue-chart-3";
import { Chart, registerables } from "chart.js";
import * as report from "@/api/report.js";
import { useStore } from "vuex";
Chart.register(...registerables);

export default defineComponent({
  name: "Ranking",
  components: { BarChart },
  props: { vmin: Number },
  setup(props) {
    const store = useStore();
    var data = ref([2, 2, 2]);
    const state = reactive({
      vmin: computed(() => {
        return props.vmin;
      }),
      timeRanking: Number,
      daysRanking: Number,
      consecutiveDaysRanking: Number,
      total: Number,
      isLogin: computed(() => {
        return store.getters["userStore/getIsLogin"];
      }),
    });

    const getRank = async () => {
      await report.getRank(
        ({ data }) => {
          state.timeRanking = data.time_ranking;
          state.daysRanking = data.days_ranking;
          state.consecutiveDaysRanking = data.consecutive_days_ranking;
          state.total = data.total;
          console.log(data);
        },
        (error) => {
          console.log(error);
        }
      );
      data.value[0] = (
        ((state.total - state.timeRanking + 1) / state.total) *
        100
      ).toFixed(2);
      data.value[1] = (
        ((state.total - state.consecutiveDaysRanking + 1) / state.total) *
        100
      ).toFixed(2);
      data.value[2] = (
        ((state.total - state.daysRanking + 1) / state.total) *
        100
      ).toFixed(2);
    };
    const testData = {
      labels: ["운동 시간", "연속 운동 일수", "전체 운동 일수"],
      datasets: [
        {
          data: data.value,
          backgroundColor: [
            "#77CEFF",
            "#0079AF",
            "#123E6B",
            "#97B0C4",
            "#A5C8ED",
          ],
        },
      ],
    };
    const options = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxis: {
          max: 100,
        },
      },
      plugins: {
        legend: false,
        title: {
          display: true,
          text: "나의 운동 랭킹(%)",
        },
      },
    };
    onMounted(() => {
      if (state.isLogin) {
        getRank();
      }
    });
    return { testData, options, state, data };
  },
});
</script>
<style scoped></style>
