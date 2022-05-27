<template>
  <div>
    <div id="selected_day_wrapper">
      <span id="month">{{ state.month + 1 }}</span>
      <span id="day">{{ state.day }}</span>
    </div>
    <div id="clock_wrapper">
      <div id="tui-time-picker-container"></div>
    </div>
    <div>
      <b-form-input
        id="schedule_content"
        v-model="state.value"
        placeholder="오늘은 무슨 운동할까요?"
      ></b-form-input>
    </div>
    <div id="button_group">
      <div v-if="state.flag">
        <b-button class="mx-1 button" variant="outline-success" @click="confirm"
          >확인</b-button
        >
        <b-button class="mx-1 button" variant="outline-danger" @click="cancle"
          >취소</b-button
        >
      </div>
      <div v-if="!state.flag">
        <b-button class="mx-1 button" variant="outline-warning" @click="modify"
          >수정</b-button
        >
        <b-button class="mx-1 button" variant="outline-danger" @click="remove"
          >삭제</b-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import TimePicker from "tui-time-picker";
import { reactive } from "@vue/reactivity";
import { onMounted, watch } from "@vue/runtime-core";
import { notify } from "@kyvg/vue3-notification";
export default {
  name: "ScheduleFrom",
  props: {
    selectedDay: Date,
    selectedContent: String,
    selectedFlag: Boolean,
    selectedId: Number,
  },
  setup(props, { emit }) {
    const state = reactive({
      value: "",
      year: "",
      month: "",
      day: "",
      hour: "",
      minute: "",
      instance: "",
      flag: true,
      id: "",
    });
    const dayWatcher = watch(
      () => props.selectedDay,
      () => {
        state.month = props.selectedDay.getMonth();
        state.day = props.selectedDay.getDate();
        state.year = props.selectedDay.getFullYear();
        state.hour = props.selectedDay.getHours();
        state.minute = props.selectedDay.getMinutes();
        state.instance.setTime(state.hour, state.minute);
      }
    );
    const contentWatcher = watch(
      () => props.selectedContent,
      () => {
        state.value = props.selectedContent;
      }
    );
    const flagWatcher = watch(
      () => props.selectedFlag,
      () => {
        state.flag = props.selectedFlag;
      }
    );
    const idWatcher = watch(
      () => props.selectedId,
      () => {
        state.id = props.selectedId;
      }
    );
    const confirm = () => {
      if (!state.value) {
        notify({
          title: "운동 내용을 입력해주세요!",
          speed: 300,
          duration: 1000,
          type: "error",
        });
        return;
      }
      const time = `${state.year}-${state.month + 1}-${
        state.day
      } ${state.instance.getHour()}:${state.instance.getMinute()}`;
      const content = state.value;

      emit("confirm", { time: time, content: content });
    };
    const modify = () => {
      if (!state.value) {
        notify({
          title: "운동 내용을 입력해주세요!",
          speed: 300,
          duration: 1000,
          type: "error",
        });
        return;
      }
      const time = `${state.year}-${state.month + 1}-${
        state.day
      } ${state.instance.getHour()}:${state.instance.getMinute()}`;
      const content = state.value;
      emit("modify", { time: time, content: content, id: state.id });
    };
    const cancle = () => {
      state.value = "";
      state.hour = "";
      state.minute = "";
      emit("cancle");
    };
    const remove = () => {
      emit("remove", state.id);
    };
    onMounted(() => {
      TimePicker.localeTexts["customKey"] = {
        am: "a.m.",
        pm: "p.m.",
      };
      const container = document.getElementById("tui-time-picker-container");
      state.instance = new TimePicker(container, {
        initialHour: state.hour,
        initialMinute: state.minute,
        inputType: "spinbox",
        showMeridiem: false,
        minuteStep: 30,
      });
    });
    return {
      state,
      confirm,
      modify,
      cancle,
      dayWatcher,
      remove,
      contentWatcher,
      flagWatcher,
      idWatcher,
    };
  },
};
</script>

<style scoped>
#selected_day_wrapper {
  margin-bottom: 5%;
}
.button {
  width: 30%;
  bottom: 5%;
  position: relative;
}
#tui-time-picker-container {
  margin-bottom: 5%;
}
#schedule_content {
  margin-bottom: 5%;
}
#month {
  font-size: 10vmin;
}
#day {
  font-size: 5vmin;
  /* opacity: 80%; */
  margin-left: 5%;
  font: gray;
}
</style>
