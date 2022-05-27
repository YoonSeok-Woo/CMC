<template>
  <div id="calendar">
    <div id="alarm_confirm">
      <img
        src="https://user-images.githubusercontent.com/63468607/159424104-1bafb828-7c19-44a2-9e73-8e4592af5989.png"
        class="alarm"
        id="agree"
        @click="
          () => {
            state.alarmConfirm = false;
          }
        "
      />
      <img
        src="https://user-images.githubusercontent.com/63468607/159424363-4c0e0386-a025-4722-b77d-a70c19f56672.png"
        class="alarm"
        id="disagree"
        @click="
          () => {
            state.alarmConfirm = true;
          }
        "
      />
    </div>
    <div id="month_wrapper">
      <img src="@/assets/left.png" id="prev" @click="prevMonth" />
      <span id="month">{{ state.currentMonth + 1 }}</span>
      <span id="year">{{ state.currentYear }}</span>
      <img src="@/assets/right.png" id="next" @click="nextMonth" />
    </div>
    <table id="day_wrapper">
      <thead>
        <tr id="week">
          <th class="ft_red">Sun</th>
          <th>Mon</th>
          <th>Tue</th>
          <th>Wed</th>
          <th>Thu</th>
          <th>Fri</th>
          <th class="ft_blue">Sat</th>
        </tr>
      </thead>
      <tbody id="tBody"></tbody>
    </table>
  </div>
  <div id="my_context" class="border">
    <img
      src="https://cdn-icons-png.flaticon.com/512/966/966615.png"
      class="close_button"
      @click="
        () => {
          state.myContextFlag = false;
        }
      "
    />
    <div id="form_wrapper">
      <ScheduleFrom
        :selectedDay="state.propDay"
        :selectedContent="state.propContent"
        :selectedFlag="state.propFlag"
        :selectedId="state.propId"
        v-on:confirm="confirm"
        v-on:modify="modify"
        v-on:cancle="cancle"
        v-on:remove="remove"
      />
      <!-- 2021-03-29 15:00 -->
    </div>
  </div>
</template>

