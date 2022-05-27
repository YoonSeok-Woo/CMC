import { apiInstance } from "./index.js";

const api = apiInstance();

async function getMonthlySchedule(params, success, fail) {
  const year = params.year;
  const month = params.month;
  await api
    .get(`schedules/monthly_schedule/${year}/${month}`)
    .then(success)
    .catch(fail);
}

async function postSchedule(params, success, fail) {
  await api
    .post(`schedules/schedules/`, {
      schedule_time: params.time,
      schedule_title: params.content,
    })
    .then(success)
    .catch(fail);
}
async function putSchedule(params, success, fail) {
  const id = params.id;
  console.log(typeof id);
  await api
    .put(`schedules/schedules/${id}/`, {
      schedule_time: params.time,
      schedule_title: params.content,
    })
    .then(success)
    .catch(fail);
}
async function deleteSchedule(id, success, fail) {
  await api.delete(`schedules/schedules/${id}/`).then(success).catch(fail);
}

export { getMonthlySchedule, postSchedule, deleteSchedule, putSchedule };