<script>
import { reactive } from "@vue/reactivity";
import { onMounted, watch } from "@vue/runtime-core";
import ScheduleFrom from "@/components/ScheduleFrom.vue";
import { notify } from "@kyvg/vue3-notification";
import * as schedule from "@/api/schedule.js";
export default {
  components: {
    ScheduleFrom,
  },
  setup() {
    const monthList = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    const dayList = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const today = new Date();
    const state = reactive({
      currentMonth: new Date().getMonth(),
      currentYear: new Date().getFullYear(),
      myContextFlag: false,
      alarmConfirm: false,
      propDay: new Date(),
      propContent: String,
      propFlag: true,
      propId: Number,
      scheduleList: [],
      scheduleMap: new Map(),
    });
    const makeCalendar = async (day) => {
      let target = document.getElementById("tBody");
      while (target.hasChildNodes()) {
        target.removeChild(target.firstChild);
      }
      let dayCount = 1;
      let year = day.getFullYear();
      let month = day.getMonth();
      let firstDay = new Date(year, month, 1).getDay();
      let endDay = new Date(year, month + 1, 0);
      await getMonthlySchedule();
      for (let i = 0; i < 6; i++) {
        let tr = document.createElement("tr");
        if (i > 0) firstDay = 0;
        for (let j = 0; j < 7; j++) {
          let td = document.createElement("td");
          td.classList.add("day");
          let span = document.createElement("span");
          if (j < firstDay) {
            tr.appendChild(td);
            continue;
          }
          if (dayCount > endDay.getDate()) break;
          if (
            today.toDateString() ===
            new Date(year, month, dayCount).toDateString()
          )
            span.id = "today";
          if (state.scheduleMap.has(`${dayCount}`)) {
            let img = document.createElement("img");
            img.src =
              "https://user-images.githubusercontent.com/63468607/159395395-f1258bf9-7394-45d2-90ff-458baa7d2438.png";
            img.classList.add("schedule_badge");
            td.appendChild(img);
          }
          span.innerText = dayCount;
          if (j === 0) span.classList.add("ft_red");
          else if (j === 6) span.classList.add("ft_blue");
          dayCount++;
          // span.appendChild(img);
          td.appendChild(span);
          td.addEventListener("click", (event) => {
            let hour = 12;
            let minute = 0;
            let content = "";
            state.propFlag = true;
            if (state.scheduleMap.has(event.target.innerText)) {
              const day = event.target.innerText;
              const obj = state.scheduleMap.get(day);
              hour = obj.hour;
              minute = obj.minute;
              content = obj.content;
              state.propFlag = false;
              state.propId = obj.id;
            }
            state.myContextFlag = false;
            state.propDay = new Date(
              state.currentYear,
              state.currentMonth,
              event.target.innerText,
              hour,
              minute
            );
            state.propContent = content;
            state.myContextFlag = true;
          });
          tr.appendChild(td);
        }
        target.appendChild(tr);
        if (dayCount > endDay.getDate()) break;
      }
    };
    const init = onMounted(() => {
      makeCalendar(new Date());
    });
    const nextMonth = () => {
      state.currentMonth = state.currentMonth + 1;
      if (state.currentMonth > 11) {
        state.currentMonth = 0;
        state.currentYear++;
      }
    };
    const prevMonth = () => {
      state.currentMonth = state.currentMonth - 1;
      if (state.currentMonth < 0) {
        state.currentMonth = 11;
        state.currentYear--;
      }
    };
    const switctContextBox = watch(
      () => state.myContextFlag,
      () => {
        if (state.myContextFlag) {
          document.getElementById("my_context").style.display = "block";
        } else document.getElementById("my_context").style.display = "none";
      }
    );
    const updateCalendar = watch(
      () => [state.currentMonth, state.currentYear],
      () => {
        makeCalendar(new Date(state.currentYear, state.currentMonth, 1));
      }
    );
    const newSchedule = () => {};
    const watchAlarm = watch(
      () => state.alarmConfirm,
      () => {
        toggleAlarm();
      }
    );
    const toggleAlarm = () => {
      let agree = document.getElementById("agree");
      let disagree = document.getElementById("disagree");
      if (state.alarmConfirm) {
        agree.style.display = "block";
        disagree.style.display = "none";
        showAlert(state.alarmConfirm);
      } else {
        disagree.style.display = "block";
        agree.style.display = "none";
        showAlert(state.alarmConfirm);
      }
    };
    const showAlert = (alert) => {
      // TODO : User notice 1 : 미신청, 2 : 승인대기 , 3 : 승인
      // 1에서 버튼 클릭하면 승인대기 이미지로 변경

      if (alert)
        notify({
          title: "내 일정을 카카오알림으로 받을래요!",
          speed: 300,
          duration: 1000,
          type: "success",
        });
      else
        notify({
          title: "내 일정을 카카오알림으로 받지 않을래요!",
          speed: 300,
          duration: 1000,
          type: "warn",
        });
    };
    const getMonthlySchedule = async () => {
      const params = {
        year: state.currentYear,
        month: state.currentMonth + 1,
      };
      await schedule.getMonthlySchedule(
        params,
        ({ data }) => {
          state.scheduleList = data;
          state.scheduleMap = new Map();
          for (let sch of state.scheduleList) {
            const newDay = sch.schedule_time;
            const day = newDay.split("T")[0].split("-")[2].replace(/(^0+)/, "");
            const hour = newDay.split("T")[1].split(":")[0];
            const minute = newDay.split("T")[1].split(":")[1];
            const content = sch.schedule_title;
            state.scheduleMap.set(day, {
              id: sch.schedule_id,
              hour: hour,
              minute: minute,
              content: content,
            });
          }
        },
        (error) => {
          console.log(error);
        }
      );
    };
    onMounted(() => {
      // toggleAlarm();
    });
    const confirm = async (params) => {
      await schedule.postSchedule(params);
      makeCalendar(new Date(state.currentYear, state.currentMonth, 1));
      state.myContextFlag = false;
    };
    const modify = async (params) => {
      await schedule.putSchedule(params);
      makeCalendar(new Date(state.currentYear, state.currentMonth, 1));
      state.myContextFlag = false;
    };
    const cancle = () => {
      state.myContextFlag = false;
    };
    const remove = async (id) => {
      await schedule.deleteSchedule(
        id,
        ({ data }) => {
          console.log(data);
        },
        (error) => {
          console.log(error);
        }
      );
      makeCalendar(new Date(state.currentYear, state.currentMonth, 1));
      state.myContextFlag = false;
    };
    return {
      monthList,
      dayList,
      today,
      state,
      makeCalendar,
      init,
      nextMonth,
      prevMonth,
      updateCalendar,
      newSchedule,
      switctContextBox,
      toggleAlarm,
      watchAlarm,
      showAlert,
      getMonthlySchedule,
      confirm,
      cancle,
      remove,
      modify,
    };
  },
};
</script>

<style>
#month {
  font-size: 5vmin;
  margin: 1%;
  cursor: pointer;
}
#year {
  font-size: 2vmin;
  cursor: pointer;
}
.day {
  font-size: 2vmin;
  cursor: pointer;
  position: relative;
}
#week {
  font-size: 2vmin;
}
#day_wrapper {
  width: 100%;
  height: 100%;
  position: inherit;
}
#prev {
  width: 4vmin;
  cursor: pointer;
  margin-bottom: 1.5vmin;
}
#next {
  width: 4vmin;
  cursor: pointer;
  margin-bottom: 1.5vmin;
}
#calendar {
  position: relative;
  height: 100%;
}
#month_wrapper {
  height: 30%;
  margin-bottom: 2%;
}
.ft_red {
  color: red;
}
.ft_blue {
  color: blue;
}
.schedule_badge {
  width: 0.9vmin;
  top: 5%;
  left: 60%;
  position: absolute;
  pointer-events: none;
}
#my_context {
  position: absolute;
  left: 50%;
  top: -50%;
  padding-bottom: 40%;
  width: 40%;
  transform: translate(-50%, 0%);
  background: white;
  z-index: 50000;
  display: none;
}
#form_wrapper {
  width: 90%;
  height: 90%;
  top: 50%;
  left: 50%;
  position: inherit;
  transform: translate(-50%, -50%);
}
.close_button {
  cursor: pointer;
  position: absolute;
  top: 5%;
  left: 90%;
  width: 2vmin;
  height: 2vmin;
  z-index: 550;
}
.alarm {
  width: 4vmin;
  height: 4vmin;
  cursor: pointer;
  position: absolute;
  left: 5%;
  top: 5%;
}
.hide {
  display: none;
}
.show {
  display: block;
}
.border {
  border-radius: 5px;
}

#calendar {
  padding-top: 2%;
  padding-bottom: 3%;
}
</style>
